# main.py

from bin.config.config import Config
from bin.system.xbrl_system import XBRLProcessingSystem

def main():
    """
    XBRL処理システムのエントリーポイント。
    Config を読み込み、XBRLProcessingSystem を起動する。
    """

    # 設定(config.py)
    config = Config.from_defaults()

    # XBRL処理システム(system/xbrl_system.py)を起動
    system = XBRLProcessingSystem(config)
    system.run()


if __name__ == "__main__":
    main()
