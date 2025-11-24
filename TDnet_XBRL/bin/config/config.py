# config/config.py

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from bin.config import csv_reader


@dataclass
class Config:
    """
    XBRL 処理システム全体で使用する設定値を保持するクラス。
    - 企業コード一覧
    - ダウンロードフォルダ
    - 処理用のXBRLファイル保存フォルダ
    """

    codes: List[int]
    source_folder: Path
    xbrlfile_folder: Path

    # --------------------------------------------------------
    # デフォルト設定で初期化
    # --------------------------------------------------------
    @classmethod
    def from_defaults(cls):
        """
        プログラム直書きのデフォルト設定で初期化する。
        CSV から読み込む場合は from_csv() を使用する。
        """
        return cls(
            codes=[1301],  # デフォルト企業コード（任意）
            # CSVを使いたいなら以下に切り替え可能：
            # codes=csv_reader.read_csv('./config/code_list.csv'),

            source_folder=Path.home() / 'Downloads',       # ダウンロードフォルダ
            xbrlfile_folder=Path(r"E:\Zip_files")          # ZIP格納フォルダ
        )

    # --------------------------------------------------------
    # CSV ファイルから企業コードを読み込むバージョン
    # --------------------------------------------------------
    @classmethod
    def from_csv(cls, csv_path: Path, xbrlfile_folder: Optional[Path] = None):
        """
        CSV ファイルから企業コードを読み込んで設定を作成する。

        Args:
            csv_path (Path): コードリストCSVファイル
            xbrlfile_folder (Path, optional): ZIP保存フォルダ
        """
        codes = csv_reader.read_csv(str(csv_path))

        return cls(
            codes=codes,
            source_folder=Path.home() / "Downloads",
            xbrlfile_folder=xbrlfile_folder or Path(r"E:\Zip_files")
        )

    # --------------------------------------------------------
    # 型チェック／ディレクトリ存在チェック（必要なら拡張可）
    # --------------------------------------------------------
    def validate(self):
        """設定値が正しいかチェック（必要なら利用）"""
        if not isinstance(self.codes, list):
            raise ValueError("codes must be a list of integers")

        if not self.source_folder.exists():
            print(f"Warning: source_folder が存在しません: {self.source_folder}")

        if not self.xbrlfile_folder.parent.exists():
            print(f"Warning: xbrlfile_folder の親フォルダが存在しません: {self.xbrlfile_folder.parent}")
