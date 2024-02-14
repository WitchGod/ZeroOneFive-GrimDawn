from pathlib import Path

import pandas as pd
from loguru import logger


def find_key_value(key, type="player_skills", skip="_", value_match=None):
    script_parent_dir = Path(__file__).resolve().parent.parent
    # print(script_parent_dir)

    target_dir = script_parent_dir

    if type == "all_database":
        target_dir = script_parent_dir / "database/"

    if type == "all_records":
        target_dir = target_dir / "database/records/"

    if type == "all_skills":
        target_dir = target_dir / "database/records/skills/"

    target_skills = list(target_dir.glob("**/*.dbr"))

    if type == "player_skills":
        target_dir = target_dir / "database/records/skills/"
        target_skills = list(target_dir.glob("playerclass*/*.dbr"))

    for skill in target_skills:
        if skill.stem.startswith(skip):
            continue
        df = pd.read_csv(skill, sep=",", index_col=False, names=["key", "value"])
        skill_keys = df["key"].tolist()
        if key not in skill_keys:
            continue
        value = df.loc[df["key"] == key, "value"].item()
        if value_match:
            if value != value_match:
                continue
        item_log = f"{skill.parent.stem} - {skill.stem} - key: {key} - value: {value}"
        logger.info(item_log)


if __name__ == "__main__":
    key = "exclusiveSkill"
    find_key_value(key, "player_skills", skip="_class", value_match="1")
