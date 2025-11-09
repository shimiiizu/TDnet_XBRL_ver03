"""
BSの基本情報をプリンアウトする。

"""

import xbrl_bs_common_parser


def print_bs_common_info(bs_file_path):
    print(f'')
    print(f'-----{xbrl_bs_common_parser.get_company_name(bs_file_path)}-----')
    print(f'決算開始日:{xbrl_bs_common_parser.get_CurrentFiscalYearStartDateDEI(bs_file_path)}')
    print(f'決算終了日:{xbrl_bs_common_parser.get_CurrentPeriodEndDateDEI(bs_file_path)}')
    print(f'決算報告タイプ:{xbrl_bs_common_parser.get_TypeOfCurrentPeriodDEI(bs_file_path)}')
    print(f'会計方式:{xbrl_bs_common_parser.get_AccountingStandard(bs_file_path)}')


if __name__ == '__main__':
    bs_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\2780\0101010-acbs01-tse-acedjpfr-27800-2014-03-31-02-2014-10-10-ixbrl.htm'
    print_bs_common_info(bs_file_path)