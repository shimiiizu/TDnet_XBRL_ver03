"""
指定されたフォルダを削除する
"""

import shutil


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"フォルダを削除しました。")

    except:
        print(f"フォルダを削除しませんでした。")


if __name__ == "__main__":
    # 例としてフォルダパスを指定
    folder_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\5233\XBRLData"
    delete_folder(folder_path)
