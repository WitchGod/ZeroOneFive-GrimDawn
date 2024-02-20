from pathlib import Path
import shutil
import os

import pandas as pd
from pandas.errors import SettingWithCopyWarning
import warnings

warnings.simplefilter(action="ignore", category=(SettingWithCopyWarning))
from loguru import logger
import json

ref_keys = ["skillTemplates"]


def safe_parse_real(value):
    safe_value = None
    try:
        safe_value = float(value)
    except ValueError:
        safe_value = None
    return safe_value


def get_legal_templates(templates_dir):
    target_templates = list(templates_dir.glob("**/*.dbr"))
    target_templates = [t for t in target_templates if t.stem.startswith("skill_")]
    return target_templates


def modify_skill_templates(target_dir, replacement_value):
    target_tables = list(target_dir.glob("**/*.dbr"))
    base_path = Path(os.path.commonprefix(target_tables))

    for target_table in target_tables:
        if not target_table.stem.endswith("_skill"):
            continue
        df = pd.read_csv(target_table, sep=",", index_col=False, names=["key", "value"])
        dbr_keys = df["key"].tolist()
        for rkey in ref_keys:
            if rkey not in dbr_keys:
                continue
            value = df.loc[df["key"] == rkey, "value"].tolist()
            if not value:
                # Then the line's value is empty.
                value = 0
            else:
                value = value[0]
                if value.isnumeric():
                    value = safe_parse_real(value)
                elif isinstance(value, str):
                    value = value
            relative_path = Path(target_table).relative_to(base_path)
            logger.info(f"[ORIGINAL] {relative_path} - rkey: {rkey} - value: {value}")
            df.loc[df["key"] == rkey, "value"] = replacement_value
            value = df.loc[df["key"] == rkey, "value"].item()
            logger.info(f"[MODIFIED] {relative_path} - rkey: {rkey} - value: {value}")

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
    database_dir = mod_base_dir / "database"
    tables_dir = mod_base_dir / "database/records/skills/devotion"
    templates_dir = mod_base_dir / "database/records/skills/base_template skills"

    all_legal_templates = get_legal_templates(templates_dir)
    all_legal_templates = [
        Path(t).relative_to(database_dir).as_posix() for t in all_legal_templates
    ]
    all_legal_templates_str = ";".join(all_legal_templates)
    modify_skill_templates(tables_dir, all_legal_templates_str)


if __name__ == "__main__":
    main()
