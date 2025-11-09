"""
★以下のプログラムを統合するプログラム★
✅csvファイルを読み込む Read_csv
✅Zipファイルを削除　Delete_zips
✅東証上場会社情報サービスからZipファイルをダウンロード　Zip_Downloader
✅Zipを保管するためのフォルダを作成する Create_Folder
✅Zipファイルを移動　Move_zip
✅Zipファイルを解凍 Unzip
☞展開したファイルをParse（BS：完、PL：未）Parse_xbrl_common/Parse_xbrl_IFRS/Parse_xbrl_Japan_GAAP
☞抽出した情報をデータベースに保管（BS：完、PL：未）bs_db_inserter.py
✅データベースから情報を読み出し bs_db_extractor.py
✅グラフを作成する　bs_graph_creator.py
-(Webに)情報を表示 bs_viewer.py
"""
import os
import xbrlfile_folder_creater
import zipfile_mover
import files_deleter
import all_files_deleter
import folder_deleter
import unzipper
import bs_filelist_maker  # 自作モジュール： BSのXBRLファイルパスのリストを作成する
import pl_filelist_maker  # 自作モジュール： PLのXBRLファイルパスのリストを作成する
from bs_recorder import BsRecoder
from pl_recorder import PlRecoder
import csv_reader
import zipfile_downloader
from bs_db_inserter import BsDBInserter
from pl_db_inserter import PlDBInserter


# 企業コード設定
codes = [9504]
#codes = csv_reader.read_csv('../config/code_list.csv') # ★企業コードはここで設定

# ダウンロードフォルダのパス（自動的にユーザーのDownloadsフォルダを取得）
source_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
xbrlfile_folder = r"E:\Zip_files"  # Zipファイル保管先フォルダのパス

# codeのリストを表示
print(f'企業コード：{codes}')
print(f'ダウンロードフォルダ：{source_folder}')

for code in codes:
#for code in codes[10:]:
    print(f'-----{code}の開始-----')

    # ダウンロードフォルダ内のzipファイルを削除
    print(f'ダウンロードフォルダ内のzipファイルを削除')
    files_deleter.delete_zip_files(source_folder)

    # zipファイル保管先のパスを作成
    new_folder_path = os.path.join(xbrlfile_folder, str(code))

    # 東証上場会社情報サービスからZipファイルをダウンロードする
    print(f'{code}のダウンロード')
    zipfile_downloader.zip_download(code)  # ここに時間がかかる。

    # code毎にzipファイルを保管するためのフォルダを作成する
    print(f'{code}のフォルダを作成')
    xbrlfile_folder_creater.create_xbrlfile_folder(xbrlfile_folder, code)

    # ダウンロードしたzipファイルをcode毎のフォルダに移動する
    print(f'{code}のzipファイルをフォルダに移動')
    zipfile_mover.move_zipfiles(source_folder, new_folder_path)

    # zipファイルを解凍する
    print(f'{code}のzipファイルを解凍')
    unzipper.unzip_all_files(new_folder_path)

    # code毎のフォルダ内のファイルを削除
    print(f'{code}のフォルダ内の不要なファイルとフォルダを削除')
    all_files_deleter.delete_all_files(new_folder_path)
    folder_deleter.delete_folder(os.path.join(new_folder_path, r'XBRLData'))

    # ■■■BSのレコードを作成する。■■■
    print(f'{code}のフォルダ内のBSファイルのレコードを作成')

    # 本決算_連結のリストの作成
    print('本決算_連結のリストの作成')
    ac_bsfile_list = bs_filelist_maker.get_acbs_list(new_folder_path)

    for ac_bsfile in ac_bsfile_list:    # リストに対してループ処理
        bs_recorder = BsRecoder(ac_bsfile)
        bs_recorder.record_bs()
        bsdbinserter = BsDBInserter(ac_bsfile)
        bsdbinserter.insert_to_bs_db()

    if len(ac_bsfile_list) == 0:  # 連結決算がない場合には単独決算のリストを作成
        # 本決算_単独のリストの作成
        print('本決算_単独のリストの作成')
        an_bsfile_list = bs_filelist_maker.get_anbs_list(new_folder_path)

        for an_bsfile in an_bsfile_list:    # リストに対してループ処理
            bs_recorder = BsRecoder(an_bsfile)
            bs_recorder.record_bs()
            bsdbinserter = BsDBInserter(an_bsfile)
            bsdbinserter.insert_to_bs_db()

    # 四半期決算_連結のBSファイルのリスト
    print('四半期決算_連結のリストの作成')
    qc_bsfile_list = bs_filelist_maker.get_qcbs_list(new_folder_path)

    for qc_bsfile in qc_bsfile_list:    # リストに対してループ処理
        bs_recorder = BsRecoder(qc_bsfile)
        bs_recorder.record_bs()
        bsdbinserter = BsDBInserter(qc_bsfile)
        bsdbinserter.insert_to_bs_db()

    if len(qc_bsfile_list) == 0:  # 連結決算がない場合には単独決算のリストを作成
        # 四半期決算_単独のBSファイルのリスト
        print('四半期決算_単独のリストの作成')
        qn_bsfile_list = bs_filelist_maker.get_qnbs_list(new_folder_path)

        for qn_bsfile in qn_bsfile_list:    # リストに対してループ処理
            bs_recorder = BsRecoder(qn_bsfile)
            bs_recorder.record_bs()
            bsdbinserter = BsDBInserter(qn_bsfile)
            bsdbinserter.insert_to_bs_db()

    # 中間期決算_連結のBSファイルのリスト
    print('中間期決算_連結のリストの作成')
    sc_bsfile_list = bs_filelist_maker.get_scbs_list(new_folder_path)

    for sc_bsfile in sc_bsfile_list:    # リストに対してループ処理
        bs_recorder = BsRecoder(sc_bsfile)
        bs_recorder.record_bs()
        bsdbinserter = BsDBInserter(sc_bsfile)
        bsdbinserter.insert_to_bs_db()

    # 中間期決算_単独のBSファイルのリスト
    print('中間期決算_単独のリストの作成')
    sn_bsfile_list = bs_filelist_maker.get_snbs_list(new_folder_path)

    for sn_bsfile in sn_bsfile_list:  # リストに対してループ処理
        bs_recorder = BsRecoder(sn_bsfile)
        bs_recorder.record_bs()
        bsdbinserter = BsDBInserter(sn_bsfile)
        bsdbinserter.insert_to_bs_db()

