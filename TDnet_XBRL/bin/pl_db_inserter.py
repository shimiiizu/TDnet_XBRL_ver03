"""
データベースにPLデータを保管する

"""

import sqlite3
import xbrl_pl_ifrs_parser
import xbrl_pl_japan_gaap_parser
from pl_filename_parser import PlFilenameParser
import os
from datetime import datetime
from lxml import etree


class PlDBInserter:

    def __init__(self, pl_file_path):
        self.pl_file_path = pl_file_path  # 通期のPLファイルのリスト
        self.file_name = os.path.basename(pl_file_path)

        # データベースパスを動的に設定（プロジェクトルートからの相対パス）
        # 現在のスクリプトの場所から相対的にDBパスを設定
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, '..', 'db')

        # dbフォルダが存在しない場合は作成
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f'データベースディレクトリを作成しました: {db_dir}')

        self.DB = os.path.join(db_dir, 'PL_DB.db')
        print(f'データベースパス: {self.DB}')

    def extract_period_info(self):
        """
        XBRLファイルのタグから期間情報を抽出し、四半期と年度を判定

        Returns:
        --------
        tuple: (period, fiscal_year, period_end_date)
            period: 'Q1', 'Q2', 'Q3', 'Q4' or None
            fiscal_year: 年度（整数） or None
            period_end_date: datetime.date or None
        """
        try:
            # ファイル読み込み
            tree = etree.parse(self.pl_file_path)
            root = tree.getroot()
            namespaces = root.nsmap

            # --- 1. 期間終了日を XBRL コンテキストから取得 ---
            period_end_date = None

            # コンテキストをすべて取得
            context_elements = root.findall('.//{http://www.xbrl.org/2003/instance}context')
            for ctx in context_elements:
                ctx_id = ctx.get('id', '')

                # 四半期・通期を示すコンテキストを優先
                if re.search(r'CurrentQuarterInstant|CurrentYTDEnd|CurrentQuarterEnd|PriorQuarterInstant|Instant',
                             ctx_id, re.I):
                    # <instant>2023-12-31</instant>
                    instant = ctx.find('.//{http://www.xbrl.org/2003/instance}instant')
                    if instant is not None and instant.text and re.match(r'\d{4}-\d{2}-\d{2}', instant.text):
                        period_end_date = datetime.strptime(instant.text.strip(), '%Y-%m-%d').date()
                        break

                    # <endDate>2023-12-31</endDate>
                    end_date_tag = ctx.find('.//{http://www.xbrl.org/2003/instance}endDate')
                    if end_date_tag is not None and end_date_tag.text and re.match(r'\d{4}-\d{2}-\d{2}',
                                                                                   end_date_tag.text):
                        period_end_date = datetime.strptime(end_date_tag.text.strip(), '%Y-%m-%d').date()
                        break

            # --- 2. フォールバック：DocumentPeriodEndDate（年次報告書用）---
            if period_end_date is None:
                # 名前空間動的対応
                for ns_key in namespaces:
                    if 'jpcrp' in namespaces[ns_key]:
                        tag_name = f'{{{_escape_ns(namespaces[ns_key])}}}DocumentPeriodEndDate'
                        elem = root.find(f'.//{tag_name}')
                        if elem is not None and elem.text and re.match(r'\d{4}-\d{2}-\d{2}', elem.text):
                            period_end_date = datetime.strptime(elem.text.strip(), '%Y-%m-%d').date()
                            break

            # --- 3. フォールバック：ファイル名から日付抽出 ---
            if period_end_date is None:
                # 例: 13010-2023-12-31-01-2024-02-02
                m = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(self.pl_file_path))
                if m:
                    period_end_date = datetime.strptime(m.group(1), '%Y-%m-%d').date()
                else:
                    print(f'警告: 期間終了日を特定できませんでした - {self.file_name}')
                    return None, None, None

            # --- 4. 会計年度開始月（fiscal_year_start_month）を推定 ---
            # 企業コードから事前にマッピングがあれば使う（例: 1301 → 4月始まり）
            fiscal_start_month = self.get_fiscal_start_month()  # 後述

            fiscal_year = period_end_date.year
            if period_end_date.month < fiscal_start_month:
                fiscal_year -= 1  # 例: 3月決算 → 3月末は前年度

            # --- 5. 四半期判定 ---
            period = None
            month_offset = (period_end_date.month - fiscal_start_month + 12) % 12 + 1

            if month_offset <= 3:
                period = 'Q1'
            elif month_offset <= 6:
                period = 'Q2'
            elif month_offset <= 9:
                period = 'Q3'
            elif month_offset <= 12:
                period = 'Q4'

            print(f'期間情報: 終了日={period_end_date}, {period}, 年度: {fiscal_year}')

            return period, fiscal_year, period_end_date

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            import traceback
            traceback.print_exc()
            print(f'ファイル: {self.pl_file_path}')
            return None, None, None

    def insert_to_pl_db(self):
        try:
            plfilenameparser = PlFilenameParser(self.pl_file_path)
            filename = plfilenameparser.get_filename()
            code = plfilenameparser.get_code()
            publicday = plfilenameparser.get_public_day()

            # 期間情報と年度を取得
            period, fiscal_year = self.extract_period_info()

            # データベース接続
            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()

            # テーブルが存在しない場合は作成（Period と FiscalYear カラムを追加）
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

            # IFRSの場合
            first_string = 'iffr'
            second_string = 'pl'
            if first_string in self.file_name and second_string in self.file_name:
                print(f'IFRS形式のPLファイルを処理中: {filename}')

                revenueifrs = xbrl_pl_ifrs_parser.get_RevenueIFRS(self.pl_file_path)
                sellinggeneralandadministrativeexpensesifrs = xbrl_pl_ifrs_parser.get_SellingGeneralAndAdministrativeExpensesIFRS(self.pl_file_path)
                operatingprofitlossifrs = xbrl_pl_ifrs_parser.get_OperatingProfitLossIFRS(self.pl_file_path)
                profitLossifrs = xbrl_pl_ifrs_parser.get_ProfitLossIFRS(self.pl_file_path)
                dilutedearningslosspershareifrs = xbrl_pl_ifrs_parser.get_DilutedEarningsLossPerShareIFRS(self.pl_file_path)

                cursor.execute('''INSERT INTO PL 
                        (Code,FileName,PublicDay,Period,FiscalYear,RevenueIFRS,SellingGeneralAndAdministrativeExpensesIFRS,OperatingProfitLossIFRS,ProfitLossIFRS,DilutedEarningsLossPerShareIFRS)
                        VALUES (?,?,?,?,?,?,?,?,?,?)''',
                               (code, filename, publicday, period, fiscal_year, revenueifrs, sellinggeneralandadministrativeexpensesifrs,
                                operatingprofitlossifrs, profitLossifrs, dilutedearningslosspershareifrs))

                print(f'✓ IFRS PLデータを挿入: {code} - {publicday} - {period} ({fiscal_year}年度)')

            # 日本GAAPの場合
            first_string = 'jpfr'
            second_string = 'pl'
            if first_string in self.file_name and second_string in self.file_name:
                print(f'日本GAAP形式のPLファイルを処理中: {filename}')

                netsales = xbrl_pl_japan_gaap_parser.get_NetSales(self.pl_file_path)
                sellinggeneralandadministrativeexpenses = xbrl_pl_japan_gaap_parser.get_SellingGeneralAndAdministrativeExpenses(self.pl_file_path)
                operatingincome = xbrl_pl_japan_gaap_parser.get_OperatingIncome(self.pl_file_path)
                ordinaryincome = xbrl_pl_japan_gaap_parser.get_OrdinaryIncome(self.pl_file_path)
                netincome = xbrl_pl_japan_gaap_parser.get_NetIncome(self.pl_file_path)

                cursor.execute('''INSERT INTO PL 
                                        (Code,FileName,PublicDay,Period,FiscalYear,NetSales,SellingGeneralAndAdministrativeExpenses,OperatingIncome,OrdinaryIncome,NetIncome)
                                        VALUES (?,?,?,?,?,?,?,?,?,?)''',
                               (code, filename, publicday, period, fiscal_year, netsales, sellinggeneralandadministrativeexpenses,
                                operatingincome, ordinaryincome, netincome))

                print(f'✓ 日本GAAP PLデータを挿入: {code} - {publicday} - {period} ({fiscal_year}年度)')
                print(f'  売上: {netsales}, 営業利益: {operatingincome}, 純利益: {netincome}')

            conn.commit()

        except sqlite3.Error as e:
            print(f'データベースエラー: {e}')
            print(f'データベースパス: {self.DB}')
            if 'conn' in locals():
                conn.rollback()

        except Exception as e:
            print(f'PLデータ挿入エラー: {e}')
            print(f'ファイル: {self.pl_file_path}')
            if 'conn' in locals():
                conn.rollback()

        finally:
            if 'conn' in locals():
                conn.close()


if __name__ == '__main__':
    # テスト用ファイルパス（環境に合わせて変更してください）
    test_files = [
        r'E:\Zip_files\1301\0600000-qcpc11-tse-qcedjpfr-13010-2023-12-31-01-2024-02-02-ixbrl.htm'
    ]

    for pl_file_path in test_files:
        if os.path.exists(pl_file_path):
            print(f'\n処理中: {pl_file_path}')

            plfilenameparser = PlFilenameParser(pl_file_path)
            print(f'企業コード: {plfilenameparser.get_code()}')
            print(f'ファイル名: {plfilenameparser.get_filename()}')
            print(f'公表日: {plfilenameparser.get_public_day()}')

            pldbinserter = PlDBInserter(pl_file_path)
            pldbinserter.insert_to_pl_db()
        else:
            print(f'ファイルが見つかりません: {pl_file_path}')