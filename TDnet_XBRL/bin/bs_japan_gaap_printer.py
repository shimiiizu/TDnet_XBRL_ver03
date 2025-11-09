import xbrl_bs_japan_gaap_parser
from bs_filename_parser import BsFilenameParser

def print_bs_japan_gaap_info(bs_file_path):
    bsfilenameparser = BsFilenameParser(bs_file_path)
    print(f'ファイル名:{bsfilenameparser.get_filename()}')
    print(f'code:{bsfilenameparser.get_code()}')
    print(f'現金及び預金:{xbrl_bs_japan_gaap_parser.get_CashAndDeposits(bs_file_path)}億円')
    print(f'流動資産合計:{xbrl_bs_japan_gaap_parser.get_CurrentAssets(bs_file_path)}億円')
    print(f'有形固定資産:{xbrl_bs_japan_gaap_parser.get_PropertyPlantAndEquipment(bs_file_path)}億円')
    print(f'資産合計:{xbrl_bs_japan_gaap_parser.get_Assets(bs_file_path)}億円')


if __name__ == '__main__':
    bs_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\2780\0101010-acbs01-tse-acedjpfr-27800-2014-03-31-02-2014-10-10-ixbrl.htm'
    #bs_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3449\0101010-qcbs01-tse-qcedjpfr-34490-2020-03-31-01-2020-05-08-ixbrl.htm'
    print_bs_japan_gaap_info(bs_file_path)