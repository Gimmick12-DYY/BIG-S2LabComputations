#!/bin/bash
set -euo pipefail

# Usage:
#   bash fix_freesurfer_layout.sh            # real run
#   bash fix_freesurfer_layout.sh --dry-run  # preview only
#
# Assumes you run it from: /work/users/d/y/dyy12/WORK_UKB-Shape/UKBSurf/
# or change DATA_DIR below.

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

DATA_DIR="./data"

if [[ ! -d "$DATA_DIR" ]]; then
  echo "ERROR: DATA_DIR not found: $DATA_DIR"
  exit 1
fi

echo "DATA_DIR = $DATA_DIR"
echo "DRY_RUN  = $DRY_RUN"
echo

# Loop over subject directories that look like numbers (UKB IDs)
for subj_path in "$DATA_DIR"/*; do
  [[ -d "$subj_path" ]] || continue
  subj="$(basename "$subj_path")"

  # Skip non-numeric folders if any
  if [[ ! "$subj" =~ ^[0-9]+$ ]]; then
    continue
  fi

  fs_dir="$subj_path/freesurfer"
  [[ -d "$fs_dir" ]] || continue

  target="$fs_dir/$subj"
  if [[ ! -d "$target" ]]; then
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY] mkdir -p '$target'"
    else
      mkdir -p "$target"
    fi
  fi

  # Move everything under freesurfer/ into freesurfer/<subj>/ except the target itself
  moved_any=0
  for item in "$fs_dir"/*; do
    # if freesurfer/ is empty, glob stays literal
    [[ -e "$item" ]] || continue

    # don't move the target folder into itself
    if [[ "$(basename "$item")" == "$subj" ]]; then
      continue
    fi

    moved_any=1
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY] mv '$item' '$target/'"
    else
      mv "$item" "$target/"
    fi
  done

  if [[ $moved_any -eq 1 ]]; then
    echo "OK: $subj  -> moved items into $target"
  else
    echo "SKIP: $subj  (nothing to move)"
  fi
done

echo
echo "Done."
