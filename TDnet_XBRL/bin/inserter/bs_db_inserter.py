"""
データベースにBSデータを保管する
Period と FiscalYear を追加

"""

import sqlite3
import os
from bin.parser import xbrl_bs_common_parser, xbrl_bs_ifrs_parser, xbrl_bs_japan_gaap_parser
from bin.parser.bs_filename_parser import BsFilenameParser
from datetime import datetime
from lxml import etree
import re


class BsDBInserter:

    def __init__(self, bs_file_path):
        self.bs_file_path = bs_file_path
        self.file_name = os.path.basename(bs_file_path)

        # 企業コードをファイル名から取得
        parser = BsFilenameParser(bs_file_path)
        self.company_code = parser.get_code()

        # プロジェクトのルートディレクトリからの相対パスでDBを指定
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        db_dir = os.path.join(project_root, 'db')

        # dbフォルダが存在しない場合は作成
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"データベースフォルダを作成しました: {db_dir}")

        self.DB = os.path.join(db_dir, 'BS_DB.db')
        print(f"データベースパス: {self.DB}")

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
    # 期間情報抽出（PLと同じロジック）
    # =============================
    def extract_period_info(self):
        try:
            tree = etree.parse(self.bs_file_path)
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
                        tag_name = f'{{{self._escape_ns(ns_url)}}}DocumentPeriodEndDate'
                        elem = root.find(f'.//{tag_name}')
                        if elem is not None and elem.text and re.match(r'\d{4}-\d{2}-\d{2}', elem.text.strip()):
                            period_end_date = datetime.strptime(elem.text.strip(), '%Y-%m-%d').date()
                            break

            # 3. ファイル名から
            if period_end_date is None:
                m = re.search(r'(\d{4}-\d{2}-\d{2})', self.file_name)
                if m:
                    period_end_date = datetime.strptime(m.group(1), '%Y-%m-%d').date()

            # 4. CurrentPeriodEndDateDEI から取得（BS特有）
            if period_end_date is None:
                try:
                    end_day_str = xbrl_bs_common_parser.get_CurrentPeriodEndDateDEI(self.bs_file_path)
                    if end_day_str and re.match(r'\d{4}-\d{2}-\d{2}', end_day_str):
                        period_end_date = datetime.strptime(end_day_str, '%Y-%m-%d').date()
                except:
                    pass

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

    def insert_to_bs_db(self):
        accounting_standard = xbrl_bs_common_parser.get_AccountingStandard(self.bs_file_path)
        company_name = xbrl_bs_common_parser.get_company_name(self.bs_file_path)
        bsfilenameparser = BsFilenameParser(self.bs_file_path)
        code = bsfilenameparser.get_code()
        public_day = bsfilenameparser.get_public_day()
        filename = bsfilenameparser.get_filename()
        currentfiscalyearstartdatedei = xbrl_bs_common_parser.get_CurrentFiscalYearStartDateDEI(self.bs_file_path)
        currentperiodenddatedei = xbrl_bs_common_parser.get_CurrentPeriodEndDateDEI(self.bs_file_path)
        typeofcurrentperioddei = xbrl_bs_common_parser.get_TypeOfCurrentPeriodDEI(self.bs_file_path)
        accountingstandard = xbrl_bs_common_parser.get_AccountingStandard(self.bs_file_path)

        # 期間情報取得
        period, fiscal_year, _ = self.extract_period_info()
        if period is None or fiscal_year is None:
            print(f'警告: 期間情報が取得できませんでした。デフォルト値を使用します - {filename}')
            # デフォルト値として、EndDayから推定
            if currentperiodenddatedei:
                try:
                    end_date = datetime.strptime(currentperiodenddatedei, '%Y-%m-%d').date()
                    fiscal_start_month = self.get_fiscal_start_month()
                    fiscal_year = end_date.year
                    if end_date.month < fiscal_start_month:
                        fiscal_year -= 1
                    month_in_fiscal = (end_date.month - fiscal_start_month + 12) % 12 + 1
                    period = 'Q1' if month_in_fiscal <= 3 else 'Q2' if month_in_fiscal <= 6 else 'Q3' if month_in_fiscal <= 9 else 'Q4'
                except:
                    period = 'Q4'
                    fiscal_year = 2020

        conn = sqlite3.connect(self.DB)
        cursor = conn.cursor()

        # テーブル作成時にPeriodとFiscalYearカラムを追加
        cursor.execute('''CREATE TABLE IF NOT EXISTS BS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            FileName TEXT,
            CompanyName TEXT,
            Code TEXT,
            FinancialReportType TEXT,
            AccountingStandard TEXT,
            PublicDay TEXT,
            StartDay TEXT,
            EndDay TEXT,
            Period TEXT,
            FiscalYear INTEGER,
            CashAndDeposits REAL,
            CashAndCashEquivalent REAL,
            CurrentAssets REAL,
            PropertyPlantAndEquipment REAL,
            Assets REAL,
            RetainedEarnings REAL,
            NetAssets REAL,
            Equity REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        cursor.execute('SELECT COUNT(*) FROM BS WHERE FileName = ?', (filename,))
        if cursor.fetchone()[0] == 0:

            if accounting_standard == "IFRS":
                current_assets_ifrs = xbrl_bs_ifrs_parser.get_CurrentAssets(self.bs_file_path)
                assets_ifrs = xbrl_bs_ifrs_parser.get_Assets(self.bs_file_path)
                cashandcashequivalent_ifrs = xbrl_bs_ifrs_parser.get_CashAndCashEquivalent(self.bs_file_path)
                propertyplantandequipment = xbrl_bs_ifrs_parser.get_PropertyPlantAndEquipment(self.bs_file_path)
                retainedearningsifrs = xbrl_bs_ifrs_parser.get_RetainedEarningsIFRS(self.bs_file_path)
                equityifrs = xbrl_bs_ifrs_parser.get_EquityIFRS(self.bs_file_path)

                cursor.execute('''INSERT INTO BS 
                (FileName, CompanyName, Code, FinancialReportType, 
                AccountingStandard, PublicDay, StartDay, EndDay, Period, FiscalYear,
                CashAndCashEquivalent, CurrentAssets, PropertyPlantAndEquipment, 
                Assets, RetainedEarnings, Equity)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                               (filename, company_name, code, typeofcurrentperioddei,
                                accountingstandard, public_day, currentfiscalyearstartdatedei,
                                currentperiodenddatedei, period, fiscal_year,
                                cashandcashequivalent_ifrs, current_assets_ifrs,
                                propertyplantandequipment, assets_ifrs, retainedearningsifrs, equityifrs))

                print(f'IFRS BSデータを登録: {code} | {period} | {fiscal_year}年度')

            elif accounting_standard == "Japan GAAP":
                cashanddeposits = xbrl_bs_japan_gaap_parser.get_CashAndDeposits(self.bs_file_path)
                propertyplantandequipment = xbrl_bs_japan_gaap_parser.get_PropertyPlantAndEquipment(self.bs_file_path)
                current_assets_japan_gaap = xbrl_bs_japan_gaap_parser.get_CurrentAssets(self.bs_file_path)
                assets_japan_gaap = xbrl_bs_japan_gaap_parser.get_Assets(self.bs_file_path)
                retainedearnings = xbrl_bs_japan_gaap_parser.get_RetainedEarnings(self.bs_file_path)
                netassets = xbrl_bs_japan_gaap_parser.get_NetAssets(self.bs_file_path)

                cursor.execute('''INSERT INTO BS 
                (FileName, CompanyName, Code, FinancialReportType, 
                AccountingStandard, PublicDay, StartDay, EndDay, Period, FiscalYear,
                CashAndDeposits, CurrentAssets, PropertyPlantAndEquipment, 
                Assets, RetainedEarnings, NetAssets)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                               (filename, company_name, code, typeofcurrentperioddei,
                                accountingstandard, public_day, currentfiscalyearstartdatedei,
                                currentperiodenddatedei, period, fiscal_year,
                                cashanddeposits, current_assets_japan_gaap,
                                propertyplantandequipment, assets_japan_gaap,
                                retainedearnings, netassets))

                print(f'日本GAAP BSデータを登録: {code} | {period} | {fiscal_year}年度')

            print(f'{filename}を登録しました。')

        else:
            print(f'すでに{filename}は登録されています。')

        conn.commit()
        conn.close()


if __name__ == '__main__':
    bs_file_path = r'C:\Users\Shimizu\PycharmProjects\TDnet_XBRL\TDnet_XBRL\zip_files\2780\0101010-acbs01-tse-acedjpfr-27800-2014-03-31-02-2014-10-10-ixbrl.htm'
    bsdbinserter = BsDBInserter(bs_file_path)
    bsdbinserter.insert_to_bs_db()