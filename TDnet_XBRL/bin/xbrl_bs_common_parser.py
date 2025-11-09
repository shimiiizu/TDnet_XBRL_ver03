from bs4 import BeautifulSoup


# 会社名を取得する関数
def get_company_name(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:FilerNameInJapaneseDEI"})

        if element is None:
            print(f"警告: {xbrl_path} で会社名が見つかりませんでした。")
            return "不明"

        return element.text
    except Exception as e:
        print(f"エラー: 会社名の取得に失敗しました: {e}")
        return "不明"


# 決算開始日を取得する関数
def get_CurrentFiscalYearStartDateDEI(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:CurrentFiscalYearStartDateDEI"})

        if element is None:
            print(f"警告: {xbrl_path} で決算開始日が見つかりませんでした。")
            return None

        return element.text
    except Exception as e:
        print(f"エラー: 決算開始日の取得に失敗しました: {e}")
        return None


# 決算終了日を取得する関数
def get_CurrentPeriodEndDateDEI(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:CurrentPeriodEndDateDEI"})

        if element is None:
            print(f"警告: {xbrl_path} で決算終了日が見つかりませんでした。")
            return None

        return element.text
    except Exception as e:
        print(f"エラー: 決算終了日の取得に失敗しました: {e}")
        return None


# 決算タイプを取得する関数
def get_TypeOfCurrentPeriodDEI(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:TypeOfCurrentPeriodDEI"})

        if element is None:
            print(f"警告: {xbrl_path} で決算タイプが見つかりませんでした。")
            return None

        return element.text
    except Exception as e:
        print(f"エラー: 決算タイプの取得に失敗しました: {e}")
        return None


# 会計の形式を取得する関数
def get_AccountingStandard(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        # 複数のパターンを試す
        element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:AccountingStandardsDEI"})

        if element is None:
            # 別の属性名を試す
            element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:AccountingStandardDEI"})

        if element is None:
            # さらに別のパターン（古いバージョン）
            element = soup.find("jpdei_cor:AccountingStandardsDEI")

        if element is None:
            print(f"警告: {xbrl_path} で会計基準が見つかりませんでした。デフォルト値(Japan GAAP)を使用します。")
            return "Japan GAAP"  # デフォルト値

        return element.text

    except Exception as e:
        print(f"エラー: 会計基準の取得に失敗しました: {e}")
        return "Japan GAAP"  # デフォルト値


if __name__ == '__main__':
    xbrl_path = r"C:\Users\Shimizu\PycharmProjects\TDnet_XBRL\TDnet_XBRL\zip_files\9163\0300000-acbs03-tse-acediffr-91630-2023-10-31-01-2023-12-13-ixbrl.htm"

    print(f"会社名: {get_company_name(xbrl_path)}")
    print(f"決算開始日: {get_CurrentFiscalYearStartDateDEI(xbrl_path)}")
    print(f"決算終了日: {get_CurrentPeriodEndDateDEI(xbrl_path)}")
    print(f"決算タイプ: {get_TypeOfCurrentPeriodDEI(xbrl_path)}")
    print(f"会計基準: {get_AccountingStandard(xbrl_path)}")