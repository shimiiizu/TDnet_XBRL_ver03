"""
指定されたフォルダ内のすべてのZipファイルを削除する

"""

import os


def delete_zip_files(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.lower().endswith(".zip"):
            os.remove(item_path)
            print(f"ファイル '{item_path}' を削除しました。")


def delete_xml_files(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.lower().endswith(".xml"):
            os.remove(item_path)
            print(f"ファイル '{item_path}' を削除しました。")


def delete_xsd_files(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.lower().endswith(".xsd"):
            os.remove(item_path)
            print(f"ファイル '{item_path}' を削除しました。")


def delete_txt_files(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.lower().endswith(".txt"):
            os.remove(item_path)
            print(f"ファイル '{item_path}' を削除しました。")


def delete_htm_files(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and item.lower().endswith("qualitative.htm"):
            os.remove(item_path)
            print(f"ファイル '{item_path}' を削除しました。")


if __name__ == "__main__":
    # 例としてフォルダパスを指定
    #folder_path = r"C:\Users\SONY\Downloads"
    folder_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\5232"
    delete_htm_files(folder_path)
