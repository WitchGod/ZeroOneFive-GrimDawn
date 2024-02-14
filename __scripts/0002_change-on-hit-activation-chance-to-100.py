from datetime import datetime
from pathlib import Path
import shutil

import pandas as pd

# Define the path to the .dbr file
dbr_file_path = Path("./database/skills/playerclass01/counterstrike1.dbr").resolve()

script_parent_dir = Path.cwd()
print(script_parent_dir)

target_path = script_parent_dir / dbr_file_path
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
backup_path = target_path.with_suffix(".dbro")
backup_path = backup_path.with_stem(f"{backup_path.stem}_{timestamp}")

print(target_path)
print(backup_path)

shutil.copyfile(target_path, backup_path)

# # Read the .dbr file into a DataFrame
df = pd.read_csv(target_path, sep=",", index_col=False, names=["key", "value"])

# # # # Filter rows where key equals "onHitActivationChance"
# on_hit_rows = df[df["key"] == "onHitActivationChance"]

# # # # Update the values
# on_hit_rows["value"] = on_hit_rows["value"].apply(
#     lambda x: "100.0" if ";" not in x else ";".join(["100.0" for _ in x.split(";")])
# )

# # # Update the original DataFrame with modified values
# df.update(on_hit_rows)

# Make activation chance perfect.
df.loc[df["key"] == "onHitActivationChance", "value"] = 100.0

# Make skill target radius huge.
df.loc[df["key"] == "skillTargetRadius", "value"] = 1000.0

# Make skill cooldown time non-existent.
df.loc[df["key"] == "skillCooldownTime", "value"] = 0.0

# Make expansion time instant.
df.loc[df["key"] == "expansionTime", "value"] = 0.0

# print(df.head(1000))

# # Write the modified DataFrame back to the .dbr file
df.to_csv(
    target_path,
    sep=",",
    header=False,
    index=False,
    lineterminator=",\n",
)
