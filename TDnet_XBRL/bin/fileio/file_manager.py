# fileio/file_manager.py

from pathlib import Path
from typing import List


class FileManager:
    """
    Zipファイル削除、移動、解凍など
    XBRL処理で必要な「ファイル操作」を抽象化したユーティリティクラス。
    各処理は外部モジュール(あなたが作成したスクリプト群)に委譲する。
    """

    # ===========================================================================
    # 基本ファイル操作
    # ===========================================================================

    @staticmethod
    def delete_files(folder: Path, pattern: str = "*.zip"):
        """
        指定フォルダ内のファイル削除（zipなど）
        """
        from bin.fileio import files_deleter
        files_deleter.delete_zip_files(str(folder))

    @staticmethod
    def delete_all_files(folder: Path):
        """
        指定フォルダ内の全ファイル削除
        """
        from bin.fileio import all_files_deleter
        all_files_deleter.delete_all_files(str(folder))

    @staticmethod
    def create_folder(path: Path):
        """
        フォルダ作成
        """
        from bin.fileio import xbrlfile_folder_creater
        xbrlfile_folder_creater.create_xbrlfile_folder(
            str(path.parent),
            path.name
        )

    @staticmethod
    def delete_folder(path: Path):
        """
        フォルダ削除
        """
        from bin.fileio import folder_deleter
        folder_deleter.delete_folder(str(path))

    @staticmethod
    def move_zipfiles(source: Path, destination: Path):
        """
        Zipファイルを source → destination に移動
        """
        from bin.fileio import zipfile_mover
        zipfile_mover.move_zipfiles(str(source), str(destination))

    @staticmethod
    def unzip_all(folder: Path):
        """
        指定ディレクトリ内のすべてのZipを解凍
        """
        from bin.fileio import unzipper
        unzipper.unzip_all_files(str(folder))

    # ===========================================================================
    # 財務諸表ファイル（BS/PL）の取得
    # ===========================================================================

    @staticmethod
    def get_statement_files(
        folder: Path,
        statement_type: str,
        period_type: str,
        consolidation: str
    ) -> List[str]:
        """
        BS/PL のファイルリストを取得する統合関数。

        Args:
            folder: 企業フォルダ
            statement_type: 'bs' or 'pl'
            period_type: 'annual' / 'quarterly' / 'semiannual'
            consolidation: 'consolidated' or 'standalone'
        """

        from bin.fileio import bs_filelist_maker
        from bin.fileio import pl_filelist_maker

        # annual → a、quarterly → q、semiannual → s
        period_code = {
            'annual': 'a',
            'quarterly': 'q',
            'semiannual': 's'
        }[period_type]

        # consolidated → c、standalone → n
        consolidation_code = {
            'consolidated': 'c',
            'standalone': 'n'
        }[consolidation]

        # 組み合わせ例：ac / qc / sn
        code = f"{period_code}{consolidation_code}"

        if statement_type == 'bs':
            method_name = f"get_{code}bs_list"
            return getattr(bs_filelist_maker, method_name)(str(folder))

        else:  # PL
            method_name = f"get_{code}pl_list"
            return getattr(pl_filelist_maker, method_name)(str(folder))
