# pl_db_inserter.py  (BS_DB.db でも PL_DB.db でも共通)

import sqlite3
import os
from datetime import datetime
from lxml import etree
import re
from pl_filename_parser import PlFilenameParser

# IFRS / GAAP パーサーは必要に応じて
# import xbrl_pl_ifrs_parser
# import xbrl_pl_japan_gaap_parser


class PlDBInserter:
    def __init__(self, pl_file_path):
        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)

        # 企業コード取得
        parser = PlFilenameParser(pl_file_path)
        self.company_code = parser.get_code()

        # DBパス
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, '..', 'db')
        os.makedirs(db_dir, exist_ok=True)
        self.DB = os.path.join(db_dir, 'BS_DB.db')  # または 'PL_DB.db'
        print(f'データベースパス: {self.DB}')

    def _escape_ns(self, ns_url):
        return ns_url.replace('http://', 'http/').replace('/', '_')

    def get_fiscal_start_month(self):
        fiscal_end_month_map = {
            '1301': 3, '7203': 3, '9984': 3, '9501': 3, '9432': 9,
        }
        return (fiscal_end_month_map.get(self.company_code, 3) % 12) + 1

    def extract_period_info(self):
        try:
            tree = etree.parse(self.pl_file_path)
            root = tree.getroot()
            namespaces = root.nsmap
            period_end_date = None

            # 1. コンテキストから
            for ctx in root.findall('.//{http://www.xbrl.org/2003/instance}context'):
                ctx_id = ctx.get('id', '')
                if re.search(r'CurrentQuarterInstant|CurrentYTDEnd|Instant', ctx_id, re.I):
                    instant = ctx.find('.//{http://www.xbrl.org/2003/instance}instant')
                    if instant is not None and instant.text and re.match(r'\d{4}-\d{2}-\d{2}', instant.text.strip()):
                        period_end_date = datetime.strptime(instant.text.strip(), '%Y-%m-%d').date()
                        break
                    end_tag = ctx.find('.//{http://www.xbrl.org/2003/instance}endDate')
                    if end_tag is not None and end_tag.text and re.match(r'\d{4}-\d{2}-\d{2}', end_tag.text.strip()):
                        period_end_date = datetime.strptime(end_tag.text.strip(), '%Y-%m-%d').date()
                        break

            # 2. DocumentPeriodEndDate
            if not period_end_date:
                for ns_key, ns_url in namespaces.items():
                    if 'jpcrp' in ns_url.lower():
                        tag_name = f'{{{{{self._escape_ns(ns_url)}}}}}DocumentPeriodEndDate'
                        elem = root.find(f'.//{tag_name}')
                        if elem is not None and elem.text and re.match(r'\d{4}-\d{2}-\d{2}', elem.text.strip()):
                            period_end_date = datetime.strptime(elem.text.strip(), '%Y-%m-%d').date()
                            break

            # 3. ファイル名から
            if not period_end_date:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', self.file_name)
                if m:
                    period_end_date = datetime.strptime(m.group(1), '%Y-%m-%d').date()

            if not period_end_date:
                print(f'警告: 期間終了日が取得できません - {self.file_name}')
                return None, None, None

            # 四半期・年度判定
            start_month = self.get_fiscal_start_month()
            fiscal_year = period_end_date.year
            if period_end_date.month < start_month:
                fiscal_year -= 1
            month_in_fiscal = (period_end_date.month - start_month + 12) % 12 + 1
            period = 'Q1' if month_in_fiscal <= 3 else 'Q2' if month_in_fiscal <= 6 else 'Q3' if month_in_fiscal <= 9 else 'Q4'

            print(f'期間情報: {period_end_date} → {period} / {fiscal_year}年度')
            return period, fiscal_year, period_end_date

        except Exception as e:
            print(f'期間情報抽出エラー: {e}')
            import traceback; traceback.print_exc()
            return None, None, None

    def insert_to_pl_db(self):
        try:
            parser = PlFilenameParser(self.pl_file_path)
            filename = parser.get_filename()
            code = parser.get_code()
            publicday = parser.get_public_day()

            period, fiscal_year, _ = self.extract_period_info()
            if not period or not fiscal_year:
                print(f'スキップ: 期間情報なし - {filename}')
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 重複チェックは一切なし！常にINSERT！
            cursor.execute('''
                INSERT INTO PL (Code, FileName, PublicDay, Period, FiscalYear)
                VALUES (?, ?, ?, ?, ?)
            ''', (code, filename, publicday, period, fiscal_year))

            conn.commit()
            print(f'登録完了: {code} | {filename} | {period} | {fiscal_year}年度')

        except Exception as e:
            print(f'挿入エラー: {e}')
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()


# =============================
# テスト実行
# =============================
if __name__ == '__main__':
    test_file = r'E:\Zip_files\1301\0500000-scbs15-tse-scedjpfr-13010-2024-09-30-01-2024-11-06-ixbrl.htm'

    if os.path.exists(test_file):
        print(f'\n{"="*70}')
        print(f'強制登録テスト開始: {test_file}')
        print(f'{"="*70}')
        inserter = PlDBInserter(test_file)
        inserter.insert_to_pl_db()
    else:
        print("ファイルが見つかりません")