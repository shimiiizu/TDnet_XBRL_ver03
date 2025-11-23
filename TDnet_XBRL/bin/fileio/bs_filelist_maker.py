"""
code毎に分類されたXBRLファイルの中からBSファイルだけを抜き出し、リストを作成する
qcbsは四半期毎の決算、acbsは本決算
"""
import glob
import os


def get_qcbs_list(folder_path):
    search_string = 'qcbs'  # 検索したい文字列を指定
    matching_files_qcbs = glob.glob(f'{folder_path}/*{search_string}*')  # 特定の文字列が含まれるファイルの一覧を取得
    return matching_files_qcbs


def get_qnbs_list(folder_path):
    search_string = 'qnbs'  # 検索したい文字列を指定
    matching_files_qnbs = glob.glob(f'{folder_path}/*{search_string}*') # 特定の文字列が含まれるファイルの一覧を取得
    return matching_files_qnbs


def get_acbs_list(folder_path):
    search_string = 'acbs'  # 検索したい文字列を指定
    matching_files_acbs = glob.glob(f'{folder_path}/*{search_string}*') # 特定の文字列が含まれるファイルの一覧を取得
    return matching_files_acbs


def get_anbs_list(folder_path):
    search_string = 'anbs'  # 検索したい文字列を指定
    matching_files_acbs = glob.glob(f'{folder_path}/*{search_string}*')  # 特定の文字列が含まれるファイルの一覧を取得
    return matching_files_acbs


def get_scbs_list(folder_path):
    search_string = 'scbs'  # 検索したい文字列を指定
    matching_files_scbs = glob.glob(f'{folder_path}/*{search_string}*')  # 特定の文字列が含まれるファイルの一覧を取得
    return matching_files_scbs


def get_snbs_list(folder_path):
    search_string = 'snbs'  # 検索したい文字列を指定
    matching_files_snbs = glob.glob(f'{folder_path}/*{search_string}*') # 特定の文字列が含まれるファイルの一覧を取得
    return matching_files_snbs


if __name__ == '__main__':
    #folder_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\2780"  # フォルダのパスを指定
    folder_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\7003"
    print('acbs: 本決算_連結', len(get_acbs_list(folder_path)))
    print('anbs: 本決算_単独', len(get_anbs_list(folder_path)))
    print('qcbs　四半期決算_連結:', len(get_qcbs_list(folder_path)))
    print('qnbs　四半期決算_単独:', len(get_qnbs_list(folder_path)))
    print('scbs: 中間決算_連結', len(get_scbs_list(folder_path)))
    print('snbs: 中間決算_単独', len(get_snbs_list(folder_path)))