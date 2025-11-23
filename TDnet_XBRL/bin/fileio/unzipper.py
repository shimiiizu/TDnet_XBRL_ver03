import os
import zipfile
import shutil


def unzip_all_files(folder_path):
    """
    指定されたフォルダ内のすべてのzipファイルを解凍する関数
    """

    for zip_file in os.listdir(folder_path):
        zipfile_path = os.path.join(folder_path, zip_file)

        # zipファイルに対して処理を実行する
        if os.path.isfile(zipfile_path) and zip_file.lower().endswith(".zip"):
            with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
                # zipを解凍
                zip_ref.extractall(folder_path)
                print(f"ファイル '{zip}' を解凍しました。")

                # 解凍後のファイルを移動(Attachmentに入っているものだけを移動。Summaryはまだ対応していない)

                if os.path.exists(os.path.join(folder_path, r'XBRLData\Attachment')) and os.path.isdir(os.path.join(folder_path, r'XBRLData\Attachment')):
                    for file in os.listdir(os.path.join(folder_path, r'XBRLData\Attachment')):
                        src_path = os.path.join(folder_path, r'XBRLData\Attachment', file)
                        dst_path = os.path.join(folder_path, file)
                        shutil.move(src_path, dst_path)
                        print(f'{file} を {dst_path} に移動しました。')
                else:
                    pass

        else:
            pass


if __name__ == "__main__":
    #xbrl_file_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\5233"
    xbrl_file_path = r"C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\6988"
    unzip_all_files(xbrl_file_path)

