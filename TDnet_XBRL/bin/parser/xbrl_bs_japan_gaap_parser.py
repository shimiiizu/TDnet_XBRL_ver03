import os
from bs4 import BeautifulSoup


# 現金及び預金(億円)を取得する関数
def get_CashAndDeposits(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearInstant"
        elif 'qc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'an' in file_name:
            contextref = "CurrentYearInstant_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        elif 'sc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'sn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        else:
            contextref = "CurrentYearInstant"

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:CashAndDeposits"})

        if tag is None:
            print(f"警告: 現金及び預金が見つかりませんでした: {file_name}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            decimals_value = "-8"  # デフォルト値（億円）

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        cash_and_deposits = tag.text
        cash_and_deposits = int(cash_and_deposits.replace(",", ""))
        cash_and_deposits = round(cash_and_deposits * exchange_ratio, 1)
        return cash_and_deposits

    except Exception as e:
        print(f"エラー: 現金及び預金の取得に失敗: {e}")
        return None


# 流動資産合計(億円)を取得する関数
def get_CurrentAssets(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearInstant"
        elif 'qc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'an' in file_name:
            contextref = "CurrentYearInstant_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        elif 'sc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'sn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        else:
            contextref = "CurrentYearInstant"

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:CurrentAssets"})

        if tag is None:
            print(f"警告: 流動資産が見つかりませんでした: {file_name}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            decimals_value = "-8"

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        current_assets = tag.text
        current_assets = int(current_assets.replace(",", ""))
        current_assets = round(current_assets * exchange_ratio, 1)
        return current_assets

    except Exception as e:
        print(f"エラー: 流動資産の取得に失敗: {e}")
        return None


# 有形固定資産合計(億円)を取得する関数
def get_PropertyPlantAndEquipment(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearInstant"
        elif 'qc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'an' in file_name:
            contextref = "CurrentYearInstant_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        elif 'sc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'sn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        else:
            contextref = "CurrentYearInstant"

        tag = soup.find("ix:nonfraction",
                        attrs={"contextref": contextref, "name": "jppfs_cor:PropertyPlantAndEquipment"})

        if tag is None:
            print(f"警告: 有形固定資産が見つかりませんでした: {file_name}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            decimals_value = "-8"

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        property_plant_and_equipment = tag.text
        property_plant_and_equipment = int(property_plant_and_equipment.replace(",", ""))
        property_plant_and_equipment = round(property_plant_and_equipment * exchange_ratio, 1)
        return property_plant_and_equipment

    except Exception as e:
        print(f"エラー: 有形固定資産の取得に失敗: {e}")
        return None


# 資産合計(億円)を取得する関数
def get_Assets(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearInstant"
        elif 'qc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'an' in file_name:
            contextref = "CurrentYearInstant_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        elif 'sc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'sn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        else:
            contextref = "CurrentYearInstant"

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:Assets"})

        if tag is None:
            print(f"警告: 資産合計が見つかりませんでした: {file_name}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            decimals_value = "-8"

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        assets = tag.text
        assets = int(assets.replace(",", ""))
        assets = round(assets * exchange_ratio, 1)
        return assets

    except Exception as e:
        print(f"エラー: 資産合計の取得に失敗: {e}")
        return None


# 利益剰余金(億円)を取得する関数
def get_RetainedEarnings(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearInstant"
        elif 'qc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'an' in file_name:
            contextref = "CurrentYearInstant_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        elif 'sc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'sn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        else:
            contextref = "CurrentYearInstant"

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:RetainedEarnings"})

        if tag is None:
            print(f"警告: 利益剰余金が見つかりませんでした: {file_name}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            decimals_value = "-8"

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        retainedearnings = tag.text
        retainedearnings = int(retainedearnings.replace(",", ""))
        retainedearnings = round(retainedearnings * exchange_ratio, 1)
        return retainedearnings

    except Exception as e:
        print(f"エラー: 利益剰余金の取得に失敗: {e}")
        return None


# 純資産合計(億円)を取得する関数
def get_NetAssets(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearInstant"
        elif 'qc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'an' in file_name:
            contextref = "CurrentYearInstant_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        elif 'sc' in file_name:
            contextref = "CurrentQuarterInstant"
        elif 'sn' in file_name:
            contextref = "CurrentQuarterInstant_NonConsolidatedMember"
        else:
            contextref = "CurrentYearInstant"

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:NetAssets"})

        if tag is None:
            print(f"警告: 純資産合計が見つかりませんでした: {file_name}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            decimals_value = "-8"

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        NetAssets = tag.text
        NetAssets = int(NetAssets.replace(",", ""))
        NetAssets = round(NetAssets * exchange_ratio, 1)
        return NetAssets

    except Exception as e:
        print(f"エラー: 純資産合計の取得に失敗: {e}")
        return None


if __name__ == '__main__':
    xbrl_path = r"C:\Users\Shimizu\PycharmProjects\TDnet_XBRL\TDnet_XBRL\zip_files\6196\0500000-anbs02-tse-anedjpfr-61960-2016-08-31-01-2016-09-29-ixbrl.htm"
    print(f"現金及び預金: {get_CashAndDeposits(xbrl_path)}億円")
    print(f"流動資産: {get_CurrentAssets(xbrl_path)}億円")
    print(f"有形固定資産: {get_PropertyPlantAndEquipment(xbrl_path)}億円")
    print(f"資産合計: {get_Assets(xbrl_path)}億円")
    print(f"利益剰余金: {get_RetainedEarnings(xbrl_path)}億円")
    print(f"純資産: {get_NetAssets(xbrl_path)}億円")