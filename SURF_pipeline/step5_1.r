##############################
#Step1: extract ROI timeseries for left hemisphere
##############################
cd /work/users/d/y/dyy12/WORK_UKB-Shape/UKBSurf # Change this to your PATH
module load r/4.3.2
module load freesurfer/6.0.0
module load fsl/6.0.6
HCPPIPEDIR=/work/users/t/e/tengfei/HCPpipelines/
MYBASEDIR=/work/users/t/e/tengfei/HCPpipelines/cifti
EnvironmentScript=${HCPPIPEDIR}/Examples/Scripts/SetUpHCPPipeline.sh;source ${EnvironmentScript}
HCPPIPEDIR_Templates=${HCPPIPEDIR}/global/templates
export PATH=$PATH:${MYBASEDIR}/ciftify/ciftify/bin
export PYTHONPATH=$PYTHONPATH:${MYBASEDIR}/ciftify
export CIFTIFY_TEMPLATES=${MYBASEDIR}/ciftify/data
export HCP_DATA=/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf/data/ # Change this to your PATH
R
sub0=dir('data')
fmriPath='fMRI_out_method5'
L=length(sub0)
for(ii in 1:L)
{
	if(ii%%10==0)print(L-ii)
	str0=paste0('cd ${HCP_DATA}/',sub0[ii],'/T1_out/',sub0[ii],'/MNINonLinear;wb_command -cifti-parcellate Results/',fmriPath,'/',fmriPath,'_Atlas_s10.dtseries.nii ')
	str0=paste0(str0,'${HCPPIPEDIR_Templates}/MSMAll/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii ')
	str0=paste0(str0,'COLUMN Results/',fmriPath,'/',fmriPath,'_Atlas_s10.ptseries.nii;')
	str0=paste0(str0,'wb_command -cifti-convert -to-text Results/',fmriPath,'/',fmriPath,'_Atlas_s10.ptseries.nii ')
	str0=paste0(str0,'Results/',fmriPath,'/',fmriPath,'_Atlas_s10.txt;')
	system(str0)
}
##############################
#Step2: extract ROI timeseries for right hemisphere
##############################
cd /work/users/d/y/dyy12/WORK_UKB-Shape/UKBSurf # Change this to your PATH
module load r/4.3.2
module load freesurfer/6.0.0
module load fsl/6.0.6
HCPPIPEDIR=/work/users/t/e/tengfei/HCPpipelines/
MYBASEDIR=/work/users/t/e/tengfei/HCPpipelines/cifti
EnvironmentScript=${HCPPIPEDIR}/Examples/Scripts/SetUpHCPPipeline.sh;source ${EnvironmentScript}
HCPPIPEDIR_Templates=${HCPPIPEDIR}/global/templates
export PATH=$PATH:${MYBASEDIR}/ciftify/ciftify/bin
export PYTHONPATH=$PYTHONPATH:${MYBASEDIR}/ciftify
export CIFTIFY_TEMPLATES=${MYBASEDIR}/ciftify/data
export HCP_DATA=/work/users/d/y/dyy12/WORK_UKB-Shape/UKBSurf/data/ # Change this to your PATH
R
sub0=dir('data')
L=length(sub0)
fmriPath='fMRI_out_method5'
for(ii in 1:L)
{
	if(ii%%10==0)print(L-ii)
	str0=paste0('cd ${HCP_DATA}/',sub0[ii],'/T1_out/',sub0[ii],'/MNINonLinear;wb_command -cifti-parcellate Results/',fmriPath,'/',fmriPath,'_Atlas_s10.dtseries.nii ')
	str0=paste0(str0,'${HCPPIPEDIR_Templates}/MSMAll/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii ')
	str0=paste0(str0,'COLUMN Results/',fmriPath,'/',fmriPath,'_Atlas_s10_R.ptseries.nii;')
	str0=paste0(str0,'wb_command -cifti-convert -to-text Results/',fmriPath,'/',fmriPath,'_Atlas_s10_R.ptseries.nii ')
	str0=paste0(str0,'Results/',fmriPath,'/',fmriPath,'_Atlas_s10_R.txt;')
	system(str0)
}
for(ii in 1:L)
{
if(ii%%10==0)print(L-ii)
A1=read.table(paste0('data/',sub0[ii],'/T1_out/',sub0[ii],'/MNINonLinear/Results/',fmriPath,'/',fmriPath,'_Atlas_s10.txt'),head=F)
A2=read.table(paste0('data/',sub0[ii],'/T1_out/',sub0[ii],'/MNINonLinear/Results/',fmriPath,'/',fmriPath,'_Atlas_s10_R.txt'),head=F)
A3=t(rbind(A1,A2))
write.table(A3,file=paste0('data/',sub0[ii],'/T1_out/',sub0[ii],'/MNINonLinear/Results/',fmriPath,'/',fmriPath,'_Atlas_s10_T.txt'),quote=F,row.names=F,col.names=F)
}

