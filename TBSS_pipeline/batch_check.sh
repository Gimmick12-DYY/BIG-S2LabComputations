#!/bin/bash

# For TBSS pipeline, this script checks for the presence of DWI files and organizes them into subject-specific directories.

# Set target file and directory
TARGET_DIR="/work/users/d/y/dyy12/WORK_TBSS/code"
TARGET_FILE="$TARGET_DIR/FDT_batAll.sh"

# Check if file exists
if [[ ! -f "$TARGET_FILE" ]]; then
  echo "File not found: $TARGET_FILE"
  exit 1
fi

# Count total number of qsub lines (ignore the shebang)
TOTAL_LINES=$(grep "^sbatch" "$TARGET_FILE" | wc -l)

# If 1000 or fewer sbatch lines, no need to split
if [[ "$TOTAL_LINES" -le 1000 ]]; then
  echo "No need to split. Total sbatch lines: $TOTAL_LINES"
  exit 0
fi

# Desired lines per output file
CHUNK_SIZE=1000
COUNT=1

# Create temporary chunks directly from grep output
mkdir -p "$TARGET_DIR"
grep "^sbatch" "$TARGET_FILE" | split -l $CHUNK_SIZE -d - "$TARGET_DIR/FDT_chunk_"

# Create output scripts with proper shebang
for chunk in "$TARGET_DIR"/FDT_chunk_*; do
  OUTFILE="$TARGET_DIR/FDT_batAll${COUNT}.sh"
  {
    echo "#!/bin/bash"
    cat "$chunk"
  } > "$OUTFILE"
  
  chmod +x "$OUTFILE"
  rm "$chunk"
  echo "Created: $OUTFILE"
  COUNT=$((COUNT + 1))
done