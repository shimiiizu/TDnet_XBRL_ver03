from bs4 import BeautifulSoup


"""
# 会社名を取得する関数
def get_company_name(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f: # ローカルのHTMLファイルを読み込む
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser') # BeautifulSoupでHTMLをパース
    company_name = soup.find("ix:nonnumeric", attrs={"name": "jpdei_cor:FilerNameInJapaneseDEI"}).text
    return company_name
"""

def get_quarter(xbrl_path):
    with open(xbrl_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find("ix:nonnumeric", attrs={"contextref": "CurrentYTDDuration", "name": "jpcrp_cor:YearToQuarterEndConsolidatedStatementOfIncomeTextBlock"})
    quarter = tag.text
    return quarter



if __name__ == '__main__':
    xbrl_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\4183\0102010-qcpl11-tse-qcedjpfr-41830-2014-06-30-01-2014-08-01-ixbrl.htm"
    #get_company_name(xbrl_path)
    print(get_quarter(xbrl_path))