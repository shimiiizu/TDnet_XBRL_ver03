# main.py

from config import Config
from xbrl_system import XBRLProcessingSystem

def main():
    """
    XBRL処理システムのエントリーポイント。
    Config を読み込み、XBRLProcessingSystem を起動する。
    """
    # 設定を読み込み（CSV版を利用しても良い）
    config = Config.from_defaults()
    # config = Config.from_csv("./config/code_list.csv")

    # 必要であれば設定チェック
    # config.validate()

    # XBRL処理システムを起動
    system = XBRLProcessingSystem(config)
    system.run()


if __name__ == "__main__":
    main()
