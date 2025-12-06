import os
import sys
from bs4 import BeautifulSoup

# 共通関数をインポート
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(current_dir, '..', 'utils')
sys.path.insert(0, utils_dir)
from sc.utils.xbrl_utils import find_tag_with_flexible_context, extract_value_from_tag


# 売上(億円)を取得する関数
def get_NetSales(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:NetSales", context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "NetSales")

    except Exception as e:
        print(f'エラー: NetSales取得失敗 - {xbrl_path}: {e}')
        return None


# 販売費及び一般管理費(億円)を取得する関数
def get_SellingGeneralAndAdministrativeExpenses(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:SellingGeneralAndAdministrativeExpenses",
                                             context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "SellingGeneralAndAdministrativeExpenses")

    except Exception as e:
        print(f'エラー: SellingGeneralAndAdministrativeExpenses取得失敗 - {xbrl_path}: {e}')
        return None


# 営業利益(億円)を取得する関数
def get_OperatingIncome(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:OperatingIncome", context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "OperatingIncome")

    except Exception as e:
        print(f'エラー: OperatingIncome取得失敗 - {xbrl_path}: {e}')
        return None


# 経常利益(億円)を取得する関数
def get_OrdinaryIncome(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:OrdinaryIncome", context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "OrdinaryIncome")

    except Exception as e:
        print(f'エラー: OrdinaryIncome取得失敗 - {xbrl_path}: {e}')
        return None


# 純利益(億円)を取得する関数
def get_NetIncome(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        # NetIncomeを探す
        tag = find_tag_with_flexible_context(soup, "jppfs_cor:NetIncome", context_type='duration')

        # NetIncomeが見つからない場合はProfitLossを試す
        if tag is None:
            tag = find_tag_with_flexible_context(soup, "jppfs_cor:ProfitLoss", context_type='duration')

        return extract_value_from_tag(tag, xbrl_path, "NetIncome/ProfitLoss")

    except Exception as e:
        print(f'エラー: NetIncome取得失敗 - {xbrl_path}: {e}')
        return None


if __name__ == '__main__':
    # テスト用
    xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\7172\0102010-acpl01-tse-acedjpfr-71720-2014-12-31-01-2015-02-12-ixbrl.htm"

    print(f'売上: {get_NetSales(xbrl_path)}')
    print(f'販管費: {get_SellingGeneralAndAdministrativeExpenses(xbrl_path)}')
    print(f'営業利益: {get_OperatingIncome(xbrl_path)}')
    print(f'経常利益: {get_OrdinaryIncome(xbrl_path)}')
    print(f'純利益: {get_NetIncome(xbrl_path)}')