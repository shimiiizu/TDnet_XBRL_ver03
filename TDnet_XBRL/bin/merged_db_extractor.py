"""
Mergeデータベースからデータを抽出する。

"""
import sqlite3
import pandas as pd
import numpy as np


class MergedDbExtractor:
    def __init__ (self, code):
        self.db_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\db\Merged_DB.db"
        self.code = code


    def extract_code(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM MERGED WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        code = df_sorted['Code']
        return code

    def extract_public_day(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM MERGED WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        public_day = pd.to_datetime(df_sorted['PublicDay'])
        return public_day

    def extract_CompanyName(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM MERGED WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        companyname = df_sorted['CompanyName'].iloc[-1]
        return companyname
    

    def extract_FinancialReportType(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM MERGED WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        publfinancialreporttype = df_sorted['FinancialReportType']
        return publfinancialreporttype

    def extract_NetSales(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM MERGED WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        netsales = df_sorted['NetSales']
        print(df_sorted)
        newNetSaleslist = []

        for index, elem in enumerate(df_sorted['NetSales']):
            print(f'{index, elem, df_sorted['FinancialReportType'][index]}')
            if df_sorted['FinancialReportType'][index] == 'Q1':
                print('Q1です')
                newNetSaleslist.append(elem)

            elif df_sorted['FinancialReportType'][index] == 'Q2':
                print('Q2です。ひとつ前はQ1です。')
                if index-1 < 0:
                    newNetSaleslist.append(0)
                elif df_sorted['FinancialReportType'][index-1] == 'Q1':
                    newNetSaleslist.append(np.round(elem-df_sorted['NetSales'][index-1],1))

            elif df_sorted['FinancialReportType'][index] == 'Q3':
                print('Q3です')
                if index - 1 < 0:
                    newNetSaleslist.append("nan")
                else:
                    newNetSaleslist.append(np.round(elem - df_sorted['NetSales'][index - 1], 1))

            elif df_sorted['FinancialReportType'][index] == 'FY':
                print('FYです')
                if index - 1 < 0:
                    newNetSaleslist.append(0)
                else:
                    newNetSaleslist.append(np.round(elem - df_sorted['NetSales'][index - 1], 1))
        return newNetSaleslist

    def extract_assets(self):
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM MERGED WHERE Code = '{self.code}'"
        df = pd.read_sql_query(query, conn)
        df_sorted = df.sort_values(by='PublicDay')
        assets = df_sorted['Assets']
        return assets

        # すべての要素を float 型に変換
        newNetSaleslist = [float(x) for x in newNetSaleslist]
        # print(f'newNetSaleslist:{newNetSaleslist}')
        # print(f'newNetSaleslistの要素の数:{len(newNetSaleslist)}個')

        return newNetSaleslist


if __name__ == '__main__':
    mergeddbextractor = MergedDbExtractor(4617)
    #print(mergeddbextractor.extract_code())
    print(mergeddbextractor.extract_public_day())
    #print(mergeddbextractor.extract_FinancialReportType())
    print(mergeddbextractor.extract_NetSales())
    #print(mergeddbextractor.extract_CompanyName())
    #print(mergeddbextractor.extract_assets())

    # mergeddbextractor.extract_NetSales()
