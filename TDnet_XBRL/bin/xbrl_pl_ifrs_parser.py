from bs4 import BeautifulSoup
import os


# 売上(億円)を取得する関数
def get_RevenueIFRS(xbrl_path):
    file_name = os.path.basename(xbrl_path)
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'ac' in file_name:
        contextref = "CurrentYearDuration"
    elif 'qcpl13' in file_name:
        contextref = "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        contextref = "CurrentQuarterDuration"
    elif 'an' in file_name:
        contextref = "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        contextref = "CurrentQuarterDuration_NonConsolidatedMember"

    tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:RevenueIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    revenueifrs = tag.text
    revenueifrs = int(revenueifrs.replace(",", ""))  # カンマを削除
    revenueifrs = round(revenueifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return revenueifrs


# 販売費及び一般管理費(億円)を取得する関数
def get_SellingGeneralAndAdministrativeExpensesIFRS(xbrl_path):
    file_name = os.path.basename(xbrl_path)
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'ac' in file_name:
        contextref = "CurrentYearDuration"
    elif 'qcpl13' in file_name:
        contextref = "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        contextref = "CurrentQuarterDuration"
    elif 'an' in file_name:
        contextref = "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        contextref = "CurrentQuarterDuration_NonConsolidatedMember"

    tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:SellingGeneralAndAdministrativeExpensesIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    sellinggeneralandadministrativeexpensesifrs = tag.text
    sellinggeneralandadministrativeexpensesifrs = int(sellinggeneralandadministrativeexpensesifrs.replace(",", ""))  # カンマを削除
    sellinggeneralandadministrativeexpensesifrs = round(sellinggeneralandadministrativeexpensesifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return sellinggeneralandadministrativeexpensesifrs


# 営業利益(億円)を取得する関数
def get_OperatingProfitLossIFRS(xbrl_path):
    file_name = os.path.basename(xbrl_path)
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'ac' in file_name:
        contextref = "CurrentYearDuration"
    elif 'qcpl13' in file_name:
        contextref = "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        contextref = "CurrentQuarterDuration"
    elif 'an' in file_name:
        contextref = "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        contextref = "CurrentQuarterDuration_NonConsolidatedMember"

    tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:OperatingProfitLossIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    operatingprofitLossifrs = tag.text
    operatingprofitLossifrs = int(operatingprofitLossifrs.replace(",", ""))  # カンマを削除
    operatingprofitLossifrs = round(operatingprofitLossifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return operatingprofitLossifrs


# 営業利益(億円)を取得する関数
def get_OperatingProfitLossIFRS(xbrl_path):
    file_name = os.path.basename(xbrl_path)
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'ac' in file_name:
        contextref = "CurrentYearDuration"
    elif 'qcpl13' in file_name:
        contextref = "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        contextref = "CurrentQuarterDuration"
    elif 'an' in file_name:
        contextref = "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        contextref = "CurrentQuarterDuration_NonConsolidatedMember"

    tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:OperatingProfitLossIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    operatingprofitLossifrs = tag.text
    operatingprofitLossifrs = int(operatingprofitLossifrs.replace(",", ""))  # カンマを削除
    operatingprofitLossifrs = round(operatingprofitLossifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return operatingprofitLossifrs


# 四半期利益(億円)を取得する関数
def get_ProfitLossIFRS(xbrl_path):
    file_name = os.path.basename(xbrl_path)
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'ac' in file_name:
        contextref = "CurrentYearDuration"
    elif 'qcpl13' in file_name:
        contextref = "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        contextref = "CurrentQuarterDuration"
    elif 'an' in file_name:
        contextref = "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        contextref = "CurrentQuarterDuration_NonConsolidatedMember"

    tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:ProfitLossIFRS"})
    decimals_value = tag.get("decimals")  # お金の単位（‐3の時は千円、‐6の時は百万円 ）
    decimals_value = int(decimals_value)
    exchange_ratio = 10 ** (-8 - decimals_value)
    profitLossifrs = tag.text
    profitLossifrs = int(profitLossifrs.replace(",", ""))  # カンマを削除
    profitLossifrs = round(profitLossifrs * exchange_ratio, 1)  # 金額を億円単位に換算
    return profitLossifrs


# 希薄化後１株当たり四半期利益(億円)を取得する関数
def get_DilutedEarningsLossPerShareIFRS(xbrl_path):
    file_name = os.path.basename(xbrl_path)
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'ac' in file_name:
        contextref = "CurrentYearDuration"
    elif 'qcpl13' in file_name:
        contextref = "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        contextref = "CurrentQuarterDuration"
    elif 'an' in file_name:
        contextref = "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        contextref = "CurrentQuarterDuration_NonConsolidatedMember"

    tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:DilutedEarningsLossPerShareIFRS"})
    if tag == None:
        print('希薄化後１株当たり四半期利益(億円)を取得できませんでした。')

    else:
        dilutedearningslosspershareifrs = tag.text
        return dilutedearningslosspershareifrs


if __name__ == '__main__':
    #xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0700000-qcpl23-tse-qcediffr-36790-2023-12-31-01-2024-02-08-ixbrl.htm"
    xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\4183\0102010-acpl03-tse-acediffr-41830-2021-03-31-01-2021-05-13-ixbrl.htm"

    print(get_RevenueIFRS(xbrl_path))
    print(get_SellingGeneralAndAdministrativeExpensesIFRS(xbrl_path))
    print(get_OperatingProfitLossIFRS(xbrl_path))
    print(get_ProfitLossIFRS(xbrl_path))
    print(get_DilutedEarningsLossPerShareIFRS(xbrl_path))