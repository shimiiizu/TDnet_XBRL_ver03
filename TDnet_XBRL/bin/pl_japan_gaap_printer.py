import xbrl_pl_japan_gaap_parser
import os
from pl_filename_parser import PlFilenameParser


def print_pl_japan_gaap_info(pl_file_path):
    plfilenameparser = PlFilenameParser(pl_file_path)

    print('')
    print(f'ファイル名：{os.path.basename(pl_file_path)}')
    print(f'code:{plfilenameparser.get_code()}')
    print(f'売上:{xbrl_pl_japan_gaap_parser.get_NetSales(pl_file_path)}億円')
    print(f'販売費及び一般管理費:{xbrl_pl_japan_gaap_parser.get_SellingGeneralAndAdministrativeExpenses(pl_file_path)}億円')
    print(f'営業利益:{xbrl_pl_japan_gaap_parser.get_OperatingIncome(pl_file_path)}億円')
    print(f'純利益:{xbrl_pl_japan_gaap_parser.get_NetIncome(pl_file_path)}億円')


if __name__ == '__main__':
    pl_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0301000-acpl01-tse-acedjpfr-36790-2015-03-31-01-2015-05-15-ixbrl.htm'
    print_pl_japan_gaap_info(pl_file_path)
