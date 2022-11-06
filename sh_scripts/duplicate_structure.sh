#!/bin/bash

# Validate the number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <from_path> <to_path>"
    exit 1
fi

from_path=$(realpath $1)
to_path=$(realpath $2)

# Recursive function to duplicate structure
duplicate_structure() {
    local src=$1
    local dest=$2

    # Create destination directory if not exists
    echo mkdir -p "$dest"
    mkdir -p "$dest"

    # Loop through the items in the source directory
    for item in "$src"/*; do
        local base_name=$(basename "$item")
        if [ -d "$item" ]; then
            # If item is a directory, recurse into it
            duplicate_structure "$item" "$dest/$base_name"
        elif [ -L "$item" ]; then
            # If item is a symlink, create a new symlink
            ln -s "$(readlink -f "$item")" "$dest/$base_name"
        else
            # If item is a file, create a symlink to the original
            ln -s "$item" "$dest/$base_name"
        fi
    done
}

# Call the recursive function to start the process
duplicate_structure "$from_path" "$to_path"
