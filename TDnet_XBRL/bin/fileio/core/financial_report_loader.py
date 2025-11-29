# fileio/core/financial_report_loader.py
from pathlib import Path
from typing import List, Literal
from bin.fileio import bs_filelist_maker, pl_filelist_maker

StatementType = Literal["bs", "pl"]
PeriodType = Literal["annual", "quarterly", "semiannual"]
ConsolidationType = Literal["consolidated", "standalone"]

_CODE_MAP = {
    ("annual", "consolidated"): "ac",
    ("annual", "standalone"): "an",
    ("quarterly", "consolidated"): "qc",
    ("quarterly", "standalone"): "qn",
    ("semiannual", "consolidated"): "sc",
    ("semiannual", "standalone"): "sn",
}

def get_statement_files(
    folder: Path | str,
    statement_type: StatementType,
    period_type: PeriodType,
    consolidation: ConsolidationType,
) -> List[str]:
    code = _CODE_MAP[(period_type, consolidation)]
    folder_str = str(folder)

    # 諸表タイプに応じた設定
    if statement_type == "bs":
        maker = bs_filelist_maker
        suffixes = ["bs", "fs"]          # この順番が大事！
    else:
        maker = pl_filelist_maker
        suffixes = ["pl","pc"]

    # 動的に関数名を生成して呼び出し
    result: List[str] = []
    for suffix in suffixes:
        method = getattr(maker, f"get_{code}{suffix}_list", None)
        if method:
            result.extend(method(folder_str))
    return result