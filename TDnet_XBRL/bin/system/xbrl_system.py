# system/xbrl_system.py

from ..processor.company_processor import CompanyDataProcessor
from ..config.config import Config


class XBRLProcessingSystem:
    """
    XBRLデータ処理システム全体を管理するクラス。
    複数の企業コードをまとめて処理する「司令塔」の役割。
    """

    def __init__(self, config: Config):
        self.config = config

    # ----------------------------------------------------------------------
    # メイン実行
    # ----------------------------------------------------------------------
    def run(self):
        """全企業コードに対してXBRL処理を順次実行する"""
        print("=== XBRL Processing System 開始 ===")
        print(f"対象企業コード: {self.config.codes}")
        print(f"ダウンロードフォルダ: {self.config.source_folder}")
        print("----------------------------------------------------")

        for code in self.config.codes:
            try:
                processor = CompanyDataProcessor(code, self.config)
                processor.process()
            except Exception as e:
                print(f"[エラー] 企業コード {code} の処理中に例外が発生しました: {e}")
                # continue により他のコード処理は継続可能
                continue

        print("=== 全てのXBRL処理が完了しました ===")
