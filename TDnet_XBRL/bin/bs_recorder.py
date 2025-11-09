"""
xbrl_file_pathを引数として、BSのレコードを作成する（プリントアウトする）

"""

import xbrl_bs_common_parser  # 自作モジュール： XBRLの基本情報を抽出する
import bs_common_printer  # 自作モジュール：BSの基本情報をプリントアウトする
import bs_ifrs_printer  # 自作モジュール：BS（IFRS）情報をプリントアウトする
import bs_japan_gaap_printer  # 自作モジュール：BS（Japan_Gaap）情報をプリントアウトする

class BsRecoder:

    def __init__(self, bs_file_path):
        self.bs_file_path = bs_file_path

    def record_bs(self):
        accounting_standard = xbrl_bs_common_parser.get_AccountingStandard(self.bs_file_path)

        if accounting_standard == "IFRS":
            bs_common_printer.print_bs_common_info(self.bs_file_path)
            bs_ifrs_printer.print_bs_ifrs_info(self.bs_file_path)

        elif accounting_standard == "Japan GAAP":
            bs_common_printer.print_bs_common_info(self.bs_file_path)
            bs_japan_gaap_printer.print_bs_japan_gaap_info(self.bs_file_path)

        else:
            print('IFRSでもJapan GAAPでもありません。')