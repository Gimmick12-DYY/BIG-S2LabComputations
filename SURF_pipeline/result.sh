#!/usr/bin/env bash
# Collect UKBSurf outputs into result/ + count missing required items

set -euo pipefail

ROOT="/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf" # Change root
DATA="${ROOT}/data"
OUT="${ROOT}/result"

mkdir -p "$OUT"

ts() { date +"%F %T"; }

copy_glob() {
  local pattern="$1"
  local destdir="$2"

  mkdir -p "$destdir"

  shopt -s nullglob
  local matches=($pattern)
  shopt -u nullglob

  if ((${#matches[@]} == 0)); then
    return 1
  fi

  cp -p "${matches[@]}" "$destdir"/
  return 0
}

copy_dir() {
  local srcdir="$1"
  local destdir="$2"

  if [[ ! -d "$srcdir" ]]; then
    return 1
  fi

  mkdir -p "$(dirname "$destdir")"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --no-perms --no-owner --no-group "$srcdir"/ "$destdir"/
  else
    mkdir -p "$destdir"
    cp -a "$srcdir"/. "$destdir"/
  fi
  return 0
}

REPORT_DIR="${OUT}/_reports"
mkdir -p "$REPORT_DIR"
SUMMARY_CSV="${REPORT_DIR}/missing_summary.csv"
DETAIL_LOG="${REPORT_DIR}/missing_detail.log"

echo "subject_id,missing_count" > "$SUMMARY_CSV"
: > "$DETAIL_LOG"

total_subjects=0
total_missing=0

echo "[$(ts)] Scanning subjects under: $DATA"

for sdir in "$DATA"/*; do
  [[ -d "$sdir" ]] || continue
  SID="$(basename "$sdir")"
  [[ "$SID" =~ ^[0-9]+$ ]] || continue

  total_subjects=$((total_subjects + 1))
  miss=0

  DEST_BASE="${OUT}/${SID}"           # The directory follow this format: root/data/{subid}/T1_out/{subid}/MNINonLinear/Results/fMRI_out_method5, etc. change as needed.
  DEST_RFMRI="${DEST_BASE}/rfMRI"
  DEST_RES="${DEST_BASE}/Results/fMRI_out_method5"
  DEST_FSAVG="${DEST_BASE}/fsaverage_LR32k"

  # ---------- (B) ROI pair connectivity ----------
  if ! copy_glob "${DATA}/${SID}/rfMRI/restfMRI_d360_fullcorr_v1.txt" "$DEST_RFMRI"; then
    miss=$((miss + 1)); echo "[$(ts)] ${SID} MISSING: data/${SID}/rfMRI/restfMRI_d360_fullcorr_v1.txt" >> "$DETAIL_LOG"
  fi
  if ! copy_glob "${DATA}/${SID}/rfMRI/restfMRI_d360_NodeAmplitudes_v1.txt" "$DEST_RFMRI"; then
    miss=$((miss + 1)); echo "[$(ts)] ${SID} MISSING: data/${SID}/rfMRI/restfMRI_d360_NodeAmplitudes_v1.txt" >> "$DETAIL_LOG"
  fi

  copy_glob "${DATA}/${SID}/rfMRI/restfMRI_d360_partialcorr_v1.txt" "$DEST_RFMRI" >/dev/null 2>&1 || true

  # ---------- (C) Vertex + ROI timeseries ----------
  RESROOT="${DATA}/${SID}/T1_out/${SID}/MNINonLinear/Results/fMRI_out_method5"

  if ! copy_glob "${RESROOT}/fMRI_out_method5_Atlas_s0.dtseries.nii" "$DEST_RES"; then
    miss=$((miss + 1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s0.dtseries.nii" >> "$DETAIL_LOG"
  fi
  if ! copy_glob "${RESROOT}/trash/fMRI_out_method5_Atlas_s0_T.txt" "$DEST_RES"; then
    miss=$((miss + 1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s0_T.txt" >> "$DETAIL_LOG"
  fi
  if ! copy_glob "${RESROOT}/fMRI_out_method5_Atlas_s10_T.txt" "$DEST_RES"; then
    miss=$((miss + 1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s10_T.txt" >> "$DETAIL_LOG"
  fi

  # If you ALSO want ptseries in the results, uncomment these 4 lines:
  # copy_glob "${RESROOT}/fMRI_out_method5_Atlas_s0.ptseries.nii"  "$DEST_RES" || { miss=$((miss+1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s0.ptseries.nii"  >> "$DETAIL_LOG"; }
  # copy_glob "${RESROOT}/fMRI_out_method5_Atlas_s10.ptseries.nii" "$DEST_RES" || { miss=$((miss+1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s10.ptseries.nii" >> "$DETAIL_LOG"; }
  # copy_glob "${RESROOT}/fMRI_out_method5_Atlas_s0_R.ptseries.nii"  "$DEST_RES" || { miss=$((miss+1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s0_R.ptseries.nii"  >> "$DETAIL_LOG"; }
  # copy_glob "${RESROOT}/fMRI_out_method5_Atlas_s10_R.ptseries.nii" "$DEST_RES" || { miss=$((miss+1)); echo "[$(ts)] ${SID} MISSING: ${RESROOT}/fMRI_out_method5_Atlas_s10_R.ptseries.nii" >> "$DETAIL_LOG"; }

  # ---------- (D) Surface/thickness map directory ----------
  FSROOT="${DATA}/${SID}/T1_out/${SID}/MNINonLinear/fsaverage_LR32k"
  if ! copy_dir "$FSROOT" "$DEST_FSAVG"; then
    miss=$((miss + 1)); echo "[$(ts)] ${SID} MISSING: ${FSROOT}/" >> "$DETAIL_LOG"
  fi

  echo "${SID},${miss}" >> "$SUMMARY_CSV"
  total_missing=$((total_missing + miss))

  echo "[$(ts)] ${SID}: missing=${miss}"
done

echo
echo "Done."
echo "Subjects scanned: ${total_subjects}"
echo "Total missing items counted: ${total_missing}"
echo "Summary CSV:  ${SUMMARY_CSV}"
echo "Detail log:   ${DETAIL_LOG}"
