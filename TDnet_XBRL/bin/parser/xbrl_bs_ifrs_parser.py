from bs4 import BeautifulSoup
import os
import sys

# 共通関数をインポート
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(current_dir, '..', 'utils')
sys.path.insert(0, utils_dir)
from bin.utils.xbrl_utils import find_tag_with_flexible_context, extract_value_from_tag


# 現金同等額(億円)を取得する関数
def get_CashAndCashEquivalent(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:CashAndCashEquivalentsIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "CashAndCashEquivalent")

    except Exception as e:
        print(f"エラー: CashAndCashEquivalent の取得失敗 - {xbrl_path}: {e}")
        return None


# 流動資産合計を取得する関数
def get_CurrentAssets(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:CurrentAssetsIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "CurrentAssets")

    except Exception as e:
        print(f"エラー: CurrentAssets の取得失敗 - {xbrl_path}: {e}")
        return None


# 有形固定資産を取得する関数
def get_PropertyPlantAndEquipment(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:PropertyPlantAndEquipmentIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "PropertyPlantAndEquipment")

    except Exception as e:
        print(f"エラー: PropertyPlantAndEquipment の取得失敗 - {xbrl_path}: {e}")
        return None


# 非流動資産合計を取得する関数
def get_NonCurrentAssets(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:NonCurrentAssetsIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "NonCurrentAssets")

    except Exception as e:
        print(f"エラー: NonCurrentAssets の取得失敗 - {xbrl_path}: {e}")
        return None


# 資産合計を取得する関数
def get_Assets(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:AssetsIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "Assets")

    except Exception as e:
        print(f"エラー: Assets の取得失敗 - {xbrl_path}: {e}")
        return None


# 利益剰余金を取得する関数
def get_RetainedEarningsIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:RetainedEarningsIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "RetainedEarningsIFRS")

    except Exception as e:
        print(f"エラー: RetainedEarningsIFRS の取得失敗 - {xbrl_path}: {e}")
        return None


# 資本合計を取得する関数
def get_EquityIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:EquityIFRS", context_type='instant')
        return extract_value_from_tag(tag, xbrl_path, "EquityIFRS")

    except Exception as e:
        print(f"エラー: EquityIFRS の取得失敗 - {xbrl_path}: {e}")
        return None


if __name__ == '__main__':
    xbrl_path = r"E:\Zip_files\2471/0101010-qcfs03-tse-qcediffr-24710-2024-02-29-01-2024-04-12-ixbrl.htm"

    print("=== IFRS BS データ取得テスト ===")
    print(f"CashAndCashEquivalent: {get_CashAndCashEquivalent(xbrl_path)}")
    print(f"CurrentAssets: {get_CurrentAssets(xbrl_path)}")
    print(f"PropertyPlantAndEquipment: {get_PropertyPlantAndEquipment(xbrl_path)}")
    print(f"NonCurrentAssets: {get_NonCurrentAssets(xbrl_path)}")
    print(f"Assets: {get_Assets(xbrl_path)}")
    print(f"RetainedEarningsIFRS: {get_RetainedEarningsIFRS(xbrl_path)}")
    print(f"EquityIFRS: {get_EquityIFRS(xbrl_path)}")