# Define the path to the .dbr file
$dbrFilePath = "..\database\skills\playerclass01\counterstrike1.dbr"

# Create a backup of the .dbr file
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$backupFilePath = "$($dbrFilePath.Replace(".dbr", "_$timestamp.dbro") )"
Copy-Item -Path $dbrFilePath -Destination $backupFilePath

# Read the .dbr file line by line
$content = Get-Content -Path $dbrFilePath
$newContent = foreach ($line in $content) {
    # Split the line into key and value
    $key, $value = $line -split '\s+', 2

    # If the key matches "onHitActivationChance"
    if ($key -eq "onHitActivationChance") {
        # Check if the value is a single value or semicolon-separated
        if ($value -notlike "*;*") {
            # If it's a single value, change it to 100.0
            $value = "100.0"
        } else {
            # If it's semicolon-separated, split it and replace every value with 100.0
            $values = $value -split ";"
            $values = $values | ForEach-Object { "100.0" }
            $value = $values -join ";"
        }
    }

    # Reconstruct the line with updated value
    "$key $value"
}

# Overwrite the original .dbr file with the modified content
$newContent | Set-Content -Path $dbrFilePath