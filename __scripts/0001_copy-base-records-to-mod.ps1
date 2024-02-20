# ! Change the destination as needed.
# TODO: Change to a loop-based copying but this is less problematic, e.g. shadow-deletes. 

# $source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx0\records"
# $source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records"
# $source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records"
# $destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records"

# if (-not (Test-Path -Path $destination)) {
#     New-Item -Path $destination -ItemType Directory -Force
# }

# Copy-Item -Path "$source1\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 5
# Copy-Item -Path "$source2\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 5
# Copy-Item -Path "$source3\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 5

# $source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx0\records\controllers"
# $source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records\controllers"
# $source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records\controllers"
# $destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records\controllers"

# if (-not (Test-Path -Path $destination)) {
#     New-Item -Path $destination -ItemType Directory -Force
# }

# Copy-Item -Path "$source1\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source2\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source3\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2

# $source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx0\records\items"
# $source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records\items"
# $source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records\items"
# $destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records\items"

# if (-not (Test-Path -Path $destination)) {
#     New-Item -Path $destination -ItemType Directory -Force
# }

# Copy-Item -Path "$source1\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source2\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source3\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2

# $source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx0\records\creatures"
# $source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records\creatures"
# $source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records\creatures"
# $destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records\creatures"

# if (-not (Test-Path -Path $destination)) {
#     New-Item -Path $destination -ItemType Directory -Force
# }

# Copy-Item -Path "$source1\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source2\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source3\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2

# $source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx0\records\game"
# $source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records\game"
# $source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records\game"
# $destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records\game"

# if (-not (Test-Path -Path $destination)) {
#     New-Item -Path $destination -ItemType Directory -Force
# }

# Copy-Item -Path "$source1\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source2\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2
# Copy-Item -Path "$source3\*" -Destination $destination -Recurse -Force -ErrorAction SilentlyContinue
# Start-Sleep -Seconds 2

$source1 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx0\records"
$source2 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx1\database\records"
$source3 = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\gdx2\database\records"
$destination = "E:\SteamLibrary\steamapps\common\Grim Dawn\dev\mods\ZeroOneFive\database\records"

if (-not (Test-Path -Path $destination)) {
    New-Item -Path $destination -ItemType Directory -Force
}

# Robocopy source1 to destination
robocopy $source1 $destination /E /MIR /R:0 /W:0 /NFL /NDL /NS /NC

# Wait for 5 seconds
Start-Sleep -Seconds 5

# Robocopy source2 to destination
robocopy $source2 $destination /E /MIR /R:0 /W:0 /NFL /NDL /NS /NC

# Wait for 5 seconds
Start-Sleep -Seconds 5

# Robocopy source3 to destination
robocopy $source3 $destination /E /MIR /R:0 /W:0 /NFL /NDL /NS /NC