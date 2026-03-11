set -euo pipefail

ROOT="/work/users/d/y/dyy12/WORK_UKB-Shape/UKBSurf"
RESULT="${ROOT}/data"

ts() { date +"%F %T"; }

deleted_dtseries=0
deleted_rfmri=0
subjects=0

echo "[$(ts)] Cleaning files under: ${RESULT}"

for sdir in "${RESULT}"/*; do
  [[ -d "$sdir" ]] || continue
  SID="$(basename "$sdir")"
  [[ "$SID" =~ ^[0-9]+$ ]] || continue

  subjects=$((subjects + 1))

  # 1) Delete s10.dtseries
  DTFILE="${sdir}/Results/fMRI_out_method5/fMRI_out_method5_Atlas_s10.dtseries.nii"
  if [[ -f "$DTFILE" ]]; then
    rm -f "$DTFILE"
    deleted_dtseries=$((deleted_dtseries + 1))
    echo "[$(ts)] ${SID}: deleted $(basename "$DTFILE")"
  fi

  # 2) Delete rfMRI.nii.gz
  RFFILE="${sdir}/rfMRI/rfMRI.nii.gz"
  if [[ -f "$RFFILE" ]]; then
    rm -f "$RFFILE"
    deleted_rfmri=$((deleted_rfmri + 1))
    echo "[$(ts)] ${SID}: deleted $(basename "$RFFILE")"
  fi
done

echo
echo "Cleanup complete."
echo "Subjects scanned:           ${subjects}"
echo "Deleted s10.dtseries files: ${deleted_dtseries}"
echo "Deleted rfMRI.nii.gz files: ${deleted_rfmri}"
