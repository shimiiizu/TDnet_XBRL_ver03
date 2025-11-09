"""
merged DB情報を表示する。

"""
from stock_price_getter import StockPriceGettr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import japanize_matplotlib
from merged_db_extractor import MergedDbExtractor
from pl_db_extractor import PlDbExtractor
import numpy as np

#code = 7172  # ★★★　JIA　〇
#code = 3679  # ★★★ じげん　△
#code = 3288  # ★★★　オープンハウス △
#code = 4617  # ★★★ 中国塗料　△
#code = 4004  # ★★★ レゾナック 〇
#code = 3941  # ★★★ レンゴー　〇
#code = 2780  # ★★★ コメ兵　△
#code = 6988  # ★★★ 日東電工　△
#code = 7014  # ★★★ 名村造船　〇
#code = 5834  # ★★★ SBIリーシング　〇
code = 5233  # ★★★ 太平洋セメント　〇
#code = 7003  # ★★★ 三井E＆S　KeyError: 0

mergeddbextractor = MergedDbExtractor(code)
pldbextractor = PlDbExtractor(code)

# 株価との比較対象を選択
#hikaku = mergeddbextractor.extract_NetSales() # ★
hikaku = mergeddbextractor.extract_assets() # ★

print(hikaku)

# リスト内の数値でない要素やNaN値を0に置き換える
hikaku = [value if isinstance(value, (int, float, np.float64)) and not np.isnan(value) else 0 for value in hikaku]

print(hikaku)


# 株価を取得
startday = mergeddbextractor.extract_public_day()[0]
stockpricegetter = StockPriceGettr(startday, str(code) + ".T")
stock_price, stock_date = stockpricegetter.get_stock_price()


# 年を短縮するフォーマッター関数
def short_year(x, pos):
    return mdates.num2date(x).strftime('%y-%m')


# グラフの作成
fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(stock_date, stock_price)
ax1.set_ylabel('株価（円）')

# 日付フォーマットの設定
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_formatter(FuncFormatter(short_year))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))

# Noneの値がないことを確認
#public_days = mergeddbextractor.extract_public_day()
#hikaku = [value if value is not None else 0 for value in hikaku]  # Noneを0または別のデフォルト値に置き換える


# 右側のY軸を作成し、データをプロット
ax2 = ax1.twinx()
ax2.bar(mergeddbextractor.extract_public_day(), hikaku, color='skyblue', width=20, alpha=0.5)  # ★
ax2.set_ylabel('（億円）')

# X軸のラベルを90度回転
for label in ax1.get_xticklabels():
    label.set_rotation(90)

# グラフのタイトルを追加
fig.suptitle(mergeddbextractor.extract_CompanyName() + ' ' + str(code))
fig.tight_layout()
plt.show()
