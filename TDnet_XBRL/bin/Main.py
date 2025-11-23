"""
XBRL財務データ処理システム
東証上場会社の財務データ（BS・PL）をダウンロード、解析、データベースに保存
"""
import os
from pathlib import Path
from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod
import csv_reader


@dataclass
class Config:
    """設定情報を管理するクラス"""
    codes: List[int]
    source_folder: Path
    xbrlfile_folder: Path

    @classmethod
    def from_defaults(cls):
        """デフォルト設定で初期化"""
        return cls(
            codes=[2471],  # ここで企業コードを設定
            # codes=csv_reader.read_csv('../config/code_list.csv'),  # CSVから読み込む場合
            source_folder=Path.home() / 'Downloads',
            xbrlfile_folder=Path(r"E:\Zip_files")
        )


class FileManager:
    """ファイル・フォルダ操作を統合管理するクラス"""

    @staticmethod
    def delete_files(folder: Path, pattern: str = "*.zip"):
        """指定パターンのファイルを削除"""
        import files_deleter
        files_deleter.delete_zip_files(str(folder))

    @staticmethod
    def delete_all_files(folder: Path):
        """フォルダ内の全ファイルを削除"""
        import all_files_deleter
        all_files_deleter.delete_all_files(str(folder))

    @staticmethod
    def create_folder(path: Path):
        """フォルダを作成"""
        import xbrlfile_folder_creater
        xbrlfile_folder_creater.create_xbrlfile_folder(str(path.parent), path.name)

    @staticmethod
    def delete_folder(path: Path):
        """フォルダを削除"""
        import folder_deleter
        folder_deleter.delete_folder(str(path))

    @staticmethod
    def move_zipfiles(source: Path, destination: Path):
        """Zipファイルを移動"""
        import zipfile_mover
        zipfile_mover.move_zipfiles(str(source), str(destination))

    @staticmethod
    def unzip_all(folder: Path):
        """フォルダ内の全Zipファイルを解凍"""
        import unzipper
        unzipper.unzip_all_files(str(folder))

    @staticmethod
    def get_statement_files(folder: Path, statement_type: str, period_type: str,
                           consolidation: str) -> List[str]:
        """
        財務諸表ファイルのリストを取得

        Args:
            folder: 検索対象フォルダ
            statement_type: 'bs' or 'pl'
            period_type: 'annual' (本決算), 'quarterly' (四半期), 'semiannual' (中間期)
            consolidation: 'consolidated' (連結) or 'standalone' (単独)
        """
        import bs_filelist_maker
        import pl_filelist_maker

        # period_typeとconsolidationからメソッド名を生成
        # annual + consolidated -> 'ac', quarterly + consolidated -> 'qc', etc.
        period_code = {
            'annual': 'a',
            'quarterly': 'q',
            'semiannual': 's'
        }[period_type]

        consolidation_code = {
            'consolidated': 'c',
            'standalone': 'n'
        }[consolidation]

        code = f"{period_code}{consolidation_code}"

        if statement_type == 'bs':
            method_name = f"get_{code}bs_list"
            return getattr(bs_filelist_maker, method_name)(str(folder))
        else:  # pl
            method_name = f"get_{code}pl_list"
            return getattr(pl_filelist_maker, method_name)(str(folder))


class XBRLParser(ABC):
    """XBRL財務諸表パーサーの抽象基底クラス"""

    @abstractmethod
    def parse(self, file_path: str):
        """XBRLファイルをパースしてデータを抽出"""
        pass

    @abstractmethod
    def save_to_db(self, file_path: str):
        """抽出したデータをデータベースに保存"""
        pass


class UnifiedXBRLParser(XBRLParser):
    """
    統合XBRLパーサー
    BS/PLおよび全会計基準（Japan GAAP, IFRS, Common）に対応
    """

    def parse(self, file_path: str):
        """
        XBRLファイルをパースして財務データを抽出
        ファイル名から自動的にBS/PLを判定し、適切なパーサーを使用
        """
        file_name = Path(file_path).name.lower()

        if 'bs' in file_name or 'balancesheet' in file_name:
            return self._parse_bs(file_path)
        elif 'pl' in file_name or 'profitloss' in file_name:
            return self._parse_pl(file_path)
        else:
            raise ValueError(f"Unknown statement type in file: {file_path}")

    def save_to_db(self, file_path: str):
        """抽出したデータをDBに保存"""
        file_name = Path(file_path).name.lower()

        if 'bs' in file_name or 'balancesheet' in file_name:
            self._save_bs_to_db(file_path)
        elif 'pl' in file_name or 'profitloss' in file_name:
            self._save_pl_to_db(file_path)

    def _parse_bs(self, file_path: str):
        """BS（貸借対照表）をパース"""
        from bs_recorder import BsRecoder
        recorder = BsRecoder(file_path)
        recorder.record_bs()

    def _parse_pl(self, file_path: str):
        """PL（損益計算書）をパース"""
        from pl_recorder import PlRecoder
        recorder = PlRecoder(file_path)
        recorder.record_pl()

    def _save_bs_to_db(self, file_path: str):
        """BSデータをDBに保存"""
        from bs_db_inserter import BsDBInserter
        inserter = BsDBInserter(file_path)
        inserter.insert_to_bs_db()

    def _save_pl_to_db(self, file_path: str):
        """PLデータをDBに保存"""
        from pl_db_inserter import PlDBInserter
        inserter = PlDBInserter(file_path)
        inserter.insert_to_pl_db()


class CompanyDataProcessor:
    """企業データの処理を統括するクラス"""

    def __init__(self, code: int, config: Config):
        self.code = code
        self.config = config
        self.company_folder = config.xbrlfile_folder / str(code)
        self.parser = UnifiedXBRLParser()

    def process(self):
        """企業データの全処理を実行"""
        print(f'-----{self.code}の開始-----')

        self.download()
        self.extract()
        self.parse_bs()
        self.parse_pl()

    def download(self):
        """財務データをダウンロード"""
        # ダウンロードフォルダのzipファイルを削除
        print('ダウンロードフォルダ内のzipファイルを削除')
        FileManager.delete_files(self.config.source_folder)

        # Zipファイルをダウンロード（コメントアウト：時間がかかるため）
        print(f'{self.code}のダウンロード')
        # import zipfile_downloader
        # zipfile_downloader.zip_download(self.code)

        # 企業毎のフォルダ作成
        print(f'{self.code}のフォルダを作成')
        FileManager.create_folder(self.company_folder)

        # Zipファイルを移動
        print(f'{self.code}のzipファイルをフォルダに移動')
        FileManager.move_zipfiles(self.config.source_folder, self.company_folder)

    def extract(self):
        """Zipファイルを解凍してクリーンアップ"""
        # Zipファイルを解凍
        print(f'{self.code}のzipファイルを解凍')
        FileManager.unzip_all(self.company_folder)

        # 不要なファイルとフォルダを削除
        print(f'{self.code}のフォルダ内の不要なファイルとフォルダを削除')
        FileManager.delete_all_files(self.company_folder)
        FileManager.delete_folder(self.company_folder / 'XBRLData')

    def parse_bs(self):
        """BS（貸借対照表）データをパース"""
        print(f'{self.code}のフォルダ内のBSファイルのレコードを作成')

        self._process_statements(
            statement_type='bs',
            periods=['annual', 'quarterly', 'semiannual']
        )

    def parse_pl(self):
        """PL（損益計算書）データをパース"""
        print(f'{self.code}のフォルダ内のPLファイルのレコードを作成')

        self._process_statements(
            statement_type='pl',
            periods=['annual', 'quarterly', 'semiannual']
        )

    def _process_statements(self, statement_type: str, periods: List[str]):
        """財務諸表を処理"""
        for period in periods:
            # 連結決算を処理
            print(f'{self._get_period_name(period)}_連結の{statement_type.upper()}リストの作成')
            consolidated_files = FileManager.get_statement_files(
                self.company_folder, statement_type, period, 'consolidated'
            )
            self._process_file_list(consolidated_files)

            # 連結がない場合は単独決算を処理
            if len(consolidated_files) == 0:
                print(f'{self._get_period_name(period)}_単独の{statement_type.upper()}リストの作成')
                standalone_files = FileManager.get_statement_files(
                    self.company_folder, statement_type, period, 'standalone'
                )
                self._process_file_list(standalone_files)
            elif period == 'semiannual':
                # 中間期は連結と単独両方処理
                print(f'{self._get_period_name(period)}_単独の{statement_type.upper()}リストの作成')
                standalone_files = FileManager.get_statement_files(
                    self.company_folder, statement_type, period, 'standalone'
                )
                self._process_file_list(standalone_files)

    def _process_file_list(self, file_list: List[str]):
        """ファイルリストを処理"""
        for file_path in file_list:
            self.parser.parse(file_path)
            self.parser.save_to_db(file_path)

    @staticmethod
    def _get_period_name(period: str) -> str:
        """期間タイプの日本語名を取得"""
        return {
            'annual': '本決算',
            'quarterly': '四半期決算',
            'semiannual': '中間期決算'
        }[period]


class XBRLProcessingSystem:
    """XBRLデータ処理システムのメインクラス"""

    def __init__(self, config: Config):
        self.config = config

    def run(self):
        """全企業のデータ処理を実行"""
        print(f'企業コード：{self.config.codes}')
        print(f'ダウンロードフォルダ：{self.config.source_folder}')

        for code in self.config.codes:
            processor = CompanyDataProcessor(code, self.config)
            processor.process()

        print('\n全ての処理が完了しました！')


def main():
    """メイン処理"""
    config = Config.from_defaults()
    system = XBRLProcessingSystem(config)
    system.run()


if __name__ == '__main__':
    main()