from flask import Flask, render_template, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import yfinance as yf

app = Flask(__name__)

# データベースファイルのパス（相対パスで取得）
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
BS_DB_PATH = os.path.join(project_root, 'db', 'BS_DB.db')
PL_DB_PATH = os.path.join(project_root, 'db', 'PL_DB.db')

print(f"BSデータベースパス: {BS_DB_PATH}")
print(f"PLデータベースパス: {PL_DB_PATH}")


def get_bs_db_connection():
    """BS用のデータベース接続"""
    conn = sqlite3.connect(BS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_pl_db_connection():
    """PL用のデータベース接続"""
    conn = sqlite3.connect(PL_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/companies')
def get_companies():
    """全社名リストを取得（BSとPLから）"""
    companies_dict = {}

    # BSデータベースから取得
    try:
        conn_bs = get_bs_db_connection()
        bs_companies = conn_bs.execute('''
            SELECT DISTINCT CompanyName, Code 
            FROM BS 
            WHERE Code IS NOT NULL
            ORDER BY CompanyName
        ''').fetchall()
        conn_bs.close()

        for company in bs_companies:
            code = company['Code']
            companies_dict[code] = {
                'name': company['CompanyName'],
                'code': code,
                'hasBS': True,
                'hasPL': False
            }
    except Exception as e:
        print(f"BS取得エラー: {e}")

    # PLデータベースから取得
    try:
        conn_pl = get_pl_db_connection()
        pl_companies = conn_pl.execute('''
            SELECT DISTINCT Code 
            FROM PL 
            WHERE Code IS NOT NULL
        ''').fetchall()
        conn_pl.close()

        for company in pl_companies:
            code = company['Code']
            if code in companies_dict:
                companies_dict[code]['hasPL'] = True
            else:
                companies_dict[code] = {
                    'name': f'Company {code}',
                    'code': code,
                    'hasBS': False,
                    'hasPL': True
                }
    except Exception as e:
        print(f"PL取得エラー: {e}")

    return jsonify(list(companies_dict.values()))


@app.route('/api/company/<code>')
def get_company_by_code(code):
    """証券コードで会社を検索"""
    conn_bs = get_bs_db_connection()

    company = conn_bs.execute('''
        SELECT DISTINCT CompanyName, Code 
        FROM BS 
        WHERE Code = ?
        LIMIT 1
    ''', (code,)).fetchone()
    conn_bs.close()

    if company:
        # PLデータの有無を確認
        try:
            conn_pl = get_pl_db_connection()
            pl_exists = conn_pl.execute('''
                SELECT COUNT(*) as count FROM PL WHERE Code = ?
            ''', (code,)).fetchone()
            conn_pl.close()
            has_pl = pl_exists['count'] > 0
        except:
            has_pl = False

        return jsonify({
            'name': company['CompanyName'],
            'code': company['Code'],
            'hasBS': True,
            'hasPL': has_pl
        })
    else:
        return jsonify({'error': 'Company not found'}), 404


@app.route('/api/stock-price/<code>')
def get_stock_price(code):
    """株価データを取得"""
    try:
        # 日本株の証券コード（.Tを付ける）
        ticker = f"{code}.T"
        stock = yf.Ticker(ticker)

        # 過去10年分のデータを取得
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10 * 365)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            return jsonify({'error': 'No stock data found'}), 404

        # データを整形
        stock_data = []
        for index, row in hist.iterrows():
            stock_data.append({
                'date': index.strftime('%Y-%m-%d'),
                'close': float(row['Close'])
            })

        return jsonify(stock_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bs-data/<company_name>')
def get_bs_data(company_name):
    """特定の会社のBSデータを取得"""
    conn = get_bs_db_connection()
    bs_data = conn.execute('''
        SELECT 
            EndDay,
            Assets,
            NetAssets,
            Equity,
            CurrentAssets,
            CashAndDeposits,
            CashAndCashEquivalent,
            PropertyPlantAndEquipment,
            RetainedEarnings,
            AccountingStandard,
            FinancialReportType
        FROM BS 
        WHERE CompanyName = ?
        ORDER BY EndDay
    ''', (company_name,)).fetchall()
    conn.close()

    return jsonify([{
        'date': row['EndDay'],
        'assets': row['Assets'],
        'netAssets': row['NetAssets'],
        'equity': row['Equity'],
        'currentAssets': row['CurrentAssets'],
        'cashAndDeposits': row['CashAndDeposits'],
        'cashAndCashEquivalent': row['CashAndCashEquivalent'],
        'propertyPlantAndEquipment': row['PropertyPlantAndEquipment'],
        'retainedEarnings': row['RetainedEarnings'],
        'accountingStandard': row['AccountingStandard'],
        'financialReportType': row['FinancialReportType']
    } for row in bs_data])


@app.route('/api/pl-data/<code>')
def get_pl_data(code):
    """特定の会社のPLデータを取得（証券コードで検索）"""
    try:
        conn = get_pl_db_connection()
        pl_data = conn.execute('''
            SELECT 
                Code,
                FileName,
                PublicDay,
                NetSales,
                SellingGeneralAndAdministrativeExpenses,
                OperatingIncome,
                OrdinaryIncome,
                NetIncome,
                RevenueIFRS,
                SellingGeneralAndAdministrativeExpensesIFRS,
                OperatingProfitLossIFRS,
                ProfitLossIFRS,
                DilutedEarningsLossPerShareIFRS
            FROM PL 
            WHERE Code = ?
            ORDER BY PublicDay
        ''', (code,)).fetchall()
        conn.close()

        return jsonify([{
            'code': row['Code'],
            'fileName': row['FileName'],
            'publicDay': row['PublicDay'],
            'netSales': row['NetSales'],
            'sellingExpenses': row['SellingGeneralAndAdministrativeExpenses'],
            'operatingIncome': row['OperatingIncome'],
            'ordinaryIncome': row['OrdinaryIncome'],
            'netIncome': row['NetIncome'],
            'revenueIFRS': row['RevenueIFRS'],
            'sellingExpensesIFRS': row['SellingGeneralAndAdministrativeExpensesIFRS'],
            'operatingProfitLossIFRS': row['OperatingProfitLossIFRS'],
            'profitLossIFRS': row['ProfitLossIFRS'],
            'dilutedEarningsLossPerShareIFRS': row['DilutedEarningsLossPerShareIFRS']
        } for row in pl_data])

    except Exception as e:
        print(f"PLデータ取得エラー: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/financial-summary/<code>')
def get_financial_summary(code):
    """BSとPLの統合データを取得"""
    try:
        # 会社情報を取得
        conn_bs = get_bs_db_connection()
        company = conn_bs.execute('''
            SELECT DISTINCT CompanyName, Code 
            FROM BS 
            WHERE Code = ?
            LIMIT 1
        ''', (code,)).fetchone()

        if not company:
            return jsonify({'error': 'Company not found'}), 404

        # BSデータを取得
        bs_data = conn_bs.execute('''
            SELECT 
                EndDay as date,
                Assets,
                NetAssets,
                Equity,
                CurrentAssets
            FROM BS 
            WHERE Code = ?
            ORDER BY EndDay
        ''', (code,)).fetchall()
        conn_bs.close()

        # PLデータを取得
        conn_pl = get_pl_db_connection()
        pl_data = conn_pl.execute('''
            SELECT 
                PublicDay as date,
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
        conn_pl.close()

        return jsonify({
            'company': {
                'name': company['CompanyName'],
                'code': company['Code']
            },
            'bs': [{
                'date': row['date'],
                'assets': row['Assets'],
                'netAssets': row['NetAssets'],
                'equity': row['Equity'],
                'currentAssets': row['CurrentAssets']
            } for row in bs_data],
            'pl': [{
                'date': row['date'],
                'netSales': row['NetSales'] or row['RevenueIFRS'],
                'operatingIncome': row['OperatingIncome'] or row['OperatingProfitLossIFRS'],
                'ordinaryIncome': row['OrdinaryIncome'],
                'netIncome': row['NetIncome'] or row['ProfitLossIFRS']
            } for row in pl_data]
        })

    except Exception as e:
        print(f"統合データ取得エラー: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # データベースの存在確認
    bs_exists = os.path.exists(BS_DB_PATH)
    pl_exists = os.path.exists(PL_DB_PATH)

    if bs_exists:
        print(f"✓ BSデータベースが見つかりました: {BS_DB_PATH}")
    else:
        print(f"⚠ BSデータベースが見つかりません: {BS_DB_PATH}")

    if pl_exists:
        print(f"✓ PLデータベースが見つかりました: {PL_DB_PATH}")
    else:
        print(f"⚠ PLデータベースが見つかりません: {PL_DB_PATH}")

    if bs_exists or pl_exists:
        app.run(debug=True, port=5001)
    else:
        print("エラー: データベースが見つかりません")