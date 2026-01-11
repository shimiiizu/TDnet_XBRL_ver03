### タイトル
TDnet_XBRL ツールキット

### 概要
TDnet_XBRL ツールキットとはXBRL形式で提供されるTDnet情報を扱うためのツールキットです。このツールキットは、TDnetから取得したXBRLデータを解析し、必要な情報を抽出・加工、表示するための機能を提供します。

### 使い方
TDnet_XBRLツールキットを使用するには、まずPython環境をセットアップし、必要な依存関係をインストールしてください。次に、TDnetからXBRLデータをダウンロードし、ツールキットの関数を使用してデータを解析します。具体的な使用例やコードスニペットは、ドキュメント内の「使用例」セクションをご参照ください。
#### ① config.pyに銘柄コードを記入
#### ② main.pyを実行
#### ③ app.pyを実行
#### ④ webブラウザで参照

### ファイル構成

- `Tdnet_xbrl/`
  - `db/`: データベース関連ファイルが含まれるディレクトリ。
    - `BS_DB`:
    - `PL_DB`:
  - `docs/`: ドキュメントファイルが含まれるディレクトリ
    - `README.md`: このREADMEファイル
  - `flask_app/`: flask関連のコードが含まれるディレクトリ
    - `templates/`: index.htmlを補完するディレクトリ
      - `app.py`:  html表示させるファイル（このコードを実行する）
    - `sc/`: ソースコードファイルが含まれるディレクトリ
      - `config/`:設定ファイルを補完
        - `config.py`: 設定管理ファイル(★★ここに銘柄コードを記入)
      - `fileio/`:設定ファイルを補完
        - `core/`
          - `file_operations.py`:  ファイル走査の関数を集めたファイル
          - `financial_report_loader.py`:          
        - `__init__.py`: パッケージ初期化ファイル
        - `all_files_delater.py`: 全てのファイルを削除するコード
        - `bs_filelist_maker.py`: BSファイルのリストを作成するコード
        - `file_manager.py`: データ抽出ロジックファイル
        - `files_deleter.py`: データ抽出ロジックファイル
        - `folder_deleter.py`: データ抽出ロジックファイル
      
        - `visualizer.py`: データ可視化ロジックファイル
      - `inserter/`:設定ファイルを補完
        - `bs_db_inserter.py`:BSのDBに値を挿入
        - `pl_db_inserter.py`:PLのDBに値を挿入
      
      - `parser/`:パーサー関連のコードを保管するディレクトリ
        - 
      - `printer/`:表示関連のコードを保管するディレクトリ
            - `bs_common_printer.py`: BSの基本情報を出力する
            - `bs_ifrs_printer.py`: BS_ifrsの情報を出力する
            - `bs_japan_gaap_printer.py`:
      - `processor/`:表示関連のコードを保管するディレクトリ
      - `systeme/`:表示関連のコードを保管するディレクトリ
      - `utils/`:表示関連のコードを保管するディレクトリ
        -`main.py`:メインのソースコード
### 今後
#### ①CF計算書も取り込めるようにする。
#### ②リファクタリングを行う。(ファイル数が多すぎるため)
#### ③文字列を含む銘柄コードに対応していない。（DBに挿入できない）

### 注意事項
#### 精度は保証されていないため、注意が必要
#### デプロイをしたい。