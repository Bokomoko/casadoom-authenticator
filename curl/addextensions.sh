#!/bin/bash
# create 
# Check if the input file is provided 
if [ -z "$1" ]; then 
    echo "Usage: $0 <input_file>" 
    exit 1 
fi 
# Command to prepend 
prepend_command="code  " 
# Read lines from the input file and run the command 
while IFS= read -r line; do
    # get rid of " and , 
    line=$(echo $line | sed 's/[",]//g')
    $prepend_command $line 
done < "$1"