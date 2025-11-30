from bs4 import BeautifulSoup

# 会社名を取得する関数(←取得できない)
# Fiscal_Yearを取得する関数（←取得できない）


def get_quarter(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonnumeric", attrs={"contextref": "CurrentYTDDuration", "name": "jpcrp_cor:YearToQuarterEndConsolidatedStatementOfIncomeTextBlock"})
    quarter = tag.text
    return quarter


if __name__ == '__main__':
    xbrl_path = r"E:\Zip_files\2471\0102010-qcpl13-tse-qcediffr-24710-2025-08-31-01-2025-10-14-ixbrl.htm"
    print(get_quarter(xbrl_path))