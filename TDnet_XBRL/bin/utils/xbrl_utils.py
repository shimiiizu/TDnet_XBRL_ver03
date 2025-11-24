"""
XBRL解析用の共通ユーティリティ関数
BS/PL両方で使用する
"""


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
            "CurrentQuarterInstant_NonConsolidatedMember"
        ]
    elif context_type == 'duration':
        # PL用の contextref リスト
        contextref_candidates = [
            "CurrentYearDuration",
            "CurrentQuarterDuration",
            "CurrentYTDDuration",
            "InterimDuration",
            "CurrentYearDuration_NonConsolidatedMember",
            "CurrentQuarterDuration_NonConsolidatedMember"
        ]
    else:
        raise ValueError(f"Invalid context_type: {context_type}")

    # 候補を順番に試す
    for contextref in contextref_candidates:
        tag = soup.find("ix:nonfraction", attrs={
            "contextref": contextref,
            "name": tag_name
        })
        if tag:
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
    """
    1株当たり情報（EPS等）を抽出する関数

    Args:
        tag: BeautifulSoupのタグオブジェクト
        file_path: ファイルパス（エラーメッセージ用）
        field_name: フィールド名（エラーメッセージ用）

    Returns:
        小数点以下2桁の数値、または None
    """
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