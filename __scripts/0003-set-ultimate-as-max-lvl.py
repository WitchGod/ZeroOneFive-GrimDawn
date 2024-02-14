from pathlib import Path

import pandas as pd
from loguru import logger


def main():
    script_parent_dir = Path(__file__).resolve().parent.parent
    # print(script_parent_dir)

    database_dir = script_parent_dir / "database/"
    # print(database_dir)

    records_dir = database_dir / "records/"
    # print(records_dir)

    skills_dir = records_dir / "skills/"
    # print(skills_dir)

    player_skills = list(skills_dir.glob("playerclass*/*.dbr"))
    # print(player_skills)

    for player_skill in player_skills:
        if player_skill.stem.startswith("_class"):
            continue
        df = pd.read_csv(player_skill, sep=",", index_col=False, names=["key", "value"])
        skill_keys = df["key"].tolist()
        skill_max_level = None
        skill_ult_level = None
        to_modify = False
        if "skillMaxLevel" in skill_keys:
            skill_max_level = df.loc[df["key"] == "skillMaxLevel", "value"].item()
        if "skillUltimateLevel" in skill_keys:
            skill_ult_level = df.loc[df["key"] == "skillUltimateLevel", "value"].item()
        if skill_max_level and skill_ult_level:
            if int(skill_ult_level) > int(skill_max_level):
                to_modify = True
        else:
            continue

        item_log = f"[ORIGINAL] {player_skill.parent.stem} - {player_skill.stem} - max: {skill_max_level} - ult: {skill_ult_level} - to_modify: {to_modify}"
        logger.info(item_log)

        if to_modify:
            df.loc[df["key"] == "skillMaxLevel", "value"] = skill_ult_level
            df.to_csv(
                player_skill,
                sep=",",
                header=False,
                index=False,
                lineterminator=",\n",
            )
            df = pd.read_csv(
                player_skill, sep=",", index_col=False, names=["key", "value"]
            )
            skill_max_level = df.loc[df["key"] == "skillMaxLevel", "value"].item()
            skill_ult_level = df.loc[df["key"] == "skillUltimateLevel", "value"].item()
            item_log = f"[MODIFIED] {player_skill.parent.stem} - {player_skill.stem} - max: {skill_max_level} - ult: {skill_ult_level}"
            logger.info(item_log)


if __name__ == "__main__":
    main()
