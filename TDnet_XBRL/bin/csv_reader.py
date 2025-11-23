"""
csvファイルを読み込み、リスト化するプログラム
"""
import pandas as pd


def read_csv(file_path):
    df = pd.read_csv(file_path, header=0)
    code_list = df['code'].tolist()
    return code_list


if __name__ == '__main__':
    file_path = '../config/code_list.csv'
    print(read_csv(file_path))
