# ! Change the destination as needed.
# TODO: Change to a loop-based copying but this is less problematic, e.g. shadow-deletes. 

$source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\database\records\skills"
$source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records\skills"
$source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records\skills"
$destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records\skills"

Copy-Item -Path "$source1\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path "$source2\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path "$source3\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue