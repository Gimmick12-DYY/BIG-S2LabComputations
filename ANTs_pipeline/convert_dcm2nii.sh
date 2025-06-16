#!/bin/bash

INPUT_DIR="HABS-04-16-25/HABS_HD_ds2"       #Path to input directory
OUTPUT_DIR="HABS-04-16-25/HABS_HD_ds2_nii"  #Path to output directory

find "$INPUT_DIR" -type d | while read -r dir; do
    if compgen -G "$dir/*.dcm" > /dev/null; then
        # Extract subject ID (first 4-digit number in path)
        subject_id=$(echo "$dir" | grep -oP '\d{4}' | head -1)
        outdir="$OUTPUT_DIR/$subject_id"

        mkdir -p "$outdir"

        echo "Converting: $dir -> $outdir"
        dcm2niix -z y -f T1 -o "$outdir" "$dir"
    fi
done