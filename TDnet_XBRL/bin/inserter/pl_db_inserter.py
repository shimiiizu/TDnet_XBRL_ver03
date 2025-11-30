# ============================================================
# このプログラムは、XBRL形式（IXBRL含む）の損益計算書（PL）ファイルを解析し、
# ・企業コード
# ・ファイル名
# ・開示日
# ・四半期（本文の日本語「当第○四半期」を直接解析）
# ・年度（期間開始日から算出）
# ・PLの主要項目（IFRS / 日本基準両対応）
# を抽出してSQLiteデータベースへ登録するツールです。
#
# 四半期は必ず、HTML本文中の「当第○四半期」から取得し、
# 判別できない場合は "Unknown" として登録します。
# ============================================================

import sqlite3
from bin.parser import xbrl_pl_japan_gaap_parser, xbrl_pl_ifrs_parser
from bin.parser.pl_filename_parser import PlFilenameParser
import os
from datetime import datetime
from lxml import etree
import re
from bin.parser import xbrl_pl_common_parser

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
    # 四半期（Q1〜Q4）をxbrl_pl_common_parserから受け取る
    # ============================================================
    def receive_quarter_from_xbrl_pl_common_parser(self):
        return xbrl_pl_common_parser.detect_quarter_from_html(self.pl_file_path)

    # ============================================================
    # 公表日（Public_Day）をpl_filename_parserから受け取る
    # ============================================================
    def receive_public_day_from_pl_filename_parser(self):
        plparser = PlFilenameParser(self.pl_file_path)
        return plparser.get_public_day()

    # ============================================================
    # 会計年度（Fiscal_Year）をpl_filename_parserから受け取る
    # ============================================================
    def receive_fiscal_year_from_pl_filename_parser(self):
        plparser = PlFilenameParser(self.pl_file_path)
        return plparser.get_fiscal_year()


    """
    # ============================================================
    # 期間情報抽出（期間開始日・終了日のみ）
    # ============================================================
    def extract_period_dates(self):
        """
        期間開始日・終了日を XBRL解析せず、ファイル名から直接取得する。
        ルール:
            - 最初の YYYY-MM-DD → 期間開始日
            - 2番目の YYYY-MM-DD → 期間終了日
            - ファイル名に日付が2つ未満なら エラー扱いとし処理を停止する
        """
        try:
            # ファイル名から YYYY-MM-DD をすべて抽出
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', self.file_name)

            # 日付が2つ未満ならエラー扱い
            if len(dates) < 2:
                raise ValueError(
                    f"ファイル名から開始日と終了日を判別できません（日付が2つ未満）: {self.file_name}"
                )

            # 1つ目 → 開始日、2つ目 → 終了日
            period_start_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
            period_end_date = datetime.strptime(dates[1], '%Y-%m-%d').date()

            print(f"[extract_period_dates] 開始日={period_start_date}, 終了日={period_end_date}")
            return period_start_date, period_end_date

        except Exception as e:
            print(f"[extract_period_dates] エラー: {e}")
            raise  # ④の仕様どおり処理中断

    # ============================================================
    # 会計年度を取得
    # ============================================================
    def extract_fiscal_year(self):
        """
        期間終了日から会計年度を取得する。
        """
        try:
            period_start_date, period_end_date = self.extract_period_dates()

            if period_end_date:
                return period_end_date.year
            else:
                return None

        except Exception as e:
            print(f'会計年度取得エラー: {e}')
            import traceback
            traceback.print_exc()
            return None

    # ============================================================
    # 期間情報を統合して取得（後方互換性のため）
    # ============================================================
    def extract_period_info(self):
        """
        期間情報を統合して取得する。

        Returns:
            tuple: (period, fiscal_year, period_end_date)
        """
        try:
            # 期間日付を取得
            period_start_date, period_end_date = self.extract_period_dates()

            if not period_end_date:
                print(f"警告: 期間終了日が取得できませんでした: {self.file_name}")
                return "Unknown", None, None

            # 四半期を取得
            period = self.receive_quarter_from_xbrl_pl_common_parser()

            # 会計年度を取得
            fiscal_year = self.extract_fiscal_year()

            print(f"期間情報: 開始={period_start_date}, 終了={period_end_date}, 四半期={period}, 年度={fiscal_year}")
            return period, fiscal_year, period_end_date

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            import traceback
            traceback.print_exc()
            return "Unknown", None, None
    """
    # ============================================================
    # DB挿入（重複チェックなし・常に追加）
    # ============================================================
    def insert_to_pl_db(self):
        try:
            plparser = PlFilenameParser(self.pl_file_path)
            filename = plparser.get_filename()
            code = plparser.get_code()
            publicday = plparser.get_public_day()
            fiscal_year = self.receive_fiscal_year_from_pl_filename_parser()

            # 期間情報取得
            #period, fiscal_year, _ = self.extract_period_info()

            conn = sqlite3.connect(self.DB)
            cursor = conn.cursor()

            # テーブル作成（created_at を日本時間で記録）
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

            inserted = False

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

                inserted = True

            # --- 日本GAAP ---
            elif 'jpfr' in self.file_name.lower() and (
                    'pl' in self.file_name.lower() or 'pc' in self.file_name.lower()):
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

                inserted = True

            if inserted:
                conn.commit()
                print(f'登録成功: {filename}')
            else:
                print(f'該当なし: IFRS でも JPGAAP でもないファイル - {filename}')

        except Exception as e:
            print(f'挿入エラー: {e}')
            import traceback
            traceback.print_exc()
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()


# ============================================================
# テスト実行
# ============================================================
if __name__ == '__main__':
    test_files = [
        r'E:\Zip_files\1301\0301000-acpc01-tse-acedjpfr-13010-2016-03-31-01-2016-05-09-ixbrl.htm'
    ]

    for pl_file_path in test_files:
        if os.path.exists(pl_file_path):
            print(f'\n{"=" * 60}')
            print(f'処理開始: {pl_file_path}')
            print(f'{"=" * 60}')
            inserter = PlDBInserter(pl_file_path)

            # DB登録
            inserter.insert_to_pl_db()

        else:
            print(f'ファイルが見つかりません: {pl_file_path}')