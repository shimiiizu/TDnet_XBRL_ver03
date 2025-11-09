"""
データベースにBSデータを保管する

"""

import sqlite3
import os
import xbrl_bs_common_parser
import xbrl_bs_japan_gaap_parser
import xbrl_bs_ifrs_parser
from bs_filename_parser import BsFilenameParser


class BsDBInserter:

    def __init__(self, bs_file_path):
        self.bs_file_path = bs_file_path  # 通期のBSファイルのリスト

        # プロジェクトのルートディレクトリからの相対パスでDBを指定
        # 現在のファイルの場所から相対的にDBパスを取得
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # binフォルダの親ディレクトリ
        db_dir = os.path.join(project_root, 'db')

        # dbフォルダが存在しない場合は作成
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"データベースフォルダを作成しました: {db_dir}")

        self.DB = os.path.join(db_dir, 'BS_DB.db')
        print(f"データベースパス: {self.DB}")


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

        conn = sqlite3.connect(self.DB)
        cursor = conn.cursor()
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
                AccountingStandard, PublicDay, StartDay, EndDay, CashAndCashEquivalent, 
                CurrentAssets, PropertyPlantAndEquipment, Assets, RetainedEarnings, Equity)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                               (filename, company_name, code, typeofcurrentperioddei,
                                accountingstandard, public_day, currentfiscalyearstartdatedei, currentperiodenddatedei, cashandcashequivalent_ifrs,
                                current_assets_ifrs, propertyplantandequipment, assets_ifrs, retainedearningsifrs, equityifrs))


            elif accounting_standard == "Japan GAAP":
                cashanddeposits = xbrl_bs_japan_gaap_parser.get_CashAndDeposits(self.bs_file_path)
                propertyplantandequipment = xbrl_bs_japan_gaap_parser.get_PropertyPlantAndEquipment(self.bs_file_path)
                current_assets_japan_gaap = xbrl_bs_japan_gaap_parser.get_CurrentAssets(self.bs_file_path)
                assets_japan_gaap = xbrl_bs_japan_gaap_parser.get_Assets(self.bs_file_path)
                retainedearnings = xbrl_bs_japan_gaap_parser.get_RetainedEarnings(self.bs_file_path)
                netassets = xbrl_bs_japan_gaap_parser.get_NetAssets(self.bs_file_path)
                cursor.execute('''INSERT INTO BS 
                            (FileName, CompanyName, Code, FinancialReportType, 
                            AccountingStandard, PublicDay, StartDay, EndDay, CashAndDeposits, 
                            CurrentAssets, PropertyPlantAndEquipment, Assets, RetainedEarnings, NetAssets)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                               (filename, company_name, code,typeofcurrentperioddei,
                                accountingstandard, public_day, currentfiscalyearstartdatedei, currentperiodenddatedei, cashanddeposits,
                                current_assets_japan_gaap, propertyplantandequipment, assets_japan_gaap, retainedearnings,netassets))

            print(f'{filename}を登録しました。')

        else:
            print(f'すでに{filename}は登録されています。')

        conn.commit()
        conn.close()


if __name__ == '__main__':
    bs_file_path =  r'C:\Users\Shimizu\PycharmProjects\TDnet_XBRL\TDnet_XBRL\zip_files\2780\0101010-acbs01-tse-acedjpfr-27800-2014-03-31-02-2014-10-10-ixbrl.htm'
    bsdbinserter = BsDBInserter(bs_file_path)
    bsdbinserter.insert_to_bs_db()