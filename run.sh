#!/bin/bash

# Activate the Poetry environment
source $(/home/pi/.local/bin/poetry env info --path)/bin/activate

# Run the entry point script
# we have to specify the whole directory because is not finding it in that route?
/home/pi/.local/bin/poetry run backlight_start | while IFS= read -r line; do echo "$(date +%Y-%m-%d\ %H:%M:%S) $line"; done >> output.log 2>&1