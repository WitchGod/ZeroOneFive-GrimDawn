from pathlib import Path
import shutil
import os

import pandas as pd
from pandas.errors import SettingWithCopyWarning
import warnings

warnings.simplefilter(action="ignore", category=(SettingWithCopyWarning))
from loguru import logger
import json


def clone_folder(source_folder, destination_folder):
    source_path = Path(source_folder)
    destination_path = Path(destination_folder)

    # Ensure source folder exists
    if not source_path.exists() or not source_path.is_dir():
        raise ValueError(
            f"Source folder '{source_folder}' does not exist or is not a directory."
        )

    # Ensure destination folder does not exist
    if destination_path.exists():
        # raise FileExistsError(
        #     f"Destination folder '{destination_folder}' already exists."
        # )
        logger.info(f"Destination folder '{destination_folder}' already exists.")
        return

    # Copy the contents of source folder to destination folder
    shutil.copytree(source_path, destination_path)


def get_params_by_type(params, type):
    filtered_params = []
    for param in params:
        if param.get("type") == type:
            filtered_params.append(param["name"])
    return filtered_params


def safe_parse_real(value):
    safe_value = None
    try:
        safe_value = float(value)
    except ValueError:
        safe_value = None
    return safe_value


def max_out_items(item_dir, params_to_max):
    target_items = list(item_dir.glob("**/*.dbr"))
    base_path = Path(os.path.commonprefix(target_items))

    for target_item in target_items:
        df = pd.read_csv(target_item, sep=",", index_col=False, names=["key", "value"])
        skill_keys = df["key"].tolist()
        if (
            "attributeScalePercent" not in skill_keys
            and "lootRandomizerJitter" not in skill_keys
        ):
            continue

        scaler = None
        jitter = None
        if "attributeScalePercent" in skill_keys:
            scaler = safe_parse_real(
                df.loc[df["key"] == "attributeScalePercent", "value"].item()
            )
        if "lootRandomizerJitter" in skill_keys:
            jitter = safe_parse_real(
                df.loc[df["key"] == "lootRandomizerJitter", "value"].item()
            )
        relative_path = Path(target_item).relative_to(base_path)
        logger.info(f"{relative_path} - scaler: {scaler} - jitter: {jitter}")

        filtered = df.loc[
            (df["key"].isin(params_to_max))
            & (df["value"].apply(lambda x: safe_parse_real(x)))
            > 0,
        ]

        multiplier = None
        max_value = None
        if "attributeScalePercent" in skill_keys:
            multiplier = scaler
        if "lootRandomizerJitter" in skill_keys:
            multiplier = jitter
        if multiplier:
            for fkey in filtered["key"].tolist():
                if fkey == "characterBaseAttackSpeed":
                    continue
                orig_value = filtered.loc[filtered["key"] == fkey, "value"].item()
                orig_value = safe_parse_real(orig_value)
                max_value = orig_value * ((100 + multiplier) / 100.0)
                # If this is a Min stat, let's remove range and apply the Max.
                if fkey.endswith("Min"):
                    print("\tFound problematic pair:", fkey)
                    new_fkey = fkey.replace("Min", "Max")
                    # Basically, a pair exists.
                    if new_fkey in filtered["key"].tolist():
                        max_value = filtered.loc[
                            filtered["key"] == new_fkey, "value"
                        ].item()
                        max_value = safe_parse_real(max_value)
                        max_value = max_value * ((100 + multiplier) / 100.0)
                    else:
                        print("\tNo pair found. No adjustment needed.")
                        break
                print(f"\t{fkey} : {orig_value} : {max_value}")
                df.loc[df["key"] == fkey, "value"] = max_value
            if "attributeScalePercent" in skill_keys:
                df.loc[df["key"] == "attributeScalePercent", "value"] = 0.0
            if "lootRandomizerJitter" in skill_keys:
                df.loc[df["key"] == "lootRandomizerJitter", "value"] = 0.0

        df.to_csv(
            target_item,
            sep=",",
            header=False,
            index=False,
            lineterminator=",\n",
        )


def main():
    script_dir = Path(__file__).resolve().parent
    _templates_dir = script_dir / "__templates/"
    _params_templates_dir = _templates_dir / "__params"
    mod_base_dir = script_dir.parent
    items_dir = mod_base_dir / "database/records/items/"

    consolidated_params_path = _params_templates_dir / "consolidated.json"
    consolidated_params = json.loads(consolidated_params_path.read_text())

    filtered_params = get_params_by_type(consolidated_params, "real")
    max_out_items(items_dir, filtered_params)


if __name__ == "__main__":
    main()
