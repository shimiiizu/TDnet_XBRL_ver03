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
        XBRLファイルから期間情報を抽出し、四半期と年度を判定

        Returns:
        --------
        tuple: (period, fiscal_year)
            period: 'Q1', 'Q2', 'Q3', 'Q4' or None
            fiscal_year: 年度（整数） or None
        """
        try:
            # XBRLファイルをパース
            tree = etree.parse(self.pl_file_path)
            root = tree.getroot()

            # 名前空間を取得
            namespaces = root.nsmap

            # context要素を探索
            contexts = root.findall('.//xbrli:context', namespaces) if 'xbrli' in namespaces else root.findall('.//{http://www.xbrl.org/2003/instance}context')

            start_date = None
            end_date = None

            # 各contextから期間情報を取得
            for context in contexts:
                # instantの場合はスキップ（期間ではなく時点情報）
                instant = context.find('.//{http://www.xbrl.org/2003/instance}instant')
                if instant is not None:
                    continue

                # period要素から開始日と終了日を取得
                period = context.find('.//{http://www.xbrl.org/2003/instance}period')
                if period is not None:
                    start = period.find('.//{http://www.xbrl.org/2003/instance}startDate')
                    end = period.find('.//{http://www.xbrl.org/2003/instance}endDate')

                    if start is not None and end is not None:
                        start_date = datetime.strptime(start.text, '%Y-%m-%d')
                        end_date = datetime.strptime(end.text, '%Y-%m-%d')

                        # 最も長い期間を採用（通常、CurrentYearDuration等）
                        if start_date and end_date:
                            break

            if start_date is None or end_date is None:
                print(f'警告: 期間情報を取得できませんでした - {self.file_name}')
                return None, None

            # 期間の長さを計算（月数）
            delta_days = (end_date - start_date).days
            delta_months = delta_days / 30.44  # 平均月日数

            # 年度を取得（終了日の年）
            fiscal_year = end_date.year

            # 四半期を判定
            period = None
            if 2.5 <= delta_months <= 4:  # 約3ヶ月
                period = 'Q1'
            elif 5.5 <= delta_months <= 7:  # 約6ヶ月
                period = 'Q2'
            elif 8.5 <= delta_months <= 10:  # 約9ヶ月
                period = 'Q3'
            elif 11 <= delta_months <= 13:  # 約12ヶ月
                period = 'Q4'
            else:
                print(f'警告: 期間が想定外です - {delta_months:.1f}ヶ月 ({self.file_name})')
                period = None

            print(f'期間情報: {start_date.date()} ~ {end_date.date()} ({delta_months:.1f}ヶ月) → {period}, 年度: {fiscal_year}')

            return period, fiscal_year

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            print(f'ファイル: {self.pl_file_path}')
            return None, None

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
                    FileName TEXT UNIQUE,
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

            # ファイル名が既に登録されているかチェック
            cursor.execute('SELECT COUNT(*) FROM PL WHERE FileName = ?', (filename,))

            if cursor.fetchone()[0] == 0:  # ファイルの情報がない場合にDBに挿入

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

            else:
                print(f'すでに{filename}は登録されています。')

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
        r'E:\Zip_files\3679\0301000-acpl01-tse-acedjpfr-36790-2016-03-31-01-2016-05-13-ixbrl.htm'
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