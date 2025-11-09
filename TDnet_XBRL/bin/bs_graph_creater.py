"""
BSに関係するグラフを作成する

このコードは、特定の企業の株価や財務データに基づいてグラフを作成するためのものです。

1. **ライブラリのインポート**:
   - `matplotlib.pyplot` と `japanize_matplotlib` を使ってグラフを描画します。
   - `BsDbExtractor` と `StockPriceGettr` は、データベースから財務データや株価を取得するためのカスタムモジュールです。
   - `matplotlib.dates` は、日付のフォーマットを設定するために使用します。

2. **BsGraphCreater クラス**:
   - グラフを作成するためのクラスです。初期化メソッドで、x軸とy軸のデータ、ラベル、グラフのタイトルを設定します。
   - `create_bs_graph` メソッドで、実際にグラフを描画します。バーグラフを作成し、日付のフォーマットやラベルを設定します。

3. **メイン部分**:
   - `startday` と `ticker` を設定し、`StockPriceGettr` を使って指定した期間の株価データを取得します。
   - `BsDbExtractor` を使って、企業名、公開日、資産データを取得します。
   - 取得したデータを使って、`BsGraphCreater` のインスタンスを作成し、グラフを描画します。

このコードは、企業の株価や財務データを視覚的に表示するためのツールとして機能します。
"""
import matplotlib.pyplot as plt
import japanize_matplotlib
from bs_db_extractor import BsDbExtractor
import matplotlib.dates as mdates
from stock_price_getter import StockPriceGettr


class BsGraphCreater():
    def __init__(self, x, y, x_label, y_label, graph_title):
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label
        self.graph_title = graph_title


    def create_bs_graph(self):
        plt.figure(figsize=(10, 4))
        plt.bar(self.x, self.y, color='skyblue', width=20)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.graph_title)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    startday = "2020-01-01"
    ticker = "2780.T"
    stockpricegetter = StockPriceGettr(startday, ticker)
    stock_price, date = stockpricegetter.get_stock_price()

    bsdbextractor = BsDbExtractor(2780)
    company_name, public_day, assets, retainedearnings, equity, netassets = bsdbextractor.extract_data()

    x = date
    y = stock_price
    x_label = 'public_day'
    y_label = 'assets(億円)'
    graph_title = company_name

    bsgraphcreater = BsGraphCreater(x, y, x_label, y_label, graph_title)
    bsgraphcreater.create_bs_graph()
