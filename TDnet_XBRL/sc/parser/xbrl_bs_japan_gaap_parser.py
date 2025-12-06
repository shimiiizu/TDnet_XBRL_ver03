import os
from bs4 import BeautifulSoup

# utils の読み込み
from sc.utils.xbrl_utils import find_tag_with_flexible_context, extract_value_from_tag


# 内部 util：BeautifulSoup 読み込み
def _load_soup(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')


# ===========================
#  各 BS 項目取得関数
# ===========================

def get_CashAndDeposits(xbrl_path):
    soup = _load_soup(xbrl_path)
    tag = find_tag_with_flexible_context(soup, "jppfs_cor:CashAndDeposits", context_type='instant')
    return extract_value_from_tag(tag, xbrl_path, "CashAndDeposits")


def get_CurrentAssets(xbrl_path):
    soup = _load_soup(xbrl_path)
    tag = find_tag_with_flexible_context(soup, "jppfs_cor:CurrentAssets", context_type='instant')
    return extract_value_from_tag(tag, xbrl_path, "CurrentAssets")


def get_PropertyPlantAndEquipment(xbrl_path):
    soup = _load_soup(xbrl_path)
    tag = find_tag_with_flexible_context(soup, "jppfs_cor:PropertyPlantAndEquipment", context_type='instant')
    return extract_value_from_tag(tag, xbrl_path, "PropertyPlantAndEquipment")


def get_Assets(xbrl_path):
    soup = _load_soup(xbrl_path)
    tag = find_tag_with_flexible_context(soup, "jppfs_cor:Assets", context_type='instant')
    return extract_value_from_tag(tag, xbrl_path, "Assets")


def get_RetainedEarnings(xbrl_path):
    soup = _load_soup(xbrl_path)
    tag = find_tag_with_flexible_context(soup, "jppfs_cor:RetainedEarnings", context_type='instant')
    return extract_value_from_tag(tag, xbrl_path, "RetainedEarnings")


def get_NetAssets(xbrl_path):
    soup = _load_soup(xbrl_path)
    tag = find_tag_with_flexible_context(soup, "jppfs_cor:NetAssets", context_type='instant')
    return extract_value_from_tag(tag, xbrl_path, "NetAssets")


# ===========================
#     テスト用コード復活
# ===========================

if __name__ == '__main__':

    # ★ 元コードにあったテストパスを復元 ★
    xbrl_path = r"E:\Zip_files\5233\0500000-scbs15-tse-scedjpfr-52330-2025-09-30-01-2025-11-11-ixbrl.htm"

    print(f"現金及び預金: {get_CashAndDeposits(xbrl_path)} 億円")
    print(f"流動資産: {get_CurrentAssets(xbrl_path)} 億円")
    print(f"有形固定資産: {get_PropertyPlantAndEquipment(xbrl_path)} 億円")
    print(f"資産合計: {get_Assets(xbrl_path)} 億円")
    print(f"利益剰余金: {get_RetainedEarnings(xbrl_path)} 億円")
    print(f"純資産: {get_NetAssets(xbrl_path)} 億円")
