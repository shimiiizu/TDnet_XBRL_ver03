"""
code毎に分類されたXBRLファイルの中からBSファイルだけを抜き出し、リストを作成する
qcbsは四半期毎の決算、acbsは本決算
fs系ファイルも含む（qcfs, acfs, scfs等）
"""
import glob
import os


# ========================================
# 四半期決算（quarterly）
# ========================================
def get_qcbs_list(folder_path):
    search_string = 'qcbs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_qcfs_list(folder_path):
    search_string = 'qcfs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_qnbs_list(folder_path):
    search_string = 'qnbs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_qnfs_list(folder_path):
    search_string = 'qnfs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


# ========================================
# 本決算（annual）
# ========================================
def get_acbs_list(folder_path):
    search_string = 'acbs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_acfs_list(folder_path):
    search_string = 'acfs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_anbs_list(folder_path):
    search_string = 'anbs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_anfs_list(folder_path):
    search_string = 'anfs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


# ========================================
# 中間決算（semiannual）
# ========================================
def get_scbs_list(folder_path):
    search_string = 'scbs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_scfs_list(folder_path):
    search_string = 'scfs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_snbs_list(folder_path):
    search_string = 'snbs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


def get_snfs_list(folder_path):
    search_string = 'snfs'
    matching_files = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files


if __name__ == '__main__':
    folder_path = r"E:\Zip_files\2471"

    print('=== 本決算 ===')
    print('acbs: 本決算_連結', len(get_acbs_list(folder_path)))
    print('acfs: 本決算_連結(fs)', len(get_acfs_list(folder_path)))
    print('anbs: 本決算_単独', len(get_anbs_list(folder_path)))
    print('anfs: 本決算_単独(fs)', len(get_anfs_list(folder_path)))

    print('\n=== 四半期決算 ===')
    print('qcbs: 四半期決算_連結', len(get_qcbs_list(folder_path)))
    print('qcfs: 四半期決算_連結(fs)', len(get_qcfs_list(folder_path)))
    print('qnbs: 四半期決算_単独', len(get_qnbs_list(folder_path)))
    print('qnfs: 四半期決算_単独(fs)', len(get_qnfs_list(folder_path)))

    print('\n=== 中間決算 ===')
    print('scbs: 中間決算_連結', len(get_scbs_list(folder_path)))
    print('scfs: 中間決算_連結(fs)', len(get_scfs_list(folder_path)))
    print('snbs: 中間決算_単独', len(get_snbs_list(folder_path)))
    print('snfs: 中間決算_単独(fs)', len(get_snfs_list(folder_path)))