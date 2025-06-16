#!/bin/bash

# Usage: ./cleanup.sh /path/to/parent_directory

PARENT_DIR="$1"

if [ -z "$PARENT_DIR" ]; then
  echo "Usage: $0 /path/to/parent_directory"
  exit 1
fi

echo "Cleaning directory: $PARENT_DIR"

# Delete all files that are NOT T1.nii.gz
find "$PARENT_DIR" -type f ! -name 'T1.nii.gz' -exec rm -f {} +

# Delete all directories (regardless of name)
find "$PARENT_DIR" -mindepth 1 -type d -exec rm -rf {} +
