import xbrl_bs_ifrs_parser
from bs_filename_parser import BsFilenameParser


def print_bs_ifrs_info(bs_file_path):
    bsfilenameparser = BsFilenameParser(bs_file_path)
    print(f'ファイル名:{bsfilenameparser.get_filename()}')
    print(f'code:{bsfilenameparser.get_code()}')
    print(f'現金同等物:{xbrl_bs_ifrs_parser.get_CashAndCashEquivalent(bs_file_path)}億円')
    print(f'流動資産合計:{xbrl_bs_ifrs_parser.get_CurrentAssets(bs_file_path)}億円')
    print(f'有形固定資産:{xbrl_bs_ifrs_parser.get_PropertyPlantAndEquipment(bs_file_path)}億円')
    print(f'資産合計:{xbrl_bs_ifrs_parser.get_Assets(bs_file_path)}億円')


if __name__ == '__main__':
    bs_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0300000-acbs03-tse-acediffr-36790-2024-03-31-01-2024-05-09-ixbrl.htm'
    print_bs_ifrs_info(bs_file_path)