#!/bin/bash

for file in GENCORE*_T1*.nii.gz; do
  # Extract parts using regex
  num1=$(echo "$file" | sed -E 's/GENCORE([0-9]+)_T1.*/\1/')
  num2=$(echo "$file" | sed -E 's/.*_T1(_GD)?_([0-9]{8})_.*/\2/')
  remainder=$(echo "$file" | sed -E 's/.*_T1(_GD)?_[0-9]{8}_(.*)\.nii\.gz/\2/')

  # Compose folder name
  folder="${num1}_${num2}_${remainder}"
  mkdir -p "$folder"

  # Move and rename the file
  mv "$file" "$folder/T1.nii.gz"
done
