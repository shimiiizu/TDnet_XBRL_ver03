from bs4 import BeautifulSoup


# 現金同等額(億円)を取得する関数
def get_CashAndCashEquivalent(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction", attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:CashAndCashEquivalentsIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    CashAndCashEquivalent = tag.text
    CashAndCashEquivalent = int(CashAndCashEquivalent.replace(",", ""))  # カンマを削除
    CashAndCashEquivalent = round(CashAndCashEquivalent * exchange_ratio, 1)  # 金額を億円単位に換算
    return CashAndCashEquivalent


# 流動資産合計を取得する関数
def get_CurrentAssets(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction",
                    attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:CurrentAssetsIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    CurrentAssets = tag.text
    CurrentAssets = int(CurrentAssets.replace(",", ""))  # カンマを削除
    CurrentAssets = round(CurrentAssets * exchange_ratio, 1)  # 金額を億円単位に換算
    return CurrentAssets


# 有形固定資産を取得する関数
def get_PropertyPlantAndEquipment(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction",
                    attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:PropertyPlantAndEquipmentIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    PropertyPlantAndEquipment = tag.text
    PropertyPlantAndEquipment = int(PropertyPlantAndEquipment.replace(",", ""))  # カンマを削除
    PropertyPlantAndEquipment = round(PropertyPlantAndEquipment * exchange_ratio, 1)  # 金額を億円単位に換算
    return PropertyPlantAndEquipment


# 非流動資産合計を取得する関数
def get_NonCurrentAssets(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction",
                    attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:NonCurrentAssetsIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    NonCurrentAssets = tag.text
    NonCurrentAssets = int(NonCurrentAssets.replace(",", ""))  # カンマを削除
    NonCurrentAssets = round(NonCurrentAssets * exchange_ratio, 1)  # 金額を億円単位に換算
    return NonCurrentAssets


# 資産合計を取得する関数
def get_Assets(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction",
                    attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:AssetsIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    Assets = tag.text
    Assets = int(Assets.replace(",", ""))  # カンマを削除
    Assets = round(Assets * exchange_ratio, 1)  # 金額を億円単位に換算
    return Assets


# 利益剰余金を取得する関数
def get_RetainedEarningsIFRS(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction",
                    attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:RetainedEarningsIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    retainedearningsifrs = tag.text
    retainedearningsifrs = int(retainedearningsifrs.replace(",", ""))  # カンマを削除
    retainedearningsifrs = round(retainedearningsifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return retainedearningsifrs


# 資本合計を取得する関数
def get_EquityIFRS(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonfraction",
                    attrs={"contextref": "CurrentYearInstant", "name": "jpigp_cor:EquityIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    equityifrs = tag.text
    equityifrs = int(equityifrs.replace(",", ""))  # カンマを削除
    equityifrs = round(equityifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return equityifrs


if __name__ == '__main__':
    xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files/9163/0300000-acbs03-tse-acediffr-91630-2023-10-31-01-2023-12-13-ixbrl.htm"
    get_CashAndCashEquivalent(xbrl_path)
    get_CurrentAssets(xbrl_path)
    get_PropertyPlantAndEquipment(xbrl_path)
    get_NonCurrentAssets(xbrl_path)
    get_Assets(xbrl_path)
    print(get_CashAndCashEquivalent(xbrl_path))
    print(get_CurrentAssets(xbrl_path))
    print(get_PropertyPlantAndEquipment(xbrl_path))
    print(get_NonCurrentAssets(xbrl_path))
    print(get_Assets(xbrl_path))
    print(get_RetainedEarningsIFRS(xbrl_path))
    print(get_EquityIFRS(xbrl_path))