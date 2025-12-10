# ============================================================
# このプログラムは、pl_dbにデータを挿入する
# 責務を分離した設計で実装
# ログ強化版（2025-12-07）
# ============================================================

import sqlite3
from sc.parser import xbrl_pl_japan_gaap_parser, xbrl_pl_ifrs_parser
from sc.parser.pl_filename_parser import PlFilenameParser
from sc.parser import xbrl_pl_common_parser
from sc.parser.fiscal_year_calculator import FiscalYearCalculator
import os


class PlDBInserter:

    def __init__(self, pl_file_path):
        print(f"[CALL] __init__(pl_file_path={pl_file_path})")

        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)

        parser = PlFilenameParser(pl_file_path)
        self.company_code = parser.get_code()
        print(f"[INFO] 企業コード取得: {self.company_code}")

        # DBパス設定
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, '../..', 'db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"[INFO] DBディレクトリ作成: {db_dir}")

        self.DB = os.path.join(db_dir, 'PL_DB.db')
        print(f"[INFO] データベースパス: {self.DB}")

    # ============================================================
    # 1. メタデータ収集
    # ============================================================
    def collect_metadata(self):
        print("[CALL] collect_metadata()")

        plparser = PlFilenameParser(self.pl_file_path)

        end_date = plparser.get_period_end_date()
        print(f"[INFO] 終了日取得: {end_date}")

        quarter = xbrl_pl_common_parser.detect_quarter_from_html(self.pl_file_path)
        print(f"[INFO] 四半期判定: {quarter}")

        fiscal_year = FiscalYearCalculator.calculate(end_date, quarter)
        print(f"[INFO] 会計年度算出: {fiscal_year}")

        metadata = {
            'filename': plparser.get_filename(),
            'code': plparser.get_code(),
            'publicday': plparser.get_public_day(),
            'fiscal_year': fiscal_year,
            'period': quarter
        }

        print(f"[RETURN] collect_metadata -> {metadata}")
        return metadata

    # ============================================================
    # 2. ファイル形式判定
    # ============================================================
    def detect_file_type(self):
        print("[CALL] detect_file_type()")
        lower = self.file_name.lower()

        if 'iffr' in lower and 'pl' in lower:
            print("[RETURN] detect_file_type -> IFRS")
            return 'IFRS'

        if 'jpfr' in lower and ('pl' in lower or 'pc' in lower):
            print("[RETURN] detect_file_type -> GAAP")
            return 'GAAP'

        print("[RETURN] detect_file_type -> UNKNOWN")
        return 'UNKNOWN'

    # ============================================================
    # 3. IFRSデータ抽出
    # ============================================================
    def extract_ifrs_data(self):
        print("[CALL] extract_ifrs_data()")

        try:
            data = {
                'revenue': xbrl_pl_ifrs_parser.get_RevenueIFRS(self.pl_file_path),
                'sga': xbrl_pl_ifrs_parser.get_SellingGeneralAndAdministrativeExpensesIFRS(self.pl_file_path),
                'op': xbrl_pl_ifrs_parser.get_OperatingProfitLossIFRS(self.pl_file_path),
                'profit': xbrl_pl_ifrs_parser.get_ProfitLossIFRS(self.pl_file_path),
                'eps': xbrl_pl_ifrs_parser.get_DilutedEarningsLossPerShareIFRS(self.pl_file_path)
            }
            print(f"[RETURN] extract_ifrs_data -> {data}")
            return data

        except Exception as e:
            print(f"[ERROR] IFRSデータ抽出失敗: {e}")
            raise

    # ============================================================
    # 4. GAAPデータ抽出
    # ============================================================
    def extract_gaap_data(self):
        print("[CALL] extract_gaap_data()")

        try:
            data = {
                'netsales': xbrl_pl_japan_gaap_parser.get_NetSales(self.pl_file_path),
                'sga': xbrl_pl_japan_gaap_parser.get_SellingGeneralAndAdministrativeExpenses(self.pl_file_path),
                'op': xbrl_pl_japan_gaap_parser.get_OperatingIncome(self.pl_file_path),
                'ordinary': xbrl_pl_japan_gaap_parser.get_OrdinaryIncome(self.pl_file_path),
                'netincome': xbrl_pl_japan_gaap_parser.get_NetIncome(self.pl_file_path)
            }
            print(f"[RETURN] extract_gaap_data -> {data}")
            return data

        except Exception as e:
            print(f"[ERROR] 日本GAAPデータ抽出失敗: {e}")
            raise

    # ============================================================
    # 5. IFRSレコードの挿入（← 復元 & ログ追加）
    # ============================================================
    def insert_ifrs_record(self, cursor, metadata, data):
        print("[CALL] insert_ifrs_record()")
        print(f"[INFO] metadata={metadata}")
        print(f"[INFO] data={data}")

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

        print("[RETURN] insert_ifrs_record -> OK")

    # ============================================================
    # 6. GAAPレコードの挿入（← 復元 & ログ追加）
    # ============================================================
    def insert_gaap_record(self, cursor, metadata, data):
        print("[CALL] insert_gaap_record()")
        print(f"[INFO] metadata={metadata}")
        print(f"[INFO] data={data}")

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

        print("[RETURN] insert_gaap_record -> OK")

    # ============================================================
    # 7. テーブル作成
    # ============================================================
    def ensure_table_exists(self, cursor):
        print("[CALL] ensure_table_exists()")

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

        print("[INFO] PLテーブル存在確認・作成完了")

    # ============================================================
    # 8. メイン処理（オーケストレーション）
    # ============================================================
    def insert_to_pl_db(self):
        print("[CALL] insert_to_pl_db()")

        conn = None
        try:
            metadata = self.collect_metadata()
            file_type = self.detect_file_type()
            print(f"[INFO] ファイル形式: {file_type}")

            if file_type == 'UNKNOWN':
                print(f"[BRANCH] UNKNOWN形式 → スキップ: {metadata['filename']}")
                return

            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()
            print("[INFO] DB接続成功")

            self.ensure_table_exists(cursor)

            if file_type == 'IFRS':
                print("[BRANCH] IFRSデータ抽出処理")
                data = self.extract_ifrs_data()
                self.insert_ifrs_record(cursor, metadata, data)

            elif file_type == 'GAAP':
                print("[BRANCH] GAAPデータ抽出処理")
                data = self.extract_gaap_data()
                self.insert_gaap_record(cursor, metadata, data)

            conn.commit()
            print("[INFO] コミット完了")
            print("[RETURN] insert_to_pl_db -> 成功")

        except Exception as e:
            print(f"[ERROR] insert_to_pl_db 中に例外: {e}")
            import traceback
            traceback.print_exc()

            if conn:
                conn.rollback()
                print("[INFO] ロールバック実行")

        finally:
            if conn:
                conn.close()
                print("[INFO] DB接続クローズ")


# ============================================================
# テスト実行
# ============================================================
if __name__ == '__main__':
    test_files = [
        r'E:\Zip_files\4612\0600000-qcpl23-tse-qcediffr-46120-2019-09-30-01-2019-11-14-ixbrl.htm'
    ]

    for pl_file_path in test_files:
        print("\n============================================================")
        print(f"処理開始: {pl_file_path}")
        print("============================================================")

        inserter = PlDBInserter(pl_file_path)
        inserter.insert_to_pl_db()

        print("============================================================\n")
