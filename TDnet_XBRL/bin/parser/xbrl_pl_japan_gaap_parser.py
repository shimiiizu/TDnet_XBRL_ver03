import os
import sys
from bs4 import BeautifulSoup

# 共通関数をインポート
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(current_dir, '..', 'utils')
sys.path.insert(0, utils_dir)
from xbrl_utils import find_tag_with_flexible_context, extract_value_from_tag


# 現金及び預金(億円)を取得する関数
def get_CashAndDeposits(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:CashAndDeposits", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "CashAndDeposits")

    except Exception as e:
        print(f"エラー: CashAndDeposits の取得失敗 - {xbrl_path}: {e}")
        return None


# 流動資産合計(億円)を取得する関数
def get_CurrentAssets(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:CurrentAssets", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "CurrentAssets")

    except Exception as e:
        print(f"エラー: CurrentAssets の取得失敗 - {xbrl_path}: {e}")
        return None


# 有形固定資産合計(億円)を取得する関数
def get_PropertyPlantAndEquipment(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:PropertyPlantAndEquipment", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "PropertyPlantAndEquipment")

    except Exception as e:
        print(f"エラー: PropertyPlantAndEquipment の取得失敗 - {xbrl_path}: {e}")
        return None


# 資産合計(億円)を取得する関数
def get_Assets(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:Assets", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "Assets")

    except Exception as e:
        print(f"エラー: Assets の取得失敗 - {xbrl_path}: {e}")
        return None


# 利益剰余金(億円)を取得する関数
def get_RetainedEarnings(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:RetainedEarnings", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "RetainedEarnings")

    except Exception as e:
        print(f"エラー: RetainedEarnings の取得失敗 - {xbrl_path}: {e}")
        return None


# 純資産合計(億円)を取得する関数
def get_NetAssets(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jppfs_cor:NetAssets", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "NetAssets")

    except Exception as e:
        print(f"エラー: NetAssets の取得失敗 - {xbrl_path}: {e}")
        return None


if __name__ == '__main__':
    xbrl_path = r"C:\Users\Shimizu\PycharmProjects\TDnet_XBRL\TDnet_XBRL\zip_files\6196\0500000-anbs02-tse-anedjpfr-61960-2016-08-31-01-2016-09-29-ixbrl.htm"
    print(f"現金及び預金: {get_CashAndDeposits(xbrl_path)}億円")
    print(f"流動資産: {get_CurrentAssets(xbrl_path)}億円")
    print(f"有形固定資産: {get_PropertyPlantAndEquipment(xbrl_path)}億円")
    print(f"資産合計: {get_Assets(xbrl_path)}億円")
    print(f"利益剰余金: {get_RetainedEarnings(xbrl_path)}億円")
    print(f"純資産: {get_NetAssets(xbrl_path)}億円")