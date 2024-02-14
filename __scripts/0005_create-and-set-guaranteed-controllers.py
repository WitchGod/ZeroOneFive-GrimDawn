from pathlib import Path
import shutil

import pandas as pd
from loguru import logger


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


def update_cloned_controllers(path_to_cloned_controllers):
    # script_parent_dir = Path(__file__).resolve().parent.parent
    # # print(script_parent_dir)

    # target_dir = script_parent_dir
    # controllers_dir = target_dir / "database/records/controllers/itemskills_zof/"

    controllers = list(path_to_cloned_controllers.glob("**/*.dbr"))

    for controller in controllers:
        if controller.stem.startswith("base"):
            continue
        df = pd.read_csv(controller, sep=",", index_col=False, names=["key", "value"])
        skill_keys = df["key"].tolist()
        if "chanceToRun" not in skill_keys:
            continue

        value = df.loc[df["key"] == "chanceToRun", "value"].item()
        update_value = 100
        item_log = f"{controller.parent.stem} - {controller.stem} - old_value: {value} - new_value: {update_value}"
        df.loc[df["key"] == "chanceToRun", "value"] = update_value
        df.to_csv(
            controller,
            sep=",",
            header=False,
            index=False,
            lineterminator=",\n",
        )

        logger.info(item_log)


def hotswap_controllers(key, replacement_value, target_dir, skip="_"):
    target_skills = list(target_dir.glob("**/*.dbr"))

    for skill in target_skills:
        if skill.stem.startswith(skip):
            continue
        df = pd.read_csv(skill, sep=",", index_col=False, names=["key", "value"])
        skill_keys = df["key"].tolist()
        if key not in skill_keys:
            continue
        value = df.loc[df["key"] == key, "value"].item()
        update_value = None
        if replacement_value not in value:
            update_value = value.replace("itemskills", replacement_value)
        if not replacement_value:
            item_log = (
                f"{skill.parent.stem} - {skill.stem} - key: {key} - value: {value}"
            )
        else:
            item_log = f"{skill.parent.stem} - {skill.stem} - key: {key} - old_value: {value} - new_value: {update_value}"
            df.loc[df["key"] == key, "value"] = update_value
            df.to_csv(
                skill,
                sep=",",
                header=False,
                index=False,
                lineterminator=",\n",
            )

        logger.info(item_log)


def main():
    script_parent_dir = Path(__file__).resolve().parent.parent
    controllers_dir = script_parent_dir / "database/records/controllers/itemskills/"
    cloned_controllers_dir = (
        script_parent_dir / "database/records/controllers/itemskills_zof/"
    )
    devotion_skills_dir = script_parent_dir / "database/records/skills/devotion/"
    items_dir = script_parent_dir / "database/records/items/"
    clone_folder(controllers_dir, cloned_controllers_dir)
    update_cloned_controllers(cloned_controllers_dir)
    hotswap_controllers("templateAutoCast", "itemskills_zof", devotion_skills_dir)
    hotswap_controllers("itemSkillAutoController", "itemskills_zof", items_dir)


if __name__ == "__main__":
    main()
