from flask import Flask, render_template, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import yfinance as yf
from collections import defaultdict

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


def convert_to_quarterly(data):
    """累計データを四半期ごとの差分に変換"""
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

    parsed = []
    for item in data:
        term = item.get('term')
        if not term:
            continue
        try:
            y_str, m_str = term.split('-')[:2]
            year = int(y_str)
            month = int(m_str)
        except Exception:
            continue

        # 3月決算想定: Apr-Jun Q1, Jul-Sep Q2, Oct-Dec Q3, Jan-Mar Q4
        if 4 <= month <= 6:
            fiscal_year = year
            quarter = 1
        elif 7 <= month <= 9:
            fiscal_year = year
            quarter = 2
        elif 10 <= month <= 12:
            fiscal_year = year
            quarter = 3
        else:  # 1-3
            fiscal_year = year - 1
            quarter = 4

        # 四半期終了日のソートキー
        if quarter == 1:
            end_year, end_month, end_day = fiscal_year, 6, 30
        elif quarter == 2:
            end_year, end_month, end_day = fiscal_year, 9, 30
        elif quarter == 3:
            end_year, end_month, end_day = fiscal_year, 12, 31
        else:
            end_year, end_month, end_day = fiscal_year + 1, 3, 31

        sort_key = (end_year, end_month, end_day)

        parsed_item = {
            'original': item,
            'term': term,
            'fiscalYear': fiscal_year,
            'quarter': quarter,
            'sort_key': sort_key
        }
        for m in metrics:
            parsed_item[m] = safe_num(item.get(m))
        parsed.append(parsed_item)

    groups = defaultdict(list)
    for p in parsed:
        groups[p['fiscalYear']].append(p)

    result = []

    for fy in sorted(groups.keys()):
        year_group = groups[fy]
        year_group.sort(key=lambda x: x['sort_key'])

        previous = None
        for item in year_group:
            out = dict(item['original'])
            for m in metrics:
                cur = item.get(m)
                prev = previous.get(m) if previous is not None else None

                if cur is None:
                    out[m] = None
                else:
                    if prev is None:
                        out[m] = cur
                    else:
                        out[m] = cur - prev

                    if out[m] is not None and float(out[m]).is_integer():
                        out[m] = int(out[m])

            out['_fiscalYear'] = item['fiscalYear']
            out['_quarter'] = item['quarter']
            result.append(out)
            previous = item

    # 終了日順でソート
    result.sort(key=lambda x: (
        (x.get('_fiscalYear') if x.get('_quarter') != 4 else x.get('_fiscalYear') + 1),
        {1: 6, 2: 9, 3: 12, 4: 3}[x.get('_quarter')],
        {1: 30, 2: 30, 3: 31, 4: 31}[x.get('_quarter')]
    ))

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
    """PLデータを取得し、四半期ごとの差分に変換"""
    try:
        conn = get_pl_db_connection()
        rows = conn.execute('''
            SELECT 
                PublicDay,
                NetSales,
                OperatingIncome,
                OrdinaryIncome,
                NetIncome,
                RevenueIFRS,
                OperatingProfitLossIFRS,
                ProfitLossIFRS
            FROM PL 
            WHERE Code = ?
            ORDER BY PublicDay
        ''', (code,)).fetchall()
        conn.close()

        data = []
        for row in rows:
            data.append({
                'term': row['PublicDay'][:7],
                'netSales': row['NetSales'] or row['RevenueIFRS'],
                'operatingIncome': row['OperatingIncome'] or row['OperatingProfitLossIFRS'],
                'ordinaryIncome': row['OrdinaryIncome'],
                'netIncome': row['NetIncome'] or row['ProfitLossIFRS']
            })

        converted_data = convert_to_quarterly(data)
        print(f"PLデータ変換: {len(data)}件 → {len(converted_data)}件（四半期ごと）")
        return jsonify(converted_data)

    except Exception as e:
        print(f"PLデータ取得エラー: {e}")
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
