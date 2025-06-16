#!/bin/bash

# Path setup
TARGET_DIR="/work/users/d/y/dyy12/WORK/code"
TARGET_FILE="$TARGET_DIR/ANTs_batAll.sh"

# Check if file exists
if [[ ! -f "$TARGET_FILE" ]]; then
  echo "File not found: $TARGET_FILE"
  exit 1
fi

# Extract all sbatch lines (skip the shebang)
SBATCH_LINES=$(grep "^sbatch " "$TARGET_FILE")
TOTAL_LINES=$(echo "$SBATCH_LINES" | wc -l)

# If 1000 or fewer sbatch lines, no need to split
if [[ "$TOTAL_LINES" -le 1000 ]]; then
  echo "No need to split. Total sbatch lines: $TOTAL_LINES"
  exit 0
fi

# Desired sbatch lines per output file
CHUNK_SIZE=1000
COUNT=1

# Split the sbatch lines into files with 1000 lines each
echo "$SBATCH_LINES" | split -l $CHUNK_SIZE -d - "$TARGET_DIR/ANTS_chunk_"

# Create output scripts with proper shebang
for chunk in "$TARGET_DIR"/ANTS_chunk_*; do
  OUTFILE="$TARGET_DIR/ANTs_batAll${COUNT}.sh"
  {
    echo "#!/bin/bash"
    cat "$chunk"
  } > "$OUTFILE"
  chmod +x "$OUTFILE"
  rm "$chunk"
  echo "Created: $OUTFILE"
  COUNT=$((COUNT + 1))
done
