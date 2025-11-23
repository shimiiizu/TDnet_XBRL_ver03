"""
BSのデータベースからデータを抽出する。

"""
import sqlite3
import pandas as pd


class BsDbExtractor:
    def __init__ (self, code):
        self.db_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\db\BS_DB.db"
        self.code = code

    def extract_data(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        company_name = df_sorted['CompanyName'].iat[-1]
        public_day = pd.to_datetime(df_sorted['PublicDay'])
        assets = df_sorted['Assets']
        retainedearnings = df_sorted['RetainedEarnings']
        equity = df_sorted['Equity']
        netassets = df_sorted['NetAssets']

        return company_name, public_day, assets, retainedearnings, equity, netassets

    def extract_company_name(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        company_name = df_sorted['CompanyName'].iat[-1]
        return company_name

    def extract_public_day(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        public_day = pd.to_datetime(df_sorted['PublicDay'])
        return public_day

    def extract_assets(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        assets = df_sorted['Assets']
        return assets

    def extract_retainedearnings(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        retainedearnings = df_sorted['RetainedEarnings']
        return retainedearnings

    def extract_equity(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        equity = df_sorted['Equity']
        return equity

    def extract_NetAssets(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM BS WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        netassets = df_sorted['NetAssets']
        return netassets



if __name__ == '__main__':
    bsdbextractor = BsDbExtractor(3679)
    company_name, public_day, assets, retainedearnings, equity, netassets = bsdbextractor.extract_data()
    print(bsdbextractor.extract_retainedearnings())
    print(bsdbextractor.extract_equity())
    print(bsdbextractor.extract_NetAssets())


