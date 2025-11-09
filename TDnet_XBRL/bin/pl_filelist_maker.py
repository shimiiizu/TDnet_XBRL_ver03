"""
code毎に分類されたXBRLファイルの中からPLファイルだけを抜き出し、リストを作成する
qcplは四半期毎の決算、acplは本決算、scplは中間期決算
"""
import glob


def get_acpl_list(folder_path):
    """本決算_連結のPLファイルリストを取得"""
    search_string = 'acpl'
    matching_files_acpl = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files_acpl


def get_anpl_list(folder_path):
    """本決算_単独のPLファイルリストを取得"""
    search_string = 'anpl'
    matching_files_anpl = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files_anpl


def get_qcpl_list(folder_path):
    """四半期決算_連結のPLファイルリストを取得"""
    search_string = 'qcpl'
    matching_files_qcpl = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files_qcpl


def get_qnpl_list(folder_path):
    """四半期決算_単独のPLファイルリストを取得"""
    search_string = 'qnpl'
    matching_files_qnpl = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files_qnpl


def get_scpl_list(folder_path):
    """中間期決算_連結のPLファイルリストを取得"""
    search_string = 'scpl'
    matching_files_scpl = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files_scpl


def get_snpl_list(folder_path):
    """中間期決算_単独のPLファイルリストを取得"""
    search_string = 'snpl'
    matching_files_snpl = glob.glob(f'{folder_path}/*{search_string}*')
    return matching_files_snpl


if __name__ == '__main__':
    # テスト用フォルダパス（環境に合わせて変更してください）
    folder_path = r"E:\Zip_files\9504"

    print(f'フォルダ: {folder_path}\n')
    print('=' * 60)

    # 本決算_連結
    acpl_list = get_acpl_list(folder_path)
    print(f'\n【本決算_連結】 acpl')
    for file in acpl_list:
        print(f'  {file}')
    print(f'合計: {len(acpl_list)}件')

    # 本決算_単独
    anpl_list = get_anpl_list(folder_path)
    print(f'\n【本決算_単独】 anpl')
    for file in anpl_list:
        print(f'  {file}')
    print(f'合計: {len(anpl_list)}件')

    # 四半期_連結
    qcpl_list = get_qcpl_list(folder_path)
    print(f'\n【四半期決算_連結】 qcpl')
    for file in qcpl_list:
        print(f'  {file}')
    print(f'合計: {len(qcpl_list)}件')

    # 四半期_単独
    qnpl_list = get_qnpl_list(folder_path)
    print(f'\n【四半期決算_単独】 qnpl')
    for file in qnpl_list:
        print(f'  {file}')
    print(f'合計: {len(qnpl_list)}件')

    # 中間期_連結
    scpl_list = get_scpl_list(folder_path)
    print(f'\n【中間期決算_連結】 scpl')
    for file in scpl_list:
        print(f'  {file}')
    print(f'合計: {len(scpl_list)}件')

    # 中間期_単独
    snpl_list = get_snpl_list(folder_path)
    print(f'\n【中間期決算_単独】 snpl')
    for file in snpl_list:
        print(f'  {file}')
    print(f'合計: {len(snpl_list)}件')

    print('\n' + '=' * 60)
    print(f'全PLファイル合計: {len(acpl_list) + len(anpl_list) + len(qcpl_list) + len(qnpl_list) + len(scpl_list) + len(snpl_list)}件')