import sqlite3


# 新しいデータベースに接続
conn_new = sqlite3.connect(r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\db\Merged_DB.db')
c_new = conn_new.cursor()

# 既存のデータベースをアタッチ
c_new.execute("ATTACH DATABASE ? AS db1", (r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\db\BS_DB.db',))
c_new.execute("ATTACH DATABASE ? AS db2", (r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\db\PL_DB.db',))

# 新しいデータベースにテーブルを作成
c_new.execute('''
CREATE TABLE IF NOT EXISTS MERGED (
    CompanyName TEXT,
    Code INTEGER,
    PublicDay TEXT,
    RevenueIFRS REAL,
    NetSales REAL,
    OperatingIncome REAL,
    Assets REAL,
    FinancialReportType TEXT,
    PRIMARY KEY (Code, PublicDay)
)
''')

# データをマージして新しいデータベースに挿入（重複を更新）
c_new.execute('''
INSERT INTO MERGED (CompanyName, Code, PublicDay, Assets, FinancialReportType, RevenueIFRS, NetSales, OperatingIncome)
SELECT a.CompanyName, a.Code, a.PublicDay, a.Assets, a.FinancialReportType, b.RevenueIFRS, b.NetSales, b.OperatingIncome
FROM db1.BS a
JOIN db2.PL b
ON a.Code = b.Code AND a.PublicDay = b.PublicDay
ON CONFLICT(Code, PublicDay) DO UPDATE SET
    CompanyName=excluded.CompanyName,
    Assets=excluded.Assets,
    FinancialReportType=excluded.FinancialReportType,
    RevenueIFRS=excluded.RevenueIFRS,
    NetSales=excluded.NetSales,
    OperatingIncome=excluded.OperatingIncome
''')

# コミットして接続を閉じる
conn_new.commit()
conn_new.close()
