"""
東証上場会社情報サービス（https://www2.jpx.co.jp/tseHpFront/JJK010010Action.do?Show=Show）から
指定した企業コードのZipをダウンロードするプログラム
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from tqdm import tqdm

def zip_download(code):
    print(f"★{code}のzipダウンロードを実行")

    driver = None
    try:
        # ブラウザを起動
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)  # 最大10秒待機

        driver.get("https://www2.jpx.co.jp/tseHpFront/JJK010010Action.do?Show=Show")

        # 検索ボックスに企業コードを入力
        input_box = wait.until(EC.presence_of_element_located((By.NAME, "eqMgrCd")))
        input_box.clear()
        input_box.send_keys(code)
        print(f"企業コード {code} を入力しました")

        # 検索ボタンを押す
        search_button = driver.find_element(By.NAME, 'searchButton')
        search_button.click()
        print("検索ボタンをクリックしました")
        time.sleep(3)  # 検索結果の読み込みを待つ

        # 検索結果があるか確認
        try:
            # 詳細ボタンを待機して取得
            detail_button = wait.until(
                EC.presence_of_element_located((By.NAME, 'detail_button'))
            )
            print("詳細ボタンが見つかりました")
            detail_button.click()
            time.sleep(2)

        except TimeoutException:
            print(f"エラー: 企業コード {code} の検索結果が見つかりません")
            print("検索結果が0件の可能性があります")
            return

        # JavaScriptを実行してタブを切り替え
        js_code = "javascript:changeTab('2');"
        driver.execute_script(js_code)
        print("タブ2に切り替えました")
        time.sleep(2)

        # 開示ボタンを押す
        try:
            kaiji_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/div[3]/div/table[4]/tbody/tr/th/input'))
            )
            kaiji_button.click()
            print("開示ボタンをクリックしました")
            time.sleep(2)
        except TimeoutException:
            print("開示ボタンが見つかりませんでした")
            return

        # 更に表示ボタンを押す
        try:
            saranihyouji_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/div[3]/div/table[5]/tbody/tr[3]/td/input'))
            )
            saranihyouji_button.click()
            print("更に表示ボタンをクリックしました")
            time.sleep(3)
        except TimeoutException:
            print("更に表示ボタンが見つかりませんでした（既に全件表示されている可能性）")

        # XBRLファイル毎にでループ処理を行う
        elements = driver.find_elements(By.XPATH, '//img[@alt="XBRL"]')

        if len(elements) == 0:
            print("XBRLファイルが見つかりませんでした")
            return

        print(f'ダウンロード総数：{len(elements)}件')

        # ダウンロード処理
        successful_downloads = 0
        failed_downloads = 0

        for i, element in enumerate(tqdm(elements, desc="Processing"), 1):
            try:
                # 要素が表示されているか確認
                if element.is_displayed():
                    element.click()
                    time.sleep(2)
                    successful_downloads += 1
                else:
                    print(f"\n{i}番目の要素は表示されていません（スキップ）")
                    failed_downloads += 1

            except Exception as e:
                print(f"\n{i}番目のダウンロードでエラー: {str(e)}")
                failed_downloads += 1
                continue

        print(f"\n完了: 成功 {successful_downloads}件, 失敗 {failed_downloads}件")

    except Exception as e:
        print(f"予期しないエラーが発生しました: {str(e)}")

    finally:
        # WebDriverを終了
        if driver:
            print('Chromeを閉じます')
            time.sleep(2)
            driver.quit()


if __name__ == '__main__':
    zip_download(7003)