#!/bin/bash

# Get the current working directory.
cwd=$(pwd)

# Check if the config.properties file exists in the current working directory.
if [ -f "$cwd/config.properties" ]; then
  # If the file exists, use it.
  config_file="$cwd/config.properties"
else
  # If the file does not exist, use the one in the .vscode directory.
  config_file="$cwd/.vscode/config.properties"
fi

# Read the values from the config.properties file.
while IFS='=' read -r key value
do
  eval ${key}=\${value}
done < "$config_file"


directory=$(pwd)/source
cd $directory

echo "___________________________________"
echo "Building $function_name in $(pwd)"


cdd="gcloud functions deploy $function_name --gen2 --runtime=$runtime --project=$project --region=$region --trigger-location=$region --source=. --entry-point=$entry_point --trigger-event-filters=type=$filter_type --trigger-event-filters=database='(default)' --trigger-event-filters-path-pattern=document=$path_pattern --memory=128Mi"

echo $cdd

eval $cdd
# print empty new line

