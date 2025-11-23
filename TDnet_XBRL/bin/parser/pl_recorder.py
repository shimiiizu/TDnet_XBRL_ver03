"""
xbrl_file_pathを引数として、PLのレコードを作成する（プリントアウトする）

"""
import xbrl_pl_common_parser
import pl_ifrs_printer  # 自作モジュール：BS（IFRS）情報をプリントアウトする
import pl_japan_gaap_printer  # 自作モジュール：BS（Japan_Gaap）情報をプリントアウトする
import os

class PlRecoder:

    def __init__(self, pl_file_path):
        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)

    def record_pl(self):
        first_string = 'iffr'
        second_string ='pl'
        if first_string in self.file_name and second_string in self.file_name:
                pl_ifrs_printer.print_pl_ifrs_info(self.pl_file_path)

        first_string = 'jpfr'
        second_string = 'pl'
        if first_string in self.file_name and second_string in self.file_name:
                pl_japan_gaap_printer.print_pl_japan_gaap_info(self.pl_file_path)


if __name__ == '__main__':
    pl_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0600000-qcpl11-tse-qcedjpfr-36790-2014-06-30-01-2014-08-12-ixbrl.htm'
    plrecorder = PlRecoder(pl_file_path)
    plrecorder.record_pl()


