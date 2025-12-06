"""
file nameから情報を抜き出す
情報：企業コード/公表日

"""
import os
import re


class BsFilenameParser:
    def __init__(self, bs_file_path):
        self.bs_file_path = bs_file_path
        self.file_name = os.path.basename(bs_file_path)

    def get_filename(self):
        filename = self.file_name
        return filename

    def get_code(self):
        pattern = r'-([0-9]{5})-'                   # 正規表現パターンを定義
        match = re.search(pattern, self.file_name)  # パターンに一致する部分を検索
        if match:
            extracted_part = match.group(1)

            if extracted_part.endswith('0'):
                extracted_part = extracted_part[:-1]
                return extracted_part

            else:
                return extracted_part
        else:
            print("codeが見つかりませんでした。")

    def get_public_day(self):
        pattern = r'(\d{4}-\d{2}-\d{2})'
        matches = re.findall(pattern, self.file_name)
        if matches:
            extracted_date = matches[-1]  # 最後の一致を取得
            return extracted_date
        else:
            print("公表日が見つかりませんでした。")


if __name__ == '__main__':
    bs_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\2780\0101010-acbs01-tse-acedjpfr-27800-2014-03-31-02-2014-10-10-ixbrl.htm'
    bsfilenameparser = BsFilenameParser(bs_file_path)
    bsfilenameparser.get_code()
    bsfilenameparser.get_public_day()
    print(f'企業コードは{bsfilenameparser.get_code()}です。')
    print(f'公表日は{bsfilenameparser.get_public_day()}です。')



