# ============================================================
# このプログラムは、pl_dbにデータを挿入する
# 責務を分離した設計で実装
# ============================================================

import sqlite3
from sc.parser import xbrl_pl_japan_gaap_parser, xbrl_pl_ifrs_parser
from sc.parser.pl_filename_parser import PlFilenameParser
from sc.parser import xbrl_pl_common_parser
from sc.parser.fiscal_year_calculator import FiscalYearCalculator
import os


class PlDBInserter:

    def __init__(self, pl_file_path):
        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)

        # 企業コードをファイル名から取得
        parser = PlFilenameParser(pl_file_path)
        self.company_code = parser.get_code()

        # データベースパス
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, '../..', 'db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f'データベースディレクトリを作成しました: {db_dir}')
        self.DB = os.path.join(db_dir, 'PL_DB.db')
        print(f'データベースパス: {self.DB}')

    # ============================================================
    # 1️⃣ メタデータ収集の責務
    # ============================================================
    def collect_metadata(self):
        """
        ファイル名とXBRLからメタデータを収集

        Returns:
            dict: {
                'filename': str,
                'code': str,
                'publicday': str,
                'fiscal_year': int,
                'period': str
            }
        """
        plparser = PlFilenameParser(self.pl_file_path)

        # 期間終了日とクォーターを取得
        end_date = plparser.get_period_end_date()
        quarter = xbrl_pl_common_parser.detect_quarter_from_html(self.pl_file_path)

        # 会計年度を算出（FiscalYearCalculatorに委譲）
        fiscal_year = FiscalYearCalculator.calculate(end_date, quarter)

        metadata = {
            'filename': plparser.get_filename(),
            'code': plparser.get_code(),
            'publicday': plparser.get_public_day(),
            'fiscal_year': fiscal_year,
            'period': quarter
        }

        print(f"メタデータ: {metadata}")
        return metadata

    # ============================================================
    # 2️⃣ ファイル形式判定の責務
    # ============================================================
    def detect_file_type(self):
        """
        IFRS or 日本GAAP or その他を判定

        Returns:
            str: 'IFRS', 'GAAP', 'UNKNOWN'
        """
        if 'iffr' in self.file_name.lower() and 'pl' in self.file_name.lower():
            return 'IFRS'
        elif 'jpfr' in self.file_name.lower() and (
                'pl' in self.file_name.lower() or 'pc' in self.file_name.lower()):
            return 'GAAP'
        else:
            return 'UNKNOWN'

    # ============================================================
    # 3️⃣ XBRLデータ抽出の責務
    # ============================================================
    def extract_ifrs_data(self):
        """
        IFRS形式のPLデータを抽出

        Returns:
            dict: IFRSデータ

        Raises:
            Exception: XBRLパース失敗時
        """
        try:
            return {
                'revenue': xbrl_pl_ifrs_parser.get_RevenueIFRS(self.pl_file_path),
                'sga': xbrl_pl_ifrs_parser.get_SellingGeneralAndAdministrativeExpensesIFRS(self.pl_file_path),
                'op': xbrl_pl_ifrs_parser.get_OperatingProfitLossIFRS(self.pl_file_path),
                'profit': xbrl_pl_ifrs_parser.get_ProfitLossIFRS(self.pl_file_path),
                'eps': xbrl_pl_ifrs_parser.get_DilutedEarningsLossPerShareIFRS(self.pl_file_path)
            }
        except Exception as e:
            print(f'IFRSデータ抽出エラー: {e}')
            raise

    def extract_gaap_data(self):
        """
        日本GAAP形式のPLデータを抽出

        Returns:
            dict: 日本GAAPデータ

        Raises:
            Exception: XBRLパース失敗時
        """
        try:
            return {
                'netsales': xbrl_pl_japan_gaap_parser.get_NetSales(self.pl_file_path),
                'sga': xbrl_pl_japan_gaap_parser.get_SellingGeneralAndAdministrativeExpenses(self.pl_file_path),
                'op': xbrl_pl_japan_gaap_parser.get_OperatingIncome(self.pl_file_path),
                'ordinary': xbrl_pl_japan_gaap_parser.get_OrdinaryIncome(self.pl_file_path),
                'netincome': xbrl_pl_japan_gaap_parser.get_NetIncome(self.pl_file_path)
            }
        except Exception as e:
            print(f'日本GAAPデータ抽出エラー: {e}')
            raise

    # ============================================================
    # 4️⃣ SQL実行の責務
    # ============================================================
    def insert_ifrs_record(self, cursor, metadata, data):
        """
        IFRSレコードをDBに挿入

        Args:
            cursor: SQLite cursor
            metadata: メタデータ辞書
            data: IFRSデータ辞書
        """
        cursor.execute('''
            INSERT INTO PL 
            (Code, FileName, PublicDay, Period, FiscalYear,
             RevenueIFRS, SellingGeneralAndAdministrativeExpensesIFRS,
             OperatingProfitLossIFRS, ProfitLossIFRS, DilutedEarningsLossPerShareIFRS)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata['code'],
            metadata['filename'],
            metadata['publicday'],
            metadata['period'],
            metadata['fiscal_year'],
            data['revenue'],
            data['sga'],
            data['op'],
            data['profit'],
            data['eps']
        ))

    def insert_gaap_record(self, cursor, metadata, data):
        """
        日本GAAPレコードをDBに挿入

        Args:
            cursor: SQLite cursor
            metadata: メタデータ辞書
            data: 日本GAAPデータ辞書
        """
        cursor.execute('''
            INSERT INTO PL 
            (Code, FileName, PublicDay, Period, FiscalYear,
             NetSales, SellingGeneralAndAdministrativeExpenses,
             OperatingIncome, OrdinaryIncome, NetIncome)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata['code'],
            metadata['filename'],
            metadata['publicday'],
            metadata['period'],
            metadata['fiscal_year'],
            data['netsales'],
            data['sga'],
            data['op'],
            data['ordinary'],
            data['netincome']
        ))

    # ============================================================
    # 5️⃣ テーブル作成の責務
    # ============================================================
    def ensure_table_exists(self, cursor):
        """
        PLテーブルが存在しなければ作成

        Args:
            cursor: SQLite cursor
        """
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
                created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                EPS REAL
            )
        ''')

    # ============================================================
    # 6️⃣ メインの挿入処理（オーケストレーション）
    # ============================================================
    def insert_to_pl_db(self):
        """
        PLデータをDBに挿入する（オーケストレーション層）
        各責務を持つメソッドを呼び出して処理を組み立てる
        """
        conn = None
        try:
            # 1. メタデータ収集
            metadata = self.collect_metadata()

            # 2. ファイル形式判定
            file_type = self.detect_file_type()

            if file_type == 'UNKNOWN':
                print(f'該当なし: IFRS でも JPGAAP でもないファイル - {metadata["filename"]}')
                return

            # 3. データベース接続
            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()

            # 4. テーブル作成
            self.ensure_table_exists(cursor)

            # 5. データ抽出 & 挿入
            if file_type == 'IFRS':
                print(f'IFRS形式のPLファイルを処理中: {metadata["filename"]}')
                data = self.extract_ifrs_data()
                self.insert_ifrs_record(cursor, metadata, data)

            elif file_type == 'GAAP':
                print(f'日本GAAP形式のPLファイルを処理中: {metadata["filename"]}')
                data = self.extract_gaap_data()
                self.insert_gaap_record(cursor, metadata, data)

            # 6. コミット
            conn.commit()
            print(f'登録成功: {metadata["filename"]}')

        except Exception as e:
            print(f'挿入エラー: {e}')
            import traceback
            traceback.print_exc()
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()


# ============================================================
# テスト実行
# ============================================================
if __name__ == '__main__':
    #test_files = [r'E:\Zip_files\1301\0301000-acpc01-tse-acedjpfr-13010-2016-03-31-01-2016-05-09-ixbrl.htm']
    test_files = [r'E:\Zip_files\4612\0600000-qcpl23-tse-qcediffr-46120-2019-09-30-01-2019-11-14-ixbrl.htm']

    for pl_file_path in test_files:
        if os.path.exists(pl_file_path):
            print(f'\n{"=" * 60}')
            print(f'処理開始: {pl_file_path}')
            print(f'{"=" * 60}')

            inserter = PlDBInserter(pl_file_path)

            # DB挿入実行
            inserter.insert_to_pl_db()

            print(f'\n{"=" * 60}')

        else:
            print(f'ファイルが見つかりません: {pl_file_path}')