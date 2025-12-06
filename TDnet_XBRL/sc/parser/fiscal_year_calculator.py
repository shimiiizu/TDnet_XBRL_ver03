# fiscal_year_calculator.py

from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


class FiscalYearCalculator:
    """
    会計年度を算出する専用クラス

    期間終了日とクォーター情報から、会計年度末の年を算出する。
    各クォーターに応じた月数を加算して会計年度末を推定する。
    """

    @staticmethod
    def calculate(end_date_str, quarter):
        """
        終了日とクォーターから会計年度（終了年）を算出

        ロジック:
        - Q1: 終了日 + 9ヶ月 → その年が会計年度
        - Q2: 終了日 + 6ヶ月 → その年が会計年度
        - Q3: 終了日 + 3ヶ月 → その年が会計年度
        - Q4: 終了日 + 0ヶ月 → その年が会計年度

        Args:
            end_date_str (str): 期間終了日（例: "2016-06-30"）
            quarter (str): クォーター（例: "Q1", "Q2", "Q3", "Q4"）

        Returns:
            int: 会計年度（会計年度末の年）
                 算出できない場合は None

        Examples:
            >>> FiscalYearCalculator.calculate("2016-06-30", "Q1")
            2017  # 2016-06-30 + 9ヶ月 = 2017-03-30

            >>> FiscalYearCalculator.calculate("2016-06-30", "Q2")
            2016  # 2016-06-30 + 6ヶ月 = 2016-12-30

            >>> FiscalYearCalculator.calculate("2016-06-30", "Q4")
            2016  # 2016-06-30 + 0ヶ月 = 2016-06-30
        """
        try:
            # 日付をパース
            match = re.match(r'(\d{4})-(\d{2})-(\d{2})', end_date_str)
            if not match:
                print(f"日付フォーマットエラー: {end_date_str}")
                return None

            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # クォーターから加算する月数を決定
            quarter_to_months = {
                'Q1': 9,  # Q1終了 + 9ヶ月 → 会計年度末
                'Q2': 6,  # Q2終了 + 6ヶ月 → 会計年度末
                'Q3': 3,  # Q3終了 + 3ヶ月 → 会計年度末
                'Q4': 0  # Q4終了 = 会計年度末
            }

            if quarter not in quarter_to_months:
                print(f"クォーター情報が不正: {quarter}")
                return None

            months_to_add = quarter_to_months[quarter]

            # 会計年度末を算出
            fiscal_year_end = end_date + relativedelta(months=months_to_add)

            # 会計年度 = 会計年度末の年
            fiscal_year = fiscal_year_end.year

            print(f"[FiscalYearCalculator] 終了日={end_date_str}, Q={quarter}, "
                  f"+{months_to_add}ヶ月={fiscal_year_end.date()}, 会計年度={fiscal_year}")

            return fiscal_year

        except Exception as e:
            print(f"会計年度算出エラー: {e}")
            import traceback
            traceback.print_exc()
            return None


# ============================================================
# テスト
# ============================================================
if __name__ == '__main__':
    test_cases = [
        # (期間終了日, クォーター, 期待される会計年度)
        ("2016-06-30", "Q1", 2017),  # 2016-06-30 + 9ヶ月 = 2017-03-30
        ("2016-06-30", "Q2", 2016),  # 2016-06-30 + 6ヶ月 = 2016-12-30
        ("2016-06-30", "Q3", 2016),  # 2016-06-30 + 3ヶ月 = 2016-09-30
        ("2016-06-30", "Q4", 2016),  # 2016-06-30 + 0ヶ月 = 2016-06-30

        # 3月決算企業のケース（4月始まり3月終わり）
        ("2016-06-30", "Q1", 2017),  # FY2017のQ1
        ("2016-09-30", "Q2", 2017),  # FY2017のQ2
        ("2016-12-31", "Q3", 2017),  # FY2017のQ3
        ("2017-03-31", "Q4", 2017),  # FY2017のQ4
    ]

    print("=== 会計年度算出テスト ===")
    for end_date, quarter, expected in test_cases:
        result = FiscalYearCalculator.calculate(end_date, quarter)
        status = "✅" if result == expected else "❌"
        print(f"{status} {end_date} {quarter} → {result} (期待値: {expected})")