import xbrl_pl_ifrs_parser
import os
from pl_filename_parser import PlFilenameParser



def print_pl_ifrs_info(pl_file_path):
    plfilenameparser = PlFilenameParser(pl_file_path)

    print('')
    print(f'ファイル名:{os.path.basename(pl_file_path)}')
    print(f'code:{plfilenameparser.get_code()}')
    print(f'売上:{xbrl_pl_ifrs_parser.get_RevenueIFRS(pl_file_path)}億円')
    print(f'販売費及び一般管理費:{xbrl_pl_ifrs_parser.get_SellingGeneralAndAdministrativeExpensesIFRS(pl_file_path)}億円')
    print(f'営業利益:{xbrl_pl_ifrs_parser.get_OperatingProfitLossIFRS(pl_file_path)}億円')
    print(f'四半期利益:{xbrl_pl_ifrs_parser.get_ProfitLossIFRS(pl_file_path)}億円')
    print(f'一株当たり四半期利益:{xbrl_pl_ifrs_parser.get_DilutedEarningsLossPerShareIFRS(pl_file_path)}億円')


if __name__ == '__main__':
    pl_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0301000-acpl03-tse-acediffr-36790-2024-03-31-01-2024-05-09-ixbrl.htm'
    print_pl_ifrs_info(pl_file_path)
