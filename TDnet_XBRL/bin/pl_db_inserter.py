import sqlite3
import xbrl_pl_ifrs_parser
import xbrl_pl_japan_gaap_parser
from pl_filename_parser import PlFilenameParser
import os
from datetime import datetime
from lxml import etree
import re


class PlDBInserter:

    def __init__(self, pl_file_path):
        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)

        # 企業コードをファイル名から取得
        parser = PlFilenameParser(pl_file_path)
        self.company_code = parser.get_code()

        # データベースパス
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, '..', 'db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f'データベースディレクトリを作成しました: {db_dir}')
        self.DB = os.path.join(db_dir, 'PL_DB.db')
        print(f'データベースパス: {self.DB}')

    # =============================
    # 補助関数：名前空間エスケープ
    # =============================
    def _escape_ns(self, ns_url):
        return ns_url.replace('http://', 'http/').replace('/', '_')

    # =============================
    # 補助関数：会計年度開始月
    # =============================
    def get_fiscal_start_month(self):
        fiscal_end_month_map = {
            '1301': 3,   # 極洋
            '7203': 3,   # トヨタ
            '9984': 3,   # ソフトバンク
            '9501': 3,   # 東京電力
            '9432': 9,   # NTT
        }
        end_month = fiscal_end_month_map.get(self.company_code, 3)
        return (end_month % 12) + 1

    # =============================
    # 期間情報抽出
    # =============================
    def extract_period_info(self):
        try:
            tree = etree.parse(self.pl_file_path)
            root = tree.getroot()
            namespaces = root.nsmap

            period_end_date = None

            # 1. コンテキストから instant / endDate
            for ctx in root.findall('.//{http://www.xbrl.org/2003/instance}context'):
                ctx_id = ctx.get('id', '')
                if re.search(r'CurrentQuarterInstant|CurrentYTDEnd|CurrentQuarterEnd|Instant', ctx_id, re.I):
                    instant = ctx.find('.//{http://www.xbrl.org/2003/instance}instant')
                    if instant is not None and instant.text and re.match(r'\d{4}-\d{2}-\d{2}', instant.text.strip()):
                        period_end_date = datetime.strptime(instant.text.strip(), '%Y-%m-%d').date()
                        break
                    end_tag = ctx.find('.//{http://www.xbrl.org/2003/instance}endDate')
                    if end_tag is not None and end_tag.text and re.match(r'\d{4}-\d{2}-\d{2}', end_tag.text.strip()):
                        period_end_date = datetime.strptime(end_tag.text.strip(), '%Y-%m-%d').date()
                        break

            # 2. DocumentPeriodEndDate
            if period_end_date is None:
                for ns_key, ns_url in namespaces.items():
                    if 'jpcrp' in ns_url.lower():
                        tag_name = f'{{{{{self._escape_ns(ns_url)}}}}}DocumentPeriodEndDate'
                        elem = root.find(f'.//{tag_name}')
                        if elem is not None and elem.text and re.match(r'\d{4}-\d{2}-\d{2}', elem.text.strip()):
                            period_end_date = datetime.strptime(elem.text.strip(), '%Y-%m-%d').date()
                            break

            # 3. ファイル名から
            if period_end_date is None:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', self.file_name)
                if m:
                    period_end_date = datetime.strptime(m.group(1), '%Y-%m-%d').date()

            if not period_end_date:
                print(f'警告: 期間終了日を特定できませんでした - {self.file_name}')
                return None, None, None

            # 年度・四半期判定
            fiscal_start_month = self.get_fiscal_start_month()
            fiscal_year = period_end_date.year
            if period_end_date.month < fiscal_start_month:
                fiscal_year -= 1

            month_in_fiscal = (period_end_date.month - fiscal_start_month + 12) % 12 + 1
            period = 'Q1' if month_in_fiscal <= 3 else 'Q2' if month_in_fiscal <= 6 else 'Q3' if month_in_fiscal <= 9 else 'Q4'

            print(f'期間情報: 終了日={period_end_date}, {period}, 年度: {fiscal_year}')
            return period, fiscal_year, period_end_date

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            import traceback
            traceback.print_exc()
            return None, None, None

    # =============================
    # DB挿入（重複チェックなし・常に追加）
    # =============================
    def insert_to_pl_db(self):
        try:
            plparser = PlFilenameParser(self.pl_file_path)
            filename = plparser.get_filename()
            code = plparser.get_code()
            publicday = plparser.get_public_day()

            # 期間情報取得
            period, fiscal_year, _ = self.extract_period_info()
            if period is None or fiscal_year is None:
                print(f'スキップ: 期間情報が取得できませんでした - {filename}')
                return

            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()

            # テーブル作成（初回のみ）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS PL (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Code TEXT,
                    FileName TEXT,
                    PublicDay TEXT,
                    Period TEXT,
                    FiscalYear INTEGER,
                    RevenueIFRS REAL,
                    SellingGeneralAndAdministrativeExpensesIFRS REAL,
                    OperatingProfitLossIFRS REAL,
                    ProfitLossIFRS REAL,
                    DilutedEarningsLossPerShareIFRS REAL,
                    NetSales REAL,
                    SellingGeneralAndAdministrativeExpenses REAL,
                    OperatingIncome REAL,
                    OrdinaryIncome REAL,
                    NetIncome REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            inserted = True

            # --- IFRS ---
            if 'iffr' in self.file_name.lower() and 'pl' in self.file_name.lower():
                print(f'IFRS形式のPLファイルを処理中: {filename}')

                revenueifrs = xbrl_pl_ifrs_parser.get_RevenueIFRS(self.pl_file_path)
                sga_ifrs = xbrl_pl_ifrs_parser.get_SellingGeneralAndAdministrativeExpensesIFRS(self.pl_file_path)
                op_ifrs = xbrl_pl_ifrs_parser.get_OperatingProfitLossIFRS(self.pl_file_path)
                profit_ifrs = xbrl_pl_ifrs_parser.get_ProfitLossIFRS(self.pl_file_path)
                eps_ifrs = xbrl_pl_ifrs_parser.get_DilutedEarningsLossPerShareIFRS(self.pl_file_path)

                cursor.execute('''
                    INSERT INTO PL 
                    (Code,FileName,PublicDay,Period,FiscalYear,
                     RevenueIFRS,SellingGeneralAndAdministrativeExpensesIFRS,
                     OperatingProfitLossIFRS,ProfitLossIFRS,DilutedEarningsLossPerShareIFRS)
                    VALUES (?,?,?,?,?,?,?,?,?,?)
                ''', (code, filename, publicday, period, fiscal_year,
                      revenueifrs, sga_ifrs, op_ifrs, profit_ifrs, eps_ifrs))

                print(f'IFRS PLデータを登録: {code} | {period} | {fiscal_year}年度')
                inserted = True

            # --- 日本GAAP ---
            elif 'jpfr' in self.file_name.lower() and 'pl' in self.file_name.lower():
                print(f'日本GAAP形式のPLファイルを処理中: {filename}')

                netsales = xbrl_pl_japan_gaap_parser.get_NetSales(self.pl_file_path)
                sga = xbrl_pl_japan_gaap_parser.get_SellingGeneralAndAdministrativeExpenses(self.pl_file_path)
                op = xbrl_pl_japan_gaap_parser.get_OperatingIncome(self.pl_file_path)
                ordinary = xbrl_pl_japan_gaap_parser.get_OrdinaryIncome(self.pl_file_path)
                netincome = xbrl_pl_japan_gaap_parser.get_NetIncome(self.pl_file_path)

                cursor.execute('''
                    INSERT INTO PL 
                    (Code,FileName,PublicDay,Period,FiscalYear,
                     NetSales,SellingGeneralAndAdministrativeExpenses,
                     OperatingIncome,OrdinaryIncome,NetIncome)
                    VALUES (?,?,?,?,?,?,?,?,?,?)
                ''', (code, filename, publicday, period, fiscal_year,
                      netsales, sga, op, ordinary, netincome))

                print(f'日本GAAP PLデータを登録: {code} | {period} | {fiscal_year}年度 | 売上={netsales}')
                inserted = True

            if inserted:
                conn.commit()
                print(f'登録成功: {filename}')
            else:
                print(f'該当なし: IFRS でも JPGAAP でもないファイル - {filename}')

        except Exception as e:
            print(f'挿入エラー: {e}')
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()


# =============================
# テスト実行（複数ファイル対応）
# =============================
if __name__ == '__main__':
    test_files = [
        r'E:\Zip_files\1301\0501000-anpl01-tse-acedjpfr-13010-2016-03-31-01-2016-05-09-ixbrl.htm'
        # 複数追加可能
    ]

    for pl_file_path in test_files:
        if os.path.exists(pl_file_path):
            print(f'\n{"="*60}')
            print(f'処理開始: {pl_file_path}')
            print(f'{"="*60}')
            inserter = PlDBInserter(pl_file_path)
            inserter.insert_to_pl_db()
        else:
            print(f'ファイルが見つかりません: {pl_file_path}')