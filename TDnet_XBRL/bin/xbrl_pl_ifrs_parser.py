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
    elif 'qcpl13' in file_name:
        return "CurrentYTDDuration"
    elif 'qcpl23' in file_name:
        return "CurrentQuarterDuration"
    elif 'an' in file_name:
        return "CurrentYearDuration_NonConsolidatedMember"
    elif 'qn' in file_name:
        return "CurrentQuarterDuration_NonConsolidatedMember"
    else:
        return "CurrentYearDuration"  # デフォルト


# 売上(億円)を取得する関数
def get_RevenueIFRS(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:RevenueIFRS"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: RevenueIFRSを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: RevenueIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 販売費及び一般管理費(億円)を取得する関数
def get_SellingGeneralAndAdministrativeExpensesIFRS(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref,
                                                 "name": "jpigp_cor:SellingGeneralAndAdministrativeExpensesIFRS"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: SellingGeneralAndAdministrativeExpensesIFRSを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: SellingGeneralAndAdministrativeExpensesIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 営業利益(億円)を取得する関数
def get_OperatingProfitLossIFRS(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:OperatingProfitLossIFRS"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: OperatingProfitLossIFRSを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: OperatingProfitLossIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 四半期利益(億円)を取得する関数
def get_ProfitLossIFRS(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction", attrs={"contextref": contextref, "name": "jpigp_cor:ProfitLossIFRS"})

        result = _safe_get_value(tag)
        if result is None:
            print(f'警告: ProfitLossIFRSを取得できませんでした - {file_name}')
        return result
    except Exception as e:
        print(f'エラー: ProfitLossIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 希薄化後１株当たり四半期利益を取得する関数
def get_DilutedEarningsLossPerShareIFRS(xbrl_path):
    try:
        file_name = os.path.basename(xbrl_path)
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        contextref = _get_contextref(file_name)
        tag = soup.find("ix:nonfraction",
                        attrs={"contextref": contextref, "name": "jpigp_cor:DilutedEarningsLossPerShareIFRS"})

        if tag is None:
            print(f'警告: DilutedEarningsLossPerShareIFRSを取得できませんでした - {file_name}')
            return None

        try:
            value_text = tag.text.strip()
            if not value_text or value_text == '-':
                return None
            return round(float(value_text.replace(",", "")), 2)
        except:
            return None
    except Exception as e:
        print(f'エラー: DilutedEarningsLossPerShareIFRS取得失敗 - {xbrl_path}: {e}')
        return None


if __name__ == '__main__':
    # テスト用
    xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\4183\0102010-acpl03-tse-acediffr-41830-2021-03-31-01-2021-05-13-ixbrl.htm"

    print(f'売上: {get_RevenueIFRS(xbrl_path)}')
    print(f'販管費: {get_SellingGeneralAndAdministrativeExpensesIFRS(xbrl_path)}')
    print(f'営業利益: {get_OperatingProfitLossIFRS(xbrl_path)}')
    print(f'純利益: {get_ProfitLossIFRS(xbrl_path)}')
    print(f'EPS: {get_DilutedEarningsLossPerShareIFRS(xbrl_path)}')