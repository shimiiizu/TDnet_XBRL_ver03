# fileio/file_manager.py
from pathlib import Path
from typing import List, Literal

from .core.basic_operations import (
    delete_files, delete_all_files, create_folder,
    delete_folder, move_zipfiles, unzip_all
)
from .core.statement_finder import get_statement_files

StatementType = Literal["bs", "pl"]
PeriodType = Literal["annual", "quarterly", "semiannual"]
ConsolidationType = Literal["consolidated", "standalone"]


class FileManager:
    """ユーザーが使う唯一のエントリーポイント"""

    # 基本操作はそのまま公開（必要ならラップしてもOK）
    delete_files = staticmethod(delete_files)
    delete_all_files = staticmethod(delete_all_files)
    create_folder = staticmethod(create_folder)
    delete_folder = staticmethod(delete_folder)
    move_zipfiles = staticmethod(move_zipfiles)
    unzip_all = staticmethod(unzip_all)

    # 財務諸表取得（型安全＋超シンプル）
    get_statement_files = staticmethod(get_statement_files)