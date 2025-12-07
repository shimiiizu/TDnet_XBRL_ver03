"""
XBRL解析用の共通ユーティリティ関数
BS/PL両方で使用する
"""
from bs4 import BeautifulSoup

def find_tag_with_flexible_context(soup, tag_name, context_type='instant'):
    """
    複数の contextref を試して、タグを取得する共通関数

    Args:
        soup: BeautifulSoupオブジェクト
        tag_name: 検索するタグ名（例: "jpigp_cor:AssetsIFRS"）
        context_type: 'instant'（BS用）または 'duration'（PL用）

    Returns:
        見つかったタグ、または None
    """
    if context_type == 'instant':
        # BS用の contextref リスト
        contextref_candidates = [
            "CurrentYearInstant",
            "CurrentQuarterInstant",
            "CurrentYTDInstant",
            "CurrentPeriodInstant",
            "CurrentYearInstant_NonConsolidatedMember",
            "CurrentQuarterInstant_NonConsolidatedMember",
            "InterimInstant"
        ]
    elif context_type == 'duration':
        # PL用の contextref リスト
        contextref_candidates = [
            "CurrentYearDuration",
            "CurrentQuarterDuration",
            "CurrentYTDDuration",
            "InterimDuration",
            "CurrentYearDuration_NonConsolidatedMember",
            "CurrentQuarterDuration_NonConsolidatedMember",
            "CurrentYTDDuration_NonConsolidatedMember",
            "Prior1YTDDuration_NonConsolidatedMember",
        ]
    else:
        raise ValueError(f"Invalid context_type: {context_type}")

    # タグタイプのリスト（大文字小文字両方対応）
    tag_types = ["ix:nonfraction", "ix:nonFraction", "ix:nonNumeric"]

    # 候補を順番に試す
    for tag_type in tag_types:
        for contextref in contextref_candidates:
            tag = soup.find(tag_type, attrs={
                "contextref": contextref,
                "name": tag_name
            })
            if tag:
                return tag

    # contextref なしでも探してみる（最終手段）
    for tag_type in tag_types:
        tag = soup.find(tag_type, attrs={"name": tag_name})
        if tag:
            print(f"警告: contextref なしで {tag_name} を発見")
            return tag

    return None


def extract_value_from_tag(tag, file_path, field_name, decimals_target=-8):
    """
    タグから値を抽出し、指定の単位に変換する共通関数

    Args:
        tag: BeautifulSoupのタグオブジェクト
        file_path: ファイルパス（エラーメッセージ用）
        field_name: フィールド名（エラーメッセージ用）
        decimals_target: 目標の単位（-8=億円）

    Returns:
        変換後の数値、または None
    """
    try:
        if not tag:
            print(f"警告: {field_name} のタグが見つかりませんでした - {file_path}")
            return None

        decimals_value = tag.get("decimals")
        if decimals_value is None:
            print(f"警告: {field_name} の decimals 属性がありません - {file_path}")
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
        print(f"エラー: {field_name} の抽出中にエラーが発生 - {file_path}: {e}")
        return None


def extract_per_share_value(tag, file_path, field_name):
    try:
        if not tag:
            print(f"警告: {field_name} のタグが見つかりませんでした - {file_path}")
            return None

        value_text = tag.text.strip()
        if not value_text or value_text == '-':
            return None

        result = round(float(value_text.replace(",", "")), 2)
        return result

    except Exception as e:
        print(f"エラー: {field_name} の抽出中にエラーが発生 - {file_path}: {e}")
        return None

# ★ fallback: XBRLタグが無い場合、表から値を抽出
def find_value_in_table(soup, label_candidates, is_eps=False):
    """
    HTML表から財務数値を抽出する汎用関数。

    ◆ 対応機能
      - 売上収益のようなラベル行に対応
      - 右端の当期列を自動抽出（182,694 → OK）
      - △表記の負数対応
      - 百万円 → 億円への換算（EPSは換算しない）
    """
    print(f"表から値を抽出を試みます。... ラベル候補: {label_candidates}")
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        # 1列目テキストが候補ラベルに一致する行を探す
        first_text = cells[0].get_text(strip=True)
        if not any(label in first_text for label in label_candidates):
            continue

        # 数値候補をすべて抽出し、最も右側（当期）を採用
        num_candidates = []
        for cell in cells:
            raw = cell.get_text(strip=True)
            cleaned = raw.replace(",", "").replace("△", "-")

            # 数値判定部分を修正
            if cleaned.replace(".", "", 1).isdigit() or \
                    (cleaned.startswith("-") and cleaned[1:].replace(".", "", 1).isdigit()):
                num_candidates.append(cleaned)

        if not num_candidates:
            return None

        # 最右列（当期）を採用
        value = float(num_candidates[-1])

        # 単位換算
        if not is_eps:
            value = value / 100.0  # 百万円 → 億円
        else:
            value = value   # 円
        return value

    #return None

if __name__ == "__main__":
    import os
    from bs4 import BeautifulSoup

    # 実ファイルの絶対パス
    xbrl_path = r"E:\Zip_files\4612\0600000-qcpl23-tse-qcediffr-46120-2019-09-30-01-2019-11-14-ixbrl.htm"
    print(f"解析対象ファイル: {os.path.abspath(xbrl_path)}")

    try:
        with open(xbrl_path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"ファイルを開けませんでした: {xbrl_path} - {e}")
        exit(1)

    soup = BeautifulSoup(html, "html.parser")

    # --- 売上収益 ---
    tag_sales = find_tag_with_flexible_context(soup, "jpigp_cor:RevenueIFRS", context_type="duration")
    sales_tag_value = extract_value_from_tag(tag_sales, xbrl_path, "RevenueIFRS")
    print("売上収益（タグから取得）:", sales_tag_value)

    sales_table_value = find_value_in_table(soup, ["売上収益"], is_eps=False)
    print("売上収益（表から取得）:", sales_table_value)
    print('------------------------------')

    # --- 営業利益 ---
    tag_op = find_tag_with_flexible_context(soup, "jpigp_cor:OperatingProfitLossIFRS", context_type="duration")
    op_tag_value = extract_value_from_tag(tag_op, xbrl_path, "OperatingProfitLossIFRS")
    print("営業利益（タグから取得）:", op_tag_value)

    op_table_value = find_value_in_table(soup, ["営業利益"], is_eps=False)
    print("営業利益（表から取得）:", op_table_value)
    print('------------------------------')

    # --- 純利益 ---
    tag_pl = find_tag_with_flexible_context(soup, "jpigp_cor:ProfitLossIFRS", context_type="duration")
    pl_tag_value = extract_value_from_tag(tag_pl, xbrl_path, "ProfitLossIFRS")
    print("純利益（タグから取得）:", pl_tag_value)

    pl_table_value = find_value_in_table(soup, ["四半期利益", "損益", "当期利益", "当期純利益", "純利益"], is_eps=False)
    print("純利益（表から取得）:", pl_table_value)
    print('------------------------------')

    # --- EPS ---
    tag_eps = find_tag_with_flexible_context(soup, "jpigp_cor:DilutedEarningsLossPerShareIFRS", context_type="duration")
    eps_tag_value = extract_per_share_value(tag_eps, xbrl_path, "EPS")
    print("EPS（タグから取得）:", eps_tag_value)

    eps_table_value = find_value_in_table(soup, ["希薄化後１株当たり四半期利益","希薄化後1株当たり利益", "希薄化後１株当たり利益", "1株当たり利益", "１株当たり利益","基本的１株当たり四半期利益"], is_eps=True)
    print("EPS（表から取得）:", eps_table_value)