"""
BS関連情報を表示する。

"""
from stock_price_getter import StockPriceGetter
from bs_db_extractor import BsDbExtractor
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

code = 3941  # ★
bsdbextractor = BsDbExtractor(code)

# 株価との比較対象を選択
# hikaku = bsdbextractor.extract_retainedearnings()  # ★(common)
# hikaku = bsdbextractor.extract_assets()  # ★(common)
# hikaku = bsdbextractor.extract_NetAssets()  # ★(Japan gaap)
hikaku = bsdbextractor.extract_equity()  # ★(IFRS)

# 株価を取得
startday = bsdbextractor.extract_public_day()[0]
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

# 右側のY軸を作成し、データをプロット
ax2 = ax1.twinx()
ax2.bar(bsdbextractor.extract_public_day(), hikaku, color='skyblue', width=20, alpha=0.5)  # ★
ax2.set_ylabel('（億円）')

# X軸のラベルを90度回転
for label in ax1.get_xticklabels():
    label.set_rotation(90)

# グラフのタイトルを追加
fig.suptitle(bsdbextractor.extract_company_name() + ' ' + str(code))
fig.tight_layout()
plt.show()
