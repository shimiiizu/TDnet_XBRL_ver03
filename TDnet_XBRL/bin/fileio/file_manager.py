# fileio/file_manager.py

"""
XBRL処理パイプライン向け ファイル操作ファサード

このモジュールは、XBRL取得・解凍・分類・解析の全工程で必要となる
ファイルシステム操作を一元的に提供します。

特徴
-----
- 外部からは FileManager クラスだけをインポートすればすべての機能が利用可能
- 基本操作（解凍・移動・削除）と財務諸表ファイル検索を同一APIで提供
- 引数には Literal 型を使用し、スペルミスによるバグを静的解析段階で防止
- 実際の処理は core/ サブパッケージに分離しており、このファイル自体は薄く保たれている
- 将来的に shutil や send2trash などに置き換える場合も、このファイルは一切変更不要
"""

from pathlib import Path
from typing import List, Literal

from .core.basic_operations import (
    delete_files, delete_all_files, create_folder,
    delete_folder, move_zipfiles, unzip_all
)
from .core.financial_report_loader import get_statement_files

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