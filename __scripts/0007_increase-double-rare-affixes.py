from pathlib import Path
import shutil
import os

import pandas as pd
from pandas.errors import SettingWithCopyWarning
import warnings

warnings.simplefilter(action="ignore", category=(SettingWithCopyWarning))
from loguru import logger
import json

ref_keys = [
    "bothPrefixSuffix",
    "brokenOnly",
    "noPrefixNoSuffix",
    "normalPrefixRareSuffix",
    "prefixOnly",
    "rareBothPrefixSuffix",
    "rarePrefixNormalSuffix",
    "rarePrefixOnly",
    "rareSuffixOnly",
    "suffixOnly",
]


def safe_parse_real(value):
    safe_value = None
    try:
        safe_value = float(value)
    except ValueError:
        safe_value = None
    return safe_value


def allow_double_rare_affixes(table_dir):
    target_tables = list(table_dir.glob("**/*.dbr"))
    base_path = Path(os.path.commonprefix(target_tables))

    for target_table in target_tables:
        if not target_table.stem.startswith("tdyn"):
            continue
        df = pd.read_csv(target_table, sep=",", index_col=False, names=["key", "value"])
        for rkey in ref_keys:
            value = df.loc[df["key"] == rkey, "value"].tolist()
            if not value:
                # Then the line's value is empty.
                value = 0
            else:
                value = value[0]
                if value.isnumeric():
                    value = safe_parse_real(value)
                elif isinstance(value, str):
                    value = 0.0
            relative_path = Path(target_table).relative_to(base_path)
            logger.info(f"{relative_path} - rkey: {rkey} - value: {value}")
            if rkey not in ["rareBothPrefixSuffix"]:
                df.loc[df["key"] == rkey, "value"] = 0.0
            else:
                df.loc[df["key"] == rkey, "value"] = 500000.0

        df.to_csv(
            target_table,
            sep=",",
            header=False,
            index=False,
            lineterminator=",\n",
        )


def main():
    script_dir = Path(__file__).resolve().parent
    mod_base_dir = script_dir.parent
    tables_dir = mod_base_dir / "database/records/items/loottables"

    allow_double_rare_affixes(tables_dir)


if __name__ == "__main__":
    main()