# ■■■PLのレコードを作成する。■■■
print(f'{code}のフォルダ内のPLファイルのレコードを作成')

# 本決算_連結のリストの作成
print('本決算_連結のPLリストの作成')
ac_plfile_list = pl_filelist_maker.get_acpl_list(new_folder_path)

for ac_plfile in ac_plfile_list:
    pl_recorder = PlRecoder(ac_plfile)
    pl_recorder.record_pl()
    pldbinserter = PlDBInserter(ac_plfile)
    pldbinserter.insert_to_pl_db()

if len(ac_plfile_list) == 0:  # 連結決算がない場合には単独決算のリストを作成
    # 本決算_単独のリストの作成
    print('本決算_単独のPLリストの作成')
    an_plfile_list = pl_filelist_maker.get_anpl_list(new_folder_path)

    for an_plfile in an_plfile_list:
        pl_recorder = PlRecoder(an_plfile)
        pl_recorder.record_pl()
        pldbinserter = PlDBInserter(an_plfile)
        pldbinserter.insert_to_pl_db()

# 四半期決算_連結のPLファイルのリスト
print('四半期決算_連結のPLリストの作成')
qc_plfile_list = pl_filelist_maker.get_qcpl_list(new_folder_path)

for qc_plfile in qc_plfile_list:
    pl_recorder = PlRecoder(qc_plfile)
    pl_recorder.record_pl()
    pldbinserter = PlDBInserter(qc_plfile)
    pldbinserter.insert_to_pl_db()

if len(qc_plfile_list) == 0:  # 連結決算がない場合には単独決算のリストを作成
    # 四半期決算_単独のPLファイルのリスト
    print('四半期決算_単独のPLリストの作成')
    qn_plfile_list = pl_filelist_maker.get_qnpl_list(new_folder_path)

    for qn_plfile in qn_plfile_list:
        pl_recorder = PlRecoder(qn_plfile)
        pl_recorder.record_pl()
        pldbinserter = PlDBInserter(qn_plfile)
        pldbinserter.insert_to_pl_db()

# 中間期決算_連結のPLファイルのリスト
print('中間期決算_連結のPLリストの作成')
sc_plfile_list = pl_filelist_maker.get_scpl_list(new_folder_path)

for sc_plfile in sc_plfile_list:
    pl_recorder = PlRecoder(sc_plfile)
    pl_recorder.record_pl()
    pldbinserter = PlDBInserter(sc_plfile)
    pldbinserter.insert_to_pl_db()

# 中間期決算_単独のPLファイルのリスト
print('中間期決算_単独のPLリストの作成')
sn_plfile_list = pl_filelist_maker.get_snpl_list(new_folder_path)

for sn_plfile in sn_plfile_list:
    pl_recorder = PlRecoder(sn_plfile)
    pl_recorder.record_pl()
    pldbinserter = PlDBInserter(sn_plfile)
    pldbinserter.insert_to_pl_db()

print('\n全ての処理が完了しました！')