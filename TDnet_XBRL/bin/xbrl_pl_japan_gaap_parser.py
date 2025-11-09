from bs4 import BeautifulSoup
import os


# 売上(億円)を取得する関数
def get_NetSales(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearDuration"
        elif 'qcpl23' in file_name:
            contextref = "CurrentQuarterDuration"
        elif 'qcpl11' in file_name:
            contextref = "CurrentYTDDuration"
        elif 'an' in file_name:
            contextref = "CurrentYearDuration_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterDuration_NonConsolidatedMember"
        else:
            print(f'警告: 未知のファイル名パターン: {file_name}')
            return None

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:NetSales"})

        if tag is None:
            print(f'警告: NetSalesタグが見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = tag.get("decimals")

        if decimals_value is None:
            print(f'警告: decimals属性が見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        netsales = tag.text

        if netsales is None or netsales.strip() == "":
            print(f'警告: 売上高の値が空です。ファイル: {file_name}')
            return None

        netsales = int(netsales.replace(",", ""))  # カンマを削除
        netsales = round(netsales * exchange_ratio, 1)  # 金額を億円単位に換算
        return netsales

    except Exception as e:
        print(f'エラー: NetSales取得失敗 - {e}, ファイル: {xbrl_path}')
        return None


# 販売費及び一般管理費(億円)を取得する関数
def get_SellingGeneralAndAdministrativeExpenses(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearDuration"
        elif 'qcpl23' in file_name:
            contextref = "CurrentQuarterDuration"
        elif 'qcpl11' in file_name:
            contextref = "CurrentYTDDuration"
        elif 'an' in file_name:
            contextref = "CurrentYearDuration_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterDuration_NonConsolidatedMember"
        else:
            print(f'警告: 未知のファイル名パターン: {file_name}')
            return None

        tag = soup.find("ix:nonfraction",
                        attrs={"contextref": contextref, "name": "jppfs_cor:SellingGeneralAndAdministrativeExpenses"})

        if tag is None:
            print(f'警告: SellingGeneralAndAdministrativeExpensesを取得できませんでした。ファイル: {file_name}')
            return None

        decimals_value = tag.get("decimals")

        if decimals_value is None:
            print(f'警告: decimals属性が見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        sellingGeneralandadministrativeexpenses = tag.text

        if sellingGeneralandadministrativeexpenses is None or sellingGeneralandadministrativeexpenses.strip() == "":
            print(f'警告: 販管費の値が空です。ファイル: {file_name}')
            return None

        sellingGeneralandadministrativeexpenses = int(sellingGeneralandadministrativeexpenses.replace(",", ""))
        sellingGeneralandadministrativeexpenses = round(sellingGeneralandadministrativeexpenses * exchange_ratio, 1)
        return sellingGeneralandadministrativeexpenses

    except Exception as e:
        print(f'エラー: SellingGeneralAndAdministrativeExpenses取得失敗 - {e}, ファイル: {xbrl_path}')
        return None


# 営業利益(億円)を取得する関数
def get_OperatingIncome(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearDuration"
        elif 'qcpl23' in file_name:
            contextref = "CurrentQuarterDuration"
        elif 'qcpl11' in file_name:
            contextref = "CurrentYTDDuration"
        elif 'an' in file_name:
            contextref = "CurrentYearDuration_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterDuration_NonConsolidatedMember"
        else:
            print(f'警告: 未知のファイル名パターン: {file_name}')
            return None

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:OperatingIncome"})

        if tag is None:
            print(f'警告: OperatingIncomeタグが見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = tag.get("decimals")

        if decimals_value is None:
            print(f'警告: decimals属性が見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        operatingincome = tag.text

        if operatingincome is None or operatingincome.strip() == "":
            print(f'警告: 営業利益の値が空です。ファイル: {file_name}')
            return None

        operatingincome = int(operatingincome.replace(",", ""))
        operatingincome = round(operatingincome * exchange_ratio, 1)
        return operatingincome

    except Exception as e:
        print(f'エラー: OperatingIncome取得失敗 - {e}, ファイル: {xbrl_path}')
        return None


# 経常利益(億円)を取得する関数
def get_OrdinaryIncome(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearDuration"
        elif 'qcpl23' in file_name:
            contextref = "CurrentQuarterDuration"
        elif 'qcpl11' in file_name:
            contextref = "CurrentYTDDuration"
        elif 'an' in file_name:
            contextref = "CurrentYearDuration_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterDuration_NonConsolidatedMember"
        else:
            print(f'警告: 未知のファイル名パターン: {file_name}')
            return None

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:OrdinaryIncome"})

        if tag is None:
            print(f'警告: OrdinaryIncomeタグが見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = tag.get("decimals")

        if decimals_value is None:
            print(f'警告: decimals属性が見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        ordinaryincome = tag.text

        if ordinaryincome is None or ordinaryincome.strip() == "":
            print(f'警告: 経常利益の値が空です。ファイル: {file_name}')
            return None

        ordinaryincome = int(ordinaryincome.replace(",", ""))
        ordinaryincome = round(ordinaryincome * exchange_ratio, 1)
        return ordinaryincome

    except Exception as e:
        print(f'エラー: OrdinaryIncome取得失敗 - {e}, ファイル: {xbrl_path}')
        return None


# 純利益(億円)を取得する関数
def get_NetIncome(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        if 'ac' in file_name:
            contextref = "CurrentYearDuration"
        elif 'qcpl23' in file_name:
            contextref = "CurrentQuarterDuration"
        elif 'qcpl11' in file_name:
            contextref = "CurrentYTDDuration"
        elif 'an' in file_name:
            contextref = "CurrentYearDuration_NonConsolidatedMember"
        elif 'qn' in file_name:
            contextref = "CurrentQuarterDuration_NonConsolidatedMember"
        else:
            print(f'警告: 未知のファイル名パターン: {file_name}')
            return None

        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:NetIncome"})

        if tag is None:
            tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:ProfitLoss"})

            if tag is None:
                print(f'警告: NetIncome/ProfitLossタグが見つかりませんでした。ファイル: {file_name}')
                return None

        decimals_value = tag.get("decimals")

        if decimals_value is None:
            print(f'警告: decimals属性が見つかりませんでした。ファイル: {file_name}')
            return None

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (-8 - decimals_value)
        netincome = tag.text

        if netincome is None or netincome.strip() == "":
            print(f'警告: 純利益の値が空です。ファイル: {file_name}')
            return None

        netincome = int(netincome.replace(",", ""))
        netincome = round(netincome * exchange_ratio, 1)
        return netincome

    except Exception as e:
        print(f'エラー: NetIncome取得失敗 - {e}, ファイル: {xbrl_path}')
        return None


if __name__ == '__main__':
    # xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0301000-acpl01-tse-acedjpfr-36790-2015-03-31-01-2015-05-15-ixbrl.htm"
    # xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0301000-acpl01-tse-acedjpfr-36790-2015-03-31-01-2015-05-15-ixbrl.htm"
    # xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0600000-qcpl11-tse-qcedjpfr-36790-2014-06-30-01-2014-08-12-ixbrl.htm"
    # xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0600000-qcpl11-tse-qcedjpfr-36790-2014-06-30-01-2014-08-12-ixbrl.htm"
    xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\7172\0102010-acpl01-tse-acedjpfr-71720-2014-12-31-01-2015-02-12-ixbrl.htm"

    print(f'売上: {get_NetSales(xbrl_path)}')
    print(f'販管費: {get_SellingGeneralAndAdministrativeExpenses(xbrl_path)}')
    print(f'営業利益: {get_OperatingIncome(xbrl_path)}')
    print(f'純利益: {get_NetIncome(xbrl_path)}')