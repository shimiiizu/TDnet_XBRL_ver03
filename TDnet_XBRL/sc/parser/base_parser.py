# parser/base_parser.py

from abc import ABC, abstractmethod


class XBRLParser(ABC):
    """
    XBRL パーサーの抽象基底クラス。

    BS / PL / CF など、財務諸表ごとに異なる処理を行うパーサーの
    インターフェース（共通仕様）を定義する。
    """

    @abstractmethod
    def parse(self, file_path: str):
        """
        XBRL ファイルを読み取り、必要なデータを抽出する処理。
        下位クラス（UnifiedXBRLParser）が実装する。

        Args:
            file_path (str): XBRL ファイルへのパス
        """
        pass

    @abstractmethod
    def save_to_db(self, file_path: str):
        """
        parse() で抽出したデータをデータベースへ保存する処理。
        下位クラスが実装する。

        Args:
            file_path (str): XBRL ファイルへのパス
        """
        pass
