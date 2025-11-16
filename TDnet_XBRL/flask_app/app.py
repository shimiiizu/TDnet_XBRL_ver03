from flask import Flask, render_template, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import yfinance as yf

app = Flask(__name__)

# データベースパス
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
BS_DB_PATH = os.path.join(project_root, 'db', 'BS_DB.db')
PL_DB_PATH = os.path.join(project_root, 'db', 'PL_DB.db')

print(f"BSデータベースパス: {BS_DB_PATH}")
print(f"PLデータベースパス: {PL_DB_PATH}")


def get_bs_db_connection():
    conn = sqlite3.connect(BS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_pl_db_connection():
    conn = sqlite3.connect(PL_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def convert_to_quarterly_from_period(data):
    """Period情報を使って累計データを四半期ごとの差分に変換"""
    if not data:
        return []

    def safe_num(x):
        if x is None:
            return None
        try:
            return float(x)
        except Exception:
            return None

    metrics = ['netSales', 'operatingIncome', 'ordinaryIncome', 'netIncome']

    # FiscalYearとPeriodでグループ化
    from collections import defaultdict
    groups = defaultdict(dict)

    for item in data:
        fiscal_year = item.get('fiscalYear')
        period = item.get('period')

        if not fiscal_year or not period:
            continue

        # Period から quarter番号を取得
        period_map = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
        quarter = period_map.get(period)

        if quarter is None:
            continue

        # 数値に変換（元データの累計値を保持）
        parsed_item = {
            'original': item,
            'fiscalYear': fiscal_year,
            'quarter': quarter,
            'period': period
        }
        for m in metrics:
            parsed_item[m] = safe_num(item.get(m))

        groups[fiscal_year][quarter] = parsed_item

    result = []

    # 各年度ごとに処理
    for fiscal_year in sorted(groups.keys()):
        year_data = groups[fiscal_year]

        for quarter in [1, 2, 3, 4]:
            if quarter not in year_data:
                continue

            current = year_data[quarter]
            out = dict(current['original'])

            # Q1はそのまま、Q2以降は差分計算（元データの累計値を使用）
            if quarter == 1:
                # Q1はそのまま使用
                for m in metrics:
                    val = current.get(m)
                    if val is not None and float(val).is_integer():
                        out[m] = int(val)
                    else:
                        out[m] = val
            else:
                # Q2, Q3, Q4は前のクオーターとの差分（元データ同士で計算）
                prev_quarter = quarter - 1

                if prev_quarter in year_data:
                    previous = year_data[prev_quarter]
                    for m in metrics:
                        cur = current.get(m)  # 元データの累計値
                        prev = previous.get(m)  # 元データの累計値

                        if cur is None or prev is None:
                            out[m] = None
                        else:
                            out[m] = cur - prev
                            if out[m] is not None and float(out[m]).is_integer():
                                out[m] = int(out[m])
                else:
                    # 前のクオーターがない場合はNone
                    for m in metrics:
                        out[m] = None

            out['_fiscalYear'] = fiscal_year
            out['_quarter'] = quarter
            result.append(out)

    # FiscalYearとQuarterでソート
    result.sort(key=lambda x: (x.get('_fiscalYear', 0), x.get('_quarter', 0)))

    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/companies')
def get_companies():
    companies_dict = {}

    # BSから取得
    try:
        conn = get_bs_db_connection()
        rows = conn.execute('SELECT DISTINCT CompanyName, Code FROM BS WHERE Code IS NOT NULL').fetchall()
        for row in rows:
            code = row['Code']
            companies_dict[code] = {'name': row['CompanyName'], 'code': code, 'hasBS': True, 'hasPL': False}
        conn.close()
    except Exception as e:
        print(f"BS会社リスト取得エラー: {e}")

    # PLから取得
    try:
        conn = get_pl_db_connection()
        rows = conn.execute('SELECT DISTINCT Code FROM PL WHERE Code IS NOT NULL').fetchall()
        for row in rows:
            code = row['Code']
            if code in companies_dict:
                companies_dict[code]['hasPL'] = True
            else:
                companies_dict[code] = {'name': f'Company {code}', 'code': code, 'hasBS': False, 'hasPL': True}
        conn.close()
    except Exception as e:
        print(f"PL会社リスト取得エラー: {e}")

    return jsonify(list(companies_dict.values()))


@app.route('/api/bs-data/<company_name>')
def get_bs_data(company_name):
    conn = get_bs_db_connection()
    rows = conn.execute('''
        SELECT 
            EndDay,
            Assets,
            NetAssets,
            CurrentAssets,
            COALESCE(CashAndDeposits, CashAndCashEquivalent, 0) AS cash,
            PropertyPlantAndEquipment AS ppe,
            RetainedEarnings
        FROM BS 
        WHERE CompanyName = ?
        ORDER BY EndDay
    ''', (company_name,)).fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'term': row['EndDay'][:7],
            'assets': row['Assets'],
            'netAssets': row['NetAssets'],
            'currentAssets': row['CurrentAssets'],
            'cash': row['cash'],
            'ppe': row['ppe'],
            'retainedEarnings': row['RetainedEarnings']
        })
    return jsonify(data)


