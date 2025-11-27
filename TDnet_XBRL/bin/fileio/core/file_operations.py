# fileio/core/file_operations.py
"""
ファイルシステムの基本操作を集約したモジュール
→ 将来的に shutil, os, send2trash などに置き換えてもここだけ修正すればOK
"""

from pathlib import Path
from typing import Optional


def delete_files(folder: Path | str, pattern: str = "*.zip") -> None:
    """指定パターンにマッチするファイルを削除（現在は委譲）"""
    from bin.fileio import files_deleter
    files_deleter.delete_zip_files(str(folder))


def delete_all_files(folder: Path | str) -> None:
    """フォルダ内の全ファイルを削除"""
    from bin.fileio import all_files_deleter
    all_files_deleter.delete_all_files(str(folder))


def create_folder(path: Path | str) -> None:
    """親フォルダ + フォルダ名で作成（例: /data/xbrl + "7203"）"""
    from bin.fileio import xbrlfile_folder_creater
    path_obj = Path(path)
    xbrlfile_folder_creater.create_xbrlfile_folder(str(path_obj.parent), path_obj.name)


def delete_folder(path: Path | str) -> None:
    """フォルダごと削除（再帰的）"""
    from bin.fileio import folder_deleter
    folder_deleter.delete_folder(str(path))


def move_zipfiles(source: Path | str, destination: Path | str) -> None:
    """zipファイルを別フォルダに移動"""
    from bin.fileio import zipfile_mover
    zipfile_mover.move_zipfiles(str(source), str(destination))


def unzip_all(folder: Path | str) -> None:
    """フォルダ内の全zipを解凍"""
    from bin.fileio import unzipper
    unzipper.unzip_all_files(str(folder))