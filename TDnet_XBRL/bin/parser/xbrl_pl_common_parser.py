from bs4 import BeautifulSoup
import re

# 会社名を取得する関数(←取得できない)
# Fiscal_Yearを取得する関数（←取得できない）


def get_quarter(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonnumeric", attrs={"contextref": "CurrentYTDDuration", "name": "jpcrp_cor:YearToQuarterEndConsolidatedStatementOfIncomeTextBlock"})
    quarter = tag.text
    return quarter


def detect_quarter_from_html(xbrl_path):
    """
    XBRL本文から四半期情報を抽出して返す。
    優先順位：
    1. 「当第○四半期」→ Q1〜Q4
    2. 「当中間」→ Q2
    3. 「当連結」または「当単独」→ Q4
    4. 見つからない → Unknown

    Args:
        xbrl_path: XBRLファイルのパス

    Returns:
        str: Q1, Q2, Q3, Q4, または Unknown
    """
    try:
        with open(xbrl_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_text = f.read()

        # 優先順位1: 「当第○四半期」を検出
        m = re.search(r'当第\s*([０-９0-9])\s*四半期', html_text)
        if m:
            q_str = m.group(1)
            q_str = q_str.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
            q = int(q_str)
            if 1 <= q <= 4:
                return f"Q{q}"

        # 優先順位2: 「当中間」を検出 → Q2
        if re.search(r'当\s*中間', html_text):
            return "Q2"

        # 優先順位3: 「当連結」または「当単独」を検出 → Q4
        if re.search(r'当\s*連結', html_text) or re.search(r'当\s*単独', html_text):
            return "Q4"

    except Exception as e:
        print(f"四半期判定エラー: {e}")

    return "Unknown"



if __name__ == '__main__':
    xbrl_path = r"E:\Zip_files\2471\0102010-qcpl13-tse-qcediffr-24710-2025-08-31-01-2025-10-14-ixbrl.htm"
    print(get_quarter(xbrl_path))