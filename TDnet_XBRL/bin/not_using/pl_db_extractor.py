"""
PLのデータベースからデータを抽出する。

"""
import sqlite3
import pandas as pd


class PlDbExtractor:
    def __init__ (self, code):
        self.db_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\db\PL_DB.db"
        self.code = code


    def extract_code(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        code = df_sorted['Code']
        return code

    def extract_public_day(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        public_day = pd.to_datetime(df_sorted['PublicDay'])
        return public_day


    def extract_revenueifrs(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        print(df_sorted)
        revenueifrs = df_sorted['RevenueIFRS']
        return revenueifrs


    def extract_NetSales(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        print(df_sorted)
        netsales = df_sorted['NetSales']
        return netsales


    def extract_sellinggeneralandadministrativeexpensesifrs(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        sellinggeneralandadministrativeexpensesifrs = df_sorted['SellingGeneralAndAdministrativeExpensesIFRS']
        return sellinggeneralandadministrativeexpensesifrs


    def extract_operatingprofitlossifrs(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        operatingprofitlossifrs = df_sorted['OperatingProfitLossIFRS']
        return operatingprofitlossifrs


    def extract_profitlossifrs(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM PL WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        profitlossifrs = df_sorted['ProfitLossIFRS']
        return profitlossifrs


if __name__ == '__main__':
    pldbextractor = PlDbExtractor(4183)
    print(pldbextractor.extract_code())
    print(pldbextractor.extract_public_day())
    print(pldbextractor.extract_revenueifrs())
    print(pldbextractor.extract_NetSales())
    print(pldbextractor.extract_sellinggeneralandadministrativeexpensesifrs())
    print(pldbextractor.extract_operatingprofitlossifrs())
    print(pldbextractor.extract_profitlossifrs())

    pldbextractor.extract_revenueifrs()