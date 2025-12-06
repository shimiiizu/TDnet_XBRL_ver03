"""
file nameから企業コードを抜き出す

"""
import os
import re


class PlFilenameParser:
    def __init__(self, pl_file_path):
        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)

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

    def get_period_end_date(self):
        """
        期間終了日（最初の日付）を取得

        Returns:
            str: 期間終了日（例: "2016-06-30"）
                 取得できない場合は None
        """
        pattern = r'(\d{4}-\d{2}-\d{2})'
        matches = re.findall(pattern, self.file_name)
        if matches:
            return matches[0]  # 最初の日付
        else:
            print("期間終了日が見つかりませんでした。")
            return None


if __name__ == '__main__':
    pl_file_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\3679\0600000-qcpl11-tse-qcedjpfr-36790-2014-06-30-01-2014-08-12-ixbrl.htm'
    plfilenameparser = PlFilenameParser(pl_file_path)
    print('filename :', plfilenameparser.get_filename())
    print('code :', plfilenameparser.get_code())
    print('public_day :', plfilenameparser.get_public_day())
    print('period_end_date :', plfilenameparser.get_period_end_date())