import os
from bs4 import BeautifulSoup

# utils の読み込み
from bin.utils.xbrl_utils import find_tag_with_flexible_context, extract_value_from_tag


# 内部 util：BeautifulSoup 読み込み
def _load_soup(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')


# --- 個別項目 ---

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
