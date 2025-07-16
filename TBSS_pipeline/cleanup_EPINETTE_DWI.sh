#!/bin/bash

# For TBSS pipeline, this script checks for the presence of DWI files and organizes them into subject-specific directories.
# Not so useful for TBSS, but included for consistency with the ANTs pipeline.

# Define the base directory
base_dir="/work/users/d/y/dyy12/WORK_TBSS/DWI"

# Make sure we are in the current working directory where the DWI files are located
cd /work/users/d/y/dyy12/WORK_TBSS/DWI || exit

# Loop over all .nii.gz files
for nii_file in *.nii.gz; do
    # Strip the .nii.gz to get the base name
    base_name="${nii_file%.nii.gz}"

    # Create a directory with the base name under the destination path
    target_folder="${base_name}"
    mkdir -p "$target_folder"

    # Move the .nii.gz, .bval, and .bvec files into the new folder if they exist
    [ -f "${base_name}.nii.gz" ] && mv "${base_name}.nii.gz" "$target_folder/"
    [ -f "${base_name}.bval" ] && mv "${base_name}.bval" "$target_folder/"
    [ -f "${base_name}.bvec" ] && mv "${base_name}.bvec" "$target_folder/"
done