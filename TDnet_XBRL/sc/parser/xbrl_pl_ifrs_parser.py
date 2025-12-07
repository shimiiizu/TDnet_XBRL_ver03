from bs4 import BeautifulSoup
from sc.utils.xbrl_utils import find_tag_with_flexible_context, extract_value_from_tag, extract_per_share_value, find_value_in_table


# 売上(億円)を取得する関数
def get_RevenueIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:RevenueIFRS", context_type='duration')
        value = extract_value_from_tag(tag, xbrl_path, "RevenueIFRS")

        # タグが見つからない場合、表形式で探す
        if value is None:
            value = find_value_in_table(soup, ["売上収益", "売上高", "売上", "収益"])
        return value

    except Exception as e:
        print(f'エラー: RevenueIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 販売費及び一般管理費(億円)を取得する関数
def get_SellingGeneralAndAdministrativeExpensesIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:SellingGeneralAndAdministrativeExpensesIFRS", context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "SellingGeneralAndAdministrativeExpensesIFRS")

    except Exception as e:
        print(f'エラー: SellingGeneralAndAdministrativeExpensesIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 営業利益(億円)を取得する関数
def get_OperatingProfitLossIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:OperatingProfitLossIFRS", context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "OperatingProfitLossIFRS")

    except Exception as e:
        print(f'エラー: OperatingProfitLossIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 四半期利益(億円)を取得する関数
def get_ProfitLossIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:ProfitLossIFRS", context_type='duration')
        return extract_value_from_tag(tag, xbrl_path, "ProfitLossIFRS")

    except Exception as e:
        print(f'エラー: ProfitLossIFRS取得失敗 - {xbrl_path}: {e}')
        return None


# 希薄化後１株当たり四半期利益を取得する関数
def get_DilutedEarningsLossPerShareIFRS(xbrl_path):
    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        tag = find_tag_with_flexible_context(soup, "jpigp_cor:DilutedEarningsLossPerShareIFRS", context_type='duration')
        return extract_per_share_value(tag, xbrl_path, "DilutedEarningsLossPerShareIFRS")

    except Exception as e:
        print(f'エラー: DilutedEarningsLossPerShareIFRS取得失敗 - {xbrl_path}: {e}')
        return None


if __name__ == '__main__':
    # テスト用
    xbrl_path = r"E:\Zip_files\4612\0600000-qcpl23-tse-qcediffr-46120-2019-09-30-01-2019-11-14-ixbrl.htm"

    print(f'売上: {get_RevenueIFRS(xbrl_path)}')
    print(f'販管費: {get_SellingGeneralAndAdministrativeExpensesIFRS(xbrl_path)}')
    print(f'営業利益: {get_OperatingProfitLossIFRS(xbrl_path)}')
    print(f'純利益: {get_ProfitLossIFRS(xbrl_path)}')
    print(f'EPS: {get_DilutedEarningsLossPerShareIFRS(xbrl_path)}')