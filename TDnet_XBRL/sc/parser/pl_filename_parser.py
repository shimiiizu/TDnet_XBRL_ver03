"""
file nameから企業コードや日付情報を抜き出す
ログ強化版
"""

import os
import re


class PlFilenameParser:

    def __init__(self, pl_file_path):
        print(f"[CALL] PlFilenameParser.__init__(pl_file_path={pl_file_path})")
        self.pl_file_path = pl_file_path
        self.file_name = os.path.basename(pl_file_path)
        print(f"[INFO] filename={self.file_name}")

    # ------------------------------------------------------------
    # ファイル名取得
    # ------------------------------------------------------------
    def get_filename(self):
        print("[CALL] get_filename()")
        filename = self.file_name
        print(f"[RETURN] get_filename -> {filename}")
        return filename

    # ------------------------------------------------------------
    # 企業コード取得
    # ------------------------------------------------------------
    def get_code(self):
        print("[CALL] get_code()")

        pattern = r'-([0-9]{5})-'
        match = re.search(pattern, self.file_name)

        if match:
            extracted = match.group(1)
            print(f"[INFO] 正規表現一致 code={extracted}")

            # 末尾が 0 の場合は削る（例：12340 → 1234）
            if extracted.endswith("0"):
                modified = extracted[:-1]
                print(f"[INFO] 末尾0削除 -> {modified}")
                print(f"[RETURN] get_code -> {modified}")
                return modified

            print(f"[RETURN] get_code -> {extracted}")
            return extracted

        print("[WARN] get_code -> codeが見つかりませんでした")
        return None

    # ------------------------------------------------------------
    # 公表日取得（最後の日付）
    # ------------------------------------------------------------
    def get_public_day(self):
        print("[CALL] get_public_day()")

        pattern = r'(\d{4}-\d{2}-\d{2})'
        matches = re.findall(pattern, self.file_name)

        if matches:
            extracted = matches[-1]
            print(f"[INFO] 公表日候補: {matches}")
            print(f"[RETURN] get_public_day -> {extracted}")
            return extracted

        print("[WARN] get_public_day -> 公表日が見つかりませんでした")
        return None

    # ------------------------------------------------------------
    # 期間終了日取得（最初の日付）
    # ------------------------------------------------------------
    def get_period_end_date(self):
        print("[CALL] get_period_end_date()")

        pattern = r'(\d{4}-\d{2}-\d{2})'
        matches = re.findall(pattern, self.file_name)

        if matches:
            extracted = matches[0]
            print(f"[INFO] 期間終了日候補: {matches}")
            print(f"[RETURN] get_period_end_date -> {extracted}")
            return extracted

        print("[WARN] get_period_end_date -> 期間終了日が見つかりませんでした")
        return None


# ------------------------------------------------------------
# テストコード
# ------------------------------------------------------------
if __name__ == '__main__':
    pl_file_path = r'E:\Zip_files\4612\0103010-acss03-tse-acediffr-46120-2024-12-31-01-2025-02-14-ixbrl.htm'
    parser = PlFilenameParser(pl_file_path)

    print('filename :', parser.get_filename())
    print('code :', parser.get_code())
    print('public_day :', parser.get_public_day())
    print('period_end_date :', parser.get_period_end_date())