@app.route('/api/pl-data/<code>')
def get_pl_data(code):
    """PLデータを取得し、Periodを使って四半期ごとの差分に変換"""
    try:
        conn = get_pl_db_connection()
        rows = conn.execute('''
            SELECT 
                PublicDay,
                Period,
                FiscalYear,
                NetSales,
                OperatingIncome,
                OrdinaryIncome,
                NetIncome,
                RevenueIFRS,
                OperatingProfitLossIFRS,
                ProfitLossIFRS
            FROM PL 
            WHERE Code = ?
            ORDER BY FiscalYear, Period
        ''', (code,)).fetchall()
        conn.close()

        data = []
        for row in rows:
            data.append({
                'term': row['PublicDay'][:7] if row['PublicDay'] else None,
                'period': row['Period'],
                'fiscalYear': row['FiscalYear'],
                'netSales': row['NetSales'] or row['RevenueIFRS'],
                'operatingIncome': row['OperatingIncome'] or row['OperatingProfitLossIFRS'],
                'ordinaryIncome': row['OrdinaryIncome'],
                'netIncome': row['NetIncome'] or row['ProfitLossIFRS']
            })

        converted_data = convert_to_quarterly_from_period(data)
        print(f"PLデータ変換: {len(data)}件 → {len(converted_data)}件（四半期ごと）")
        return jsonify(converted_data)

    except Exception as e:
        print(f"PLデータ取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/stock-price/<code>')
def get_stock_price(code):
    try:
        ticker = f"{code}.T"
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10 * 365)
        hist = stock.history(start=start_date, end=end_date, interval="1d")

        if hist.empty:
            return jsonify([])

        data = [{'date': date.strftime('%Y-%m-%d'), 'price': round(float(row['Close']), 2)}
                for date, row in hist.iterrows()]
        return jsonify(data)

    except Exception as e:
        print(f"株価取得エラー ({code}): {e}")
        return jsonify([]), 500


@app.route('/api/company/<code>')
def get_company_by_code(code):
    conn = get_bs_db_connection()
    row = conn.execute('SELECT DISTINCT CompanyName FROM BS WHERE Code = ? LIMIT 1', (code,)).fetchone()
    conn.close()
    if row:
        return jsonify({'name': row['CompanyName'], 'code': code})
    return jsonify({'error': 'Not found'}), 404


@app.route('/api/financial-summary/<code>')
def get_financial_summary(code):
    try:
        conn_bs = get_bs_db_connection()
        company = conn_bs.execute('SELECT DISTINCT CompanyName FROM BS WHERE Code = ? LIMIT 1', (code,)).fetchone()
        if not company:
            return jsonify({'error': 'Company not found'}), 404

        bs_rows = conn_bs.execute('SELECT EndDay, Assets, NetAssets FROM BS WHERE Code = ? ORDER BY EndDay',
                                  (code,)).fetchall()
        conn_bs.close()

        conn_pl = get_pl_db_connection()
        pl_rows = conn_pl.execute(
            'SELECT PublicDay, NetSales, OperatingIncome FROM PL WHERE Code = ? ORDER BY PublicDay', (code,)).fetchall()
        conn_pl.close()

        return jsonify({
            'company': {'name': company['CompanyName'], 'code': code},
            'bs': [{'date': r['EndDay'][:7], 'assets': r['Assets'], 'netAssets': r['NetAssets']} for r in bs_rows],
            'pl': [{'date': r['PublicDay'][:7], 'netSales': r['NetSales'], 'operatingIncome': r['OperatingIncome']}
                   for r in pl_rows]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    bs_exists = os.path.exists(BS_DB_PATH)
    pl_exists = os.path.exists(PL_DB_PATH)

    if bs_exists:
        print(f"✓ BSデータベース: {BS_DB_PATH}")
    else:
        print(f"⚠ BS DB なし: {BS_DB_PATH}")

    if pl_exists:
        print(f"✓ PLデータベース: {PL_DB_PATH}")
    else:
        print(f"⚠ PL DB なし: {PL_DB_PATH}")

    if bs_exists or pl_exists:
        print("\nFlaskサーバー起動中...")
        app.run(debug=True, port=5001)
    else:
        print("エラー: データベースが見つからないため起動できません")