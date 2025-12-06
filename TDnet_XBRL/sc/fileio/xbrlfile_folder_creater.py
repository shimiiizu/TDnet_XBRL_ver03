import os


def create_xbrlfile_folder(xbrlfile_folder, code):
    new_folder_path = os.path.join(xbrlfile_folder, str(code))
    if not os.path.exists(new_folder_path):
        # code毎にzipファイルを保管するためのフォルダを作成する
        os.makedirs(os.path.join(new_folder_path))
        print(f"フォルダ '{new_folder_path}' を作成しました。")

    else:
        print(f"フォルダ '{new_folder_path}' は既に存在しています。")


if __name__ == "__main__":
    xbrlfile_folder = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files"
    code = 5233
    create_xbrlfile_folder(xbrlfile_folder, code)