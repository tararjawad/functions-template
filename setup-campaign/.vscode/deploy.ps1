# Define the name of the config file
$configFileName = "config.properties"

# Check if config.properties exists in the current directory, otherwise check in the .vscode folder
if (Test-Path -Path "./$configFileName") {
    $configFilePath = "./$configFileName"
} elseif (Test-Path -Path "./.vscode/$configFileName") {
    $configFilePath = "./.vscode/$configFileName"
} else {
    Write-Error "config.properties not found in the current directory or .vscode folder."
    exit
}

# Initialize a hashtable to store config values
$config = @{}
Get-Content $configFilePath | ForEach-Object {
    $key, $value = $_ -split '=', 2
    $config[$key] = $value
}

# Assign variables from config
$project = $config['project']
$region = $config['region']
$function_name = $config['function_name']
$path_pattern = $config['path_pattern']
$filter_type = $config['filter_type']
$entry_point = $config['entry_point']
$runtime = $config['runtime']
$memory = $config['memory']

# Proceed with the rest of the script
$directory = $PWD.Path + "/source"
cd $directory
echo "Building $function_name in $PWD"
$deployCommand = "gcloud functions deploy $function_name --gen2 --project=$project --runtime=$runtime --region=$region --trigger-location=$region --source=. --entry-point=$entry_point --trigger-event-filters=type=$filter_type --trigger-event-filters=database='(default)' --trigger-event-filters-path-pattern=document=$path_pattern --memory=$memory"
Invoke-Expression $deployCommand
echo $deployCommand