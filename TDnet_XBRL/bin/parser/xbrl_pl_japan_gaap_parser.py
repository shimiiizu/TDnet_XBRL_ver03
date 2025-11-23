from bs4 import BeautifulSoup
import os


def _safe_get_value(tag, decimals_target=-8):
    """
    タグから値を安全に取得する汎用関数

    Args:
        tag: BeautifulSoupのタグオブジェクト
        decimals_target: 目標の単位（-8=億円）

    Returns:
        変換後の数値、または取得できない場合はNone
    """
    if tag is None:
        return None

    try:
        decimals_value = tag.get("decimals")
        if decimals_value is None:
            return None

        decimals_value = int(decimals_value)
        exchange_ratio = 10 ** (decimals_target - decimals_value)

        value_text = tag.text.strip()
        if not value_text or value_text == '-':
            return None

        value = int(value_text.replace(",", ""))
        result = round(value * exchange_ratio, 1)
        return result
    except Exception as e:
        print(f"値の変換エラー: {e}")
        return None


def _get_contextref(file_name):
    """ファイル名からcontextrefを決定"""
    if 'ac' in file_name:
        return "CurrentYearDuration"
    elif 'qcpl23' in file_name:
        return "CurrentQuarterDuration"
    elif 'qcpl11' in file_name:
        return "CurrentYTDDuration"
    elif 'an' in file_name:
        return "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        return "CurrentQuarterDuration_NonConsolidatedMember"
    else:
        return "CurrentYearDuration"  # デフォルト


# 売上(億円)を取得する関数
def get_NetSales(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:NetSales"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: NetSalesを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: NetSales取得失敗 - {xbrl_path}: {e}')
        return None


# 販売費及び一般管理費(億円)を取得する関数
def get_SellingGeneralAndAdministrativeExpenses(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction",
                        attrs={"contextref": contextref, "name": "jppfs_cor:SellingGeneralAndAdministrativeExpenses"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: SellingGeneralAndAdministrativeExpensesを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: SellingGeneralAndAdministrativeExpenses取得失敗 - {xbrl_path}: {e}')
        return None


# 営業利益(億円)を取得する関数
def get_OperatingIncome(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:OperatingIncome"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: OperatingIncomeを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: OperatingIncome取得失敗 - {xbrl_path}: {e}')
        return None


# 経常利益(億円)を取得する関数
def get_OrdinaryIncome(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:OrdinaryIncome"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: OrdinaryIncomeを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: OrdinaryIncome取得失敗 - {xbrl_path}: {e}')
        return None


# 純利益(億円)を取得する関数
def get_NetIncome(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)

        # NetIncomeを探す
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:NetIncome"})

        # NetIncomeが見つからない場合はProfitLossを試す
        if tag is None:
            tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jppfs_cor:ProfitLoss"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: NetIncome/ProfitLossを取得できませんでした - {file_name}')
        return result
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