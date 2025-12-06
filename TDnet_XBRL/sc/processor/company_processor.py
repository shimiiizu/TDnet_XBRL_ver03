# processor/company_processor.py

from typing import List

from ..fileio import zipfile_downloader
from ..fileio.file_manager import FileManager
from ..parser.unified_parser import UnifiedXBRLParser
from sc.config.config import Config


class CompanyDataProcessor:
    """
    1つの企業コードに対して、
    ダウンロード → 解凍 → BS/PL解析 → DB保存
    までの全工程を担当するクラス。
    """

    def __init__(self, code: int, config: Config):
        self.code = code
        self.config = config
        self.company_folder = config.xbrlfile_folder / str(code)
        self.parser = UnifiedXBRLParser()

    def process(self):
        """企業データの全処理を実行"""
        print(f'----- {self.code} の処理開始 -----')

        self.download()
        self.extract()
        self.parse_bs()
        self.parse_pl()

        print(f'----- {self.code} の処理完了 -----\n')

    # ===========================================================================
    # ダウンロード & 準備
    # ===========================================================================

    def download(self):
        """Zip ダウンロード → 移動 → フォルダ準備"""
        print('ダウンロードフォルダ内のzipファイルを削除')
        FileManager.delete_files(self.config.source_folder)

        print(f'{self.code} のZipファイルをダウンロード（必要なら有効化）')
        # import zipfile_downloader
        #zipfile_downloader.zip_download(self.code)

        print(f'{self.code} のフォルダを作成')
        FileManager.create_folder(self.company_folder)

        print(f'{self.code} のzipファイルをフォルダに移動')
        FileManager.move_zipfiles(self.config.source_folder, self.company_folder)

    # ===========================================================================
    # 解凍 & クリーニング
    # ===========================================================================

    def extract(self):
        """Zip解凍 → 不要ファイル削除"""
        print(f'{self.code} のZipファイルを解凍')
        FileManager.unzip_all(self.company_folder)

        print(f'{self.code} の不要ファイルを削除')
        FileManager.delete_all_files(self.company_folder)
        FileManager.delete_folder(self.company_folder / 'XBRLData')

    # ===========================================================================
    # 解析（BS/PL）
    # ===========================================================================

    def parse_bs(self):
        print(f'{self.code}: BSファイルの処理開始')
        self._process_statements(
            statement_type='bs',
            periods=['annual', 'quarterly', 'semiannual']
        )

    def parse_pl(self):
        print(f'{self.code}: PLファイルの処理開始')
        self._process_statements(
            statement_type='pl',
            periods=['annual', 'quarterly', 'semiannual']
        )

    # ===========================================================================
    # 内部ロジック
    # ===========================================================================

    def _process_statements(self, statement_type: str, periods: List[str]):
        """期間別に連結→単独の順でファイルを処理"""
        for period in periods:
            print(f'{self._get_period_name(period)}_連結 {statement_type.upper()} の取得')
            consolidated_files = FileManager.get_statement_files(
                self.company_folder, statement_type, period, 'consolidated'
            )
            self._process_file_list(consolidated_files)

            # 連結がない場合は単独を処理
            if len(consolidated_files) == 0:
                print(f'{self._get_period_name(period)}_単独 {statement_type.upper()} の取得')
                standalone_files = FileManager.get_statement_files(
                    self.company_folder, statement_type, period, 'standalone'
                )
                self._process_file_list(standalone_files)

            # 中間期だけは両方処理
            elif period == 'semiannual':
                print(f'{self._get_period_name(period)}_単独 {statement_type.upper()} の取得')
                standalone_files = FileManager.get_statement_files(
                    self.company_folder, statement_type, period, 'standalone'
                )
                self._process_file_list(standalone_files)

    def _process_file_list(self, files: List[str]):
        """XBRLファイルをパース → DB保存"""
        for file_path in files:
            self.parser.parse(file_path)
            self.parser.save_to_db(file_path)

    @staticmethod
    def _get_period_name(period: str) -> str:
        """期間の日本語名を返す"""
        return {
            'annual': '本決算',
            'quarterly': '四半期',
            'semiannual': '中間期'
        }[period]
