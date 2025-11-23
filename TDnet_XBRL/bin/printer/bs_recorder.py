"""
xbrl_file_pathを引数として、BSのレコードを作成する（プリントアウトする）

"""

from bin.parser import xbrl_bs_common_parser
from bin.printer import bs_common_printer, bs_japan_gaap_printer, bs_ifrs_printer


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