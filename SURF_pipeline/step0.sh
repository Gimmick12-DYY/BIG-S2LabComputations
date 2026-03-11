#!/bin/bash
# step0.sh

set -euo pipefail

Subject="${1:-}"
if [[ -z "${Subject}" ]]; then
  echo "ERROR: No Subject ID provided. Usage: bash step0.sh <SubjectID>" >&2
  exit 2
fi

# --- Debug helpers: print where we are when things fail ---
echo "=== DEBUG (step0.sh) ==="
echo "Subject: ${Subject}"
echo "PWD at start: $(pwd)"
echo "Host: $(hostname)"
echo "User: $(whoami)"
echo "Time: $(date)"
echo "========================"

# If anything errors, print PWD and key paths (so you know where it died)
trap 'echo "=== ERROR TRAP ===" >&2; echo "PWD on error: $(pwd)" >&2; echo "Subject: ${Subject}" >&2; echo "StudyFolder: ${StudyFolder:-UNSET}" >&2; echo "fsdir: ${fsdir:-UNSET}" >&2; echo "==================" >&2' ERR

# ------------------------------------------------------------------
# Original logic (with your updated StudyFolder + fsdir)
# ------------------------------------------------------------------

HCPPIPEDIR=/work/users/t/e/tengfei/HCPpipelines/
source "${HCPPIPEDIR}/gradunwarp-1.2.1/gradunwarp.build/bin/activate"

StudyFolder=/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf/data/
EnvironmentScript="${HCPPIPEDIR}/Examples/Scripts/SetUpHCPPipeline.sh"
source "${EnvironmentScript}"

HCPPIPEDIR_Templates="${HCPPIPEDIR}/global/templates"

# Your current freesurfer path assumption:
fsdir="${StudyFolder}/${Subject}/freesurfer"

# Keep this export (as in your file)
export PATH=/work/users/t/e/tengfei/UKBRetest_HCP_Surface/updated20240223/MSM_HOCR/Centos/:${PATH}

# --- More debug right before ciftify runs ---
echo "PWD before ciftify: $(pwd)"
echo "StudyFolder: ${StudyFolder}"
echo "fsdir: ${fsdir}"
echo "Checking fsdir exists:"
ls -ld "${fsdir}" || echo "FS dir missing: ${fsdir}"

echo "Which ciftify_recon_all: $(which ciftify_recon_all || true)"
echo "Which python: $(which python || true)"
echo "========================"

# Run
ciftify_recon_all "${Subject}" \
  --ciftify-work-dir "${StudyFolder}/${Subject}/T1_out" \
  --fs-subjects-dir "${fsdir}" \
  --surf-reg MSMSulc

# (rest of your original commented lines kept)
#cifti_vis_recon_all subject ${Subject} --ciftify-work-dir ${StudyFolder}/${Subject}/T1_out
#/work/users/s/h/shiliny/Hongtu/pipline/UKBSurf/
#flirt -in ${StudyFolder}/${Subject}/rfMRI/rfMRI.nii.gz -ref ${StudyFolder}/${Subject}/T1w/T1.nii.gz \
#  -applyxfm -init ${StudyFolder}/${Subject}/rfMRI/example_func2highres.mat -out ${StudyFolder}/${Subject}/rfMRI/rfMRI1.nii.gz
#ciftify_subject_fmri ${StudyFolder}/${Subject}/rfMRI/rfMRI1.nii.gz ${Subject} \
#  --T1w-anat ${StudyFolder}/${Subject}/T1_out/${Subject}/T1w/T1w.nii.gz \
#  --surf-reg MSMSulc \
#  --ciftify-work-dir ${StudyFolder}/${Subject}/T1_out fMRI_out
#cifti_vis_fmri subject fMRI_out_method2 ${Subject} --ciftify-work-dir ${StudyFolder}/${Subject}/T1_out
