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
        self.company_code = parser.get_code()  # 追加！

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
    def _escape_ns(self, ns_url):  # self 追加！
        """lxml用に名前空間をエスケープ"""
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
        return (end_month % 12) + 1  # 3月決算 → 4月開始

    # =============================
    # 期間情報抽出（修正済み）
    # =============================
    def extract_period_info(self):
        try:
            tree = etree.parse(self.pl_file_path)
            root = tree.getroot()
            namespaces = root.nsmap

            period_end_date = None

            # --- 1. コンテキストから instant / endDate ---
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

            # --- 2. DocumentPeriodEndDate ---
            if period_end_date is None:
                for ns_key, ns_url in namespaces.items():
                    if 'jpcrp' in ns_url.lower():
                        tag_name = f'{{{{{self._escape_ns(ns_url)}}}}}DocumentPeriodEndDate'  # self. 追加！
                        elem = root.find(f'.//{tag_name}')
                        if elem is not None and elem.text and re.match(r'\d{4}-\d{2}-\d{2}', elem.text.strip()):
                            period_end_date = datetime.strptime(elem.text.strip(), '%Y-%m-%d').date()
                            break

            # --- 3. ファイル名から ---
            if period_end_date is None:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', self.file_name)
                if m:
                    period_end_date = datetime.strptime(m.group(1), '%Y-%m-%d').date()

            if not period_end_date:
                print(f'警告: 期間終了日を特定できませんでした - {self.file_name}')
                return None, None, None

            # --- 年度・四半期判定 ---
            fiscal_start_month = self.get_fiscal_start_month()
            fiscal_year = period_end_date.year
            if period_end_date.month < fiscal_start_month:
                fiscal_year -= 1

            month_in_fiscal = (period_end_date.month - fiscal_start_month + 12) % 12 + 1
            if month_in_fiscal <= 3:
                period = 'Q1'
            elif month_in_fiscal <= 6:
                period = 'Q2'
            elif month_in_fiscal <= 9:
                period = 'Q3'
            else:
                period = 'Q4'

            print(f'期間情報: 終了日={period_end_date}, {period}, 年度: {fiscal_year}')
            return period, fiscal_year, period_end_date

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            import traceback
            traceback.print_exc()
            return None, None, None

    # =============================
    # DB挿入
    # =============================
    def insert_to_pl_db(self):
        try:
            plfilenameparser = PlFilenameParser(self.pl_file_path)
            filename = plfilenameparser.get_filename()
            code = plfilenameparser.get_code()
            publicday = plfilenameparser.get_public_day()

            # 期間情報取得（3つ返すが、period, fiscal_year のみ使用）
            period, fiscal_year, _ = self.extract_period_info()
            if period is None or fiscal_year is None:
                print(f'スキップ: 期間情報が取得できませんでした - {filename}')
                return

            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()

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

            # IFRS
            if 'iffr' in self.file_name and 'pl' in self.file_name:
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

                print(f'IFRS PLデータを挿入: {code} - {period} {fiscal_year}年度')

            # 日本GAAP
            elif 'jpfr' in self.file_name and 'pl' in self.file_name:
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

                print(f'日本GAAP PLデータを挿入: {code} - {period} {fiscal_year}年度')

            conn.commit()

        except Exception as e:
            print(f'PLデータ挿入エラー: {e}')
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()


# =============================
# テスト実行
# =============================
if __name__ == '__main__':
    test_files = [
        r'E:\Zip_files\1301\0600000-qcpc11-tse-qcedjpfr-13010-2023-12-31-01-2024-02-02-ixbrl.htm'
    ]

    for pl_file_path in test_files:
        if os.path.exists(pl_file_path):
            print(f'\n処理中: {pl_file_path}')
            inserter = PlDBInserter(pl_file_path)
            inserter.insert_to_pl_db()
        else:
            print(f'ファイルが見つかりません: {pl_file_path}')