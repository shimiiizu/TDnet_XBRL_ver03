from bs4 import BeautifulSoup
import re

# ------------------------------------------------------------
# 会社名を取得する
# ------------------------------------------------------------
def get_company_name(xbrl_path):
    print(f"[CALL] get_company_name(xbrl_path={xbrl_path})")

    try:
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        print("[INFO] HTML読み込み完了（会社名取得）")

        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:FilerNameInJapaneseDEI"})

        if element is None:
            print(f"[WARN] 会社名タグが見つかりませんでした: {xbrl_path}")
            print("[RETURN] get_company_name -> 不明")
            return "不明"

        company_name = element.text.strip()
        print(f"[RETURN] get_company_name -> {company_name}")
        return company_name

    except Exception as e:
        print(f"[ERROR] get_company_name 例外: {e}")
        print("[RETURN] get_company_name -> 不明")
        return "不明"


# ------------------------------------------------------------
# XBRL本文から四半期情報を抽出する
# ------------------------------------------------------------
def detect_quarter_from_html(xbrl_path):
    print(f"[CALL] detect_quarter_from_html(xbrl_path={xbrl_path})")

    """
    優先順位：
    1. 「当第○四半期」→ Q1〜Q4
    2. 「当中間」→ Q2
    3. 「当連結」「当単独」「当事業」→ Q4
    4. 見つからない → Unknown
    """

    try:
        with open(xbrl_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_text = f.read()

        print("[INFO] HTML読み込み完了（四半期判定）")

        # ----------------------------------------------------
        # 優先順位1: 「当第○四半期」
        # ----------------------------------------------------
        m = re.search(r'当第\s*([０-９0-9])\s*四半期', html_text)
        if m:
            raw = m.group(1)
            print(f"[MATCH] 当第○四半期 raw={raw}")

            # 全角→半角変換
            q_str = raw.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
            q = int(q_str)

            if 1 <= q <= 4:
                result = f"Q{q}"
                print(f"[RETURN] detect_quarter_from_html -> {result}")
                return result

        # ----------------------------------------------------
        # 優先順位2: 「当中間」→ Q2
        # ----------------------------------------------------
        if re.search(r'当\s*中間', html_text):
            print("[MATCH] 当中間 → Q2")
            print("[RETURN] detect_quarter_from_html -> Q2")
            return "Q2"

        # ----------------------------------------------------
        # 優先順位3: 「当連結」「当単独」「当事業」→ Q4
        # ----------------------------------------------------
        if (re.search(r'当\s*連結', html_text) or
            re.search(r'当\s*単独', html_text) or
            re.search(r'当\s*事業', html_text)):
            print("[MATCH] 当連結/当単独/当事業 → Q4")
            print("[RETURN] detect_quarter_from_html -> Q4")
            return "Q4"

    except Exception as e:
        print(f"[ERROR] detect_quarter_from_html 例外: {e}")

    # ----------------------------------------------------
    # 見つからなかった場合
    # ----------------------------------------------------
    print("[WARN] 四半期情報が見つからなかった → Unknown")
    print("[RETURN] detect_quarter_from_html -> Unknown")
    return "Unknown"


# ------------------------------------------------------------
# テスト
# ------------------------------------------------------------
if __name__ == '__main__':
    xbrl_path = r"E:\Zip_files\3679\0300000-acbs01-tse-acedjpfr-36790-2015-03-31-01-2015-05-15-ixbrl.htm"

    print(get_company_name(xbrl_path))
    print(detect_quarter_from_html(xbrl_path))
