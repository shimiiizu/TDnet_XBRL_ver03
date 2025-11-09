"""
データベースにPLデータを保管する

"""

import sqlite3
import xbrl_pl_ifrs_parser
import xbrl_pl_japan_gaap_parser
from pl_filename_parser import PlFilenameParser
import os


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


    def insert_to_pl_db(self):
        try:
            plfilenameparser = PlFilenameParser(self.pl_file_path)
            filename = plfilenameparser.get_filename()
            code = plfilenameparser.get_code()
            publicday = plfilenameparser.get_public_day()

            # データベース接続
            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()

            # テーブルが存在しない場合は作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS PL (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Code TEXT,
                    FileName TEXT UNIQUE,
                    PublicDay TEXT,
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
                            (Code,FileName,PublicDay,RevenueIFRS,SellingGeneralAndAdministrativeExpensesIFRS,OperatingProfitLossIFRS,ProfitLossIFRS,DilutedEarningsLossPerShareIFRS)
                            VALUES (?,?,?,?,?,?,?,?)''',
                                   (code, filename, publicday, revenueifrs, sellinggeneralandadministrativeexpensesifrs,
                                    operatingprofitlossifrs, profitLossifrs, dilutedearningslosspershareifrs))

                    print(f'✓ IFRS PLデータを挿入: {code} - {publicday}')

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
                                            (Code,FileName,PublicDay,NetSales,SellingGeneralAndAdministrativeExpenses,OperatingIncome,OrdinaryIncome,NetIncome)
                                            VALUES (?,?,?,?,?,?,?,?)''',
                                   (code, filename, publicday, netsales, sellinggeneralandadministrativeexpenses,
                                    operatingincome, ordinaryincome, netincome))

                    print(f'✓ 日本GAAP PLデータを挿入: {code} - {publicday}')
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
        r'C:\Users\Shimizu\PycharmProjects\TDnet_XBRL_ver01\TDnet_XBRL\zip_files\9504\0301000-acpl01-tse-acedjpfr-95040-2015-03-31-01-2015-05-13-ixbrl.htm',
        r'E:\Zip_files\9504\0600000-qcpl11-tse-qcedjpfr-95040-2014-06-30-01-2014-08-12-ixbrl.htm'
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