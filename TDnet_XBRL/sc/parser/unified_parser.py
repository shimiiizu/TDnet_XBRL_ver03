# parser/unified_parser.py

from pathlib import Path
from sc.parser.base_parser import XBRLParser


class UnifiedXBRLParser(XBRLParser):
    """
    BS / PL の両方に対応した統合 XBRL パーサー。
    ファイル名から BS/PL を自動判定し、
    正しい recorder / inserter を呼び出す責務を持つ。
    """

    def parse(self, file_path: str):
        """
        XBRL ファイルをパース（メモリ上にデータ抽出）
        """
        statement_type = self._detect_statement_type(file_path)

        if statement_type == "bs":
            self._parse_bs(file_path)
        elif statement_type == "pl":
            self._parse_pl(file_path)
        else:
            raise ValueError(f"Unknown statement type: {file_path}")

    def save_to_db(self, file_path: str):
        """
        パース済みデータを DB に保存
        """
        statement_type = self._detect_statement_type(file_path)

        if statement_type == "bs":
            self._save_bs_to_db(file_path)
        elif statement_type == "pl":
            self._save_pl_to_db(file_path)

    # ===========================================================================
    # 内部ロジック
    # ===========================================================================

    @staticmethod
    def _detect_statement_type(file_path: str) -> str:
        """
        ファイル名から BS/PL を判別する。
        bs系（qcbs, acbs等）とfs系（qcfs, acfs等）はBSとして扱う。
        pc系（qcpc, acpc等）はPLとして扱う。
        """
        name = Path(file_path).name.lower()

        # BS系ファイル: 'bs' または 'fs' が含まれる
        if "bs" in name or "fs" in name:
            return "bs"

        # PL系ファイル: 'pl' または 'pc' が含まれる
        if "pl" in name or "pc" in name:
            return "pl"

        return "unknown"

    # -------------------------------
    # BS
    # -------------------------------

    def _parse_bs(self, file_path: str):
        """
        BS（貸借対照表）をパース
        """
        from sc.printer.bs_recorder import BsRecoder
        recorder = BsRecoder(file_path)
        recorder.record_bs()

    def _save_bs_to_db(self, file_path: str):
        """
        BS の抽出データを DB 保存
        """
        from sc.inserter.bs_db_inserter import BsDBInserter
        inserter = BsDBInserter(file_path)
        inserter.insert_to_bs_db()

    # -------------------------------
    # PL
    # -------------------------------

    def _parse_pl(self, file_path: str):
        """
        PL（損益計算書）をパース
        """
        from sc.printer.pl_recorder import PlRecoder
        recorder = PlRecoder(file_path)
        recorder.record_pl()

    def _save_pl_to_db(self, file_path: str):
        """
        PL の抽出データを DB 保存
        """
        from sc.inserter.pl_db_inserter import PlDBInserter
        inserter = PlDBInserter(file_path)
        inserter.insert_to_pl_db()

if __name__ == "__main__":
    # テストコード
    parser = UnifiedXBRLParser()

    test_files = [
        #r"E:\Zip_files\1301\0300000-acbs01-tse-acedjpfr-13010-2016-03-31-01-2016-05-09-ixbrl.htm"  # BSファイル
        r"E:\Zip_files\4612\0102010-acbs03-tse-acediffr-46120-2024-12-31-01-2025-02-14-ixbrl.htm"  # BSファイル
    ]

    for file in test_files:
        print(f"Parsing file: {file}")
        parser.parse(file)
        parser.save_to_db(file)
        print(f"Finished processing file: {file}\n")
