# ============================================================
# このプログラムは、XBRL形式（IXBRL含む）の損益計算書（PL）ファイルを解析し、
# ・企業コード
# ・ファイル名
# ・開示日
# ・四半期（本文の日本語「当第○四半期」を直接解析）
# ・年度（期間終了日の年）
# ・PLの主要項目（IFRS / 日本基準両対応）
# を抽出してSQLiteデータベースへ登録するツールです。
#
# 四半期は必ず、HTML本文中の「当第○四半期」から取得し、
# 判別できない場合は "Unknown" として登録します。
# 企業コードからの会計年度推定は行いません。
# ============================================================

import sqlite3
from bin.parser import xbrl_pl_japan_gaap_parser, xbrl_pl_ifrs_parser
from bin.parser.pl_filename_parser import PlFilenameParser
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
        db_dir = os.path.join(current_dir, '../..', 'db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f'データベースディレクトリを作成しました: {db_dir}')
        self.DB = os.path.join(db_dir, 'PL_DB.db')
        print(f'データベースパス: {self.DB}')

    # ============================================================
    # HTML本文から四半期（Q1〜Q4）を抽出
    # ============================================================
    def detect_quarter_from_html(self):
        """
        IXBRL（HTML）本文から四半期情報を抽出して返す。
        優先順位：
        1. 「当第○四半期」→ Q1〜Q4
        2. 「当中間」→ Q2
        3. 「当連結」または「当単独」→ Q4
        4. 見つからない → Unknown
        """
        try:
            with open(self.pl_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_text = f.read()

            # 優先順位1: 「当第○四半期」を検出
            m = re.search(r'当第\s*([０-９0-9])\s*四半期', html_text)
            if m:
                q_str = m.group(1)
                # 全角数字を半角に変換
                q_str = q_str.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
                q = int(q_str)
                if 1 <= q <= 4:
                    return f"Q{q}"

            # 優先順位2: 「当中間」を検出 → Q2
            if re.search(r'当\s*中間', html_text):
                return "Q2"

            # 優先順位3: 「当連結」または「当単独」を検出 → Q4
            if re.search(r'当\s*連結', html_text) or re.search(r'当\s*単独', html_text):
                return "Q4"

        except Exception as e:
            print(f"四半期判定エラー: {e}")

        return "Unknown"
    # ============================================================
    # 期間情報抽出（期間終了日と本文四半期）
    # ============================================================
    def extract_period_info(self):
        try:
            tree = etree.parse(self.pl_file_path)
            root = tree.getroot()

            period_end_date = None

            # instant / endDate の取得
            for ctx in root.findall('.//{http://www.xbrl.org/2003/instance}context'):
                instant = ctx.find('.//{http://www.xbrl.org/2003/instance}instant')
                if instant is not None and instant.text:
                    try:
                        period_end_date = datetime.strptime(instant.text.strip(), '%Y-%m-%d').date()
                        break
                    except:
                        pass

                end_tag = ctx.find('.//{http://www.xbrl.org/2003/instance}endDate')
                if end_tag is not None and end_tag.text:
                    try:
                        period_end_date = datetime.strptime(end_tag.text.strip(), '%Y-%m-%d').date()
                        break
                    except:
                        pass

            # ファイル名 fallback
            if period_end_date is None:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', self.file_name)
                if m:
                    period_end_date = datetime.strptime(m.group(1), '%Y-%m-%d').date()

            if not period_end_date:
                print(f"警告: 期間終了日が取得できませんでした: {self.file_name}")
                return "Unknown", None, None

            # 🔥 HTML本文から四半期を最優先で取得
            period = self.detect_quarter_from_html()

            # 🔥 年度は単純に終了日の年を採用
            fiscal_year = period_end_date.year

            print(f"期間情報: 終了日={period_end_date}, 四半期={period}, 年度={fiscal_year}")
            return period, fiscal_year, period_end_date

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            return "Unknown", None, None

    # ============================================================
    # DB挿入（重複チェックなし・常に追加）
    # ============================================================
    def insert_to_pl_db(self):
        try:
            plparser = PlFilenameParser(self.pl_file_path)
            filename = plparser.get_filename()
            code = plparser.get_code()
            publicday = plparser.get_public_day()

            # 期間情報取得
            period, fiscal_year, _ = self.extract_period_info()

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

            # ============ ここにデバッグ出力を追加 ============
            print(f"\n=== デバッグ情報 ===")
            print(f"ファイル名: {self.file_name}")
            print(f"小文字変換: {self.file_name.lower()}")
            print(f"'iffr' 含む: {'iffr' in self.file_name.lower()}")
            print(f"'jpfr' 含む: {'jpfr' in self.file_name.lower()}")
            print(f"'pl' 含む: {'pl' in self.file_name.lower()}")
            print(f"'pc' 含む: {'pc' in self.file_name.lower()}")
            print(f"====================\n")
            # ============ ここまで ============


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
            print(f'\n{"="*60}')
            print(f'処理開始: {pl_file_path}')
            print(f'{"="*60}')
            inserter = PlDBInserter(pl_file_path)
            inserter.insert_to_pl_db()
        else:
            print(f'ファイルが見つかりません: {pl_file_path}')