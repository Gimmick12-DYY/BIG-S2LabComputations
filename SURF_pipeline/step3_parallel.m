%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%   Process FA data using FSL/TBSS_1 on BIOS Sever     %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% March  8, 2016 @ by CH
% Modified: split All.sh into All_*.sh, max 1000 sbatch lines each

clear all;

USE_ACCOUNT  = false;                 % <<< TOGGLE HERE
ACCOUNT_NAME = 'rc_htzhu_pi';         % Longleaf account with extra quota

Home = '/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf';   % PATH to change
cd(Home);

codedir = fullfile(Home,'code');
if ~exist(codedir, 'dir')
    mkdir(codedir);
end
system(sprintf('rm -f %s/*', codedir));

datadir = sprintf('%s/data', Home);

subNames = dir(datadir);
subNames = {subNames.name}';
subNames = subNames(3:end); % remove '.' and '..'

nn = size(subNames,1);

% ===================== split All.sh =====================
MAX_JOBS_PER_ALL = 1000;   % max sbatch lines per All_*.sh
all_idx = 0;
job_cnt = 0;

all_name = sprintf('%s/All_%d.sh', codedir, all_idx);
fid2 = fopen(all_name, 'w');
fprintf(fid2,'#!/bin/bash\n');
fprintf(fid2,'set -euo pipefail\n\n');
% =============================================================

N = 3;
K = ceil(nn/N);

for kk = 1:K

    fid21 = fopen(sprintf('%s/bat%i.pbs', codedir, kk), 'w');

    fprintf(fid21,'#!/bin/bash\n');
    fprintf(fid21,'#SBATCH --ntasks=1\n');
    fprintf(fid21,'#SBATCH --time=14:59:59\n'); % N=1 for 3hours; 8 for 24 hours
    fprintf(fid21,'#SBATCH --mem=28000\n');

    if USE_ACCOUNT
        fprintf(fid21,'#SBATCH --account=%s\n', ACCOUNT_NAME);
    end

    fprintf(fid21,'#SBATCH --wrap=bat_%i\n', kk);

    % ===== Base modules =====
    fprintf(fid21,'module purge; module load freesurfer/6.0.0; module load fsl/6.0.7;\n');

    % ===== Activate conda env with working ciftify =====
    fprintf(fid21,'module load anaconda\n'); % important: ensure conda exists in batch env
    fprintf(fid21,'source "$(conda info --base)/etc/profile.d/conda.sh"\n');
    fprintf(fid21,'conda activate /work/users/s/h/shiliny/conda_envs/surf2\n\n');

    % avoid accidentally using ~/.local
    fprintf(fid21,'export PYTHONNOUSERSITE=1\n');
    fprintf(fid21,'#unset PYTHONPATH\n');
    fprintf(fid21,'#hash -r\n\n');

    flag = 0;

    for ii = min(kk*N,nn)+((kk-1)*N+1)-(((kk-1)*N+1):min(kk*N,nn))
        ID = subNames{ii};

        % if already finished, skip
        if exist(sprintf('%s/%s/T1_out/%s/MNINonLinear/Results/fMRI_out_method5/fMRI_out_method5_Atlas_s10.dtseries.nii', ...
                datadir, ID, ID), 'file')
            continue;
        end

        disp(ii);

        fprintf(fid21,'cd %s; Subject=%s\n', Home, ID);
        fprintf(fid21,'HCPPIPEDIR=/work/users/t/e/tengfei/HCPpipelines/\n');
        fprintf(fid21,'source ${HCPPIPEDIR}/gradunwarp-1.2.1/gradunwarp.build/bin/activate\n');
        fprintf(fid21,'StudyFolder=%s/\n', datadir);
        fprintf(fid21,'EnvironmentScript=${HCPPIPEDIR}/Examples/Scripts/SetUpHCPPipeline.sh \n');
        fprintf(fid21,'source ${EnvironmentScript}\n');
        fprintf(fid21,'HCPPIPEDIR_Templates=${HCPPIPEDIR}/global/templates\n');
        fprintf(fid21,'export PATH=%s/MSM_HOCR_v2/Centos/:${PATH}\n', Home);

        fprintf(fid21,'rm -r %s/%s/T1_out/%s/MNINonLinear/Results/fMRI_out_method5/ \n', datadir, ID, ID);

        fprintf(fid21,'flirt -in ${StudyFolder}/${Subject}/T1w/T1.nii.gz -ref ${StudyFolder}/${Subject}/T1w/T1.nii.gz \\\n');
        fprintf(fid21,'-out ${StudyFolder}/${Subject}/T1w/T1x1_5.nii.gz  -applyisoxfm 1.5\n');

        fprintf(fid21,'flirt -in ${StudyFolder}/${Subject}/rfMRI/rfMRI.nii.gz -ref ${StudyFolder}/${Subject}/T1w/T1x1_5.nii.gz \\\n');
        fprintf(fid21,'-applyxfm -init ${StudyFolder}/${Subject}/rfMRI/example_func2highres.mat -out ${StudyFolder}/${Subject}/rfMRI/rfMRI1.nii.gz\n');

        fprintf(fid21,'ciftify_subject_fmri ${StudyFolder}/${Subject}/rfMRI/rfMRI1.nii.gz ${Subject} \\\n');
        fprintf(fid21,'--surf-reg MSMSulc --SmoothingFWHM 10 --DilateBelowPct 4 --ciftify-work-dir ${StudyFolder}/${Subject}/T1_out fMRI_out_method5 \n');

        fprintf(fid21,'rm %s/%s/rfMRI/rfMRI1.nii.gz\n', datadir, ID);
        fprintf(fid21,'rm %s/%s/T1_out/%s/MNINonLinear/Results/fMRI_out_method5/fMRI_out_method5.nii.gz\n', datadir, ID, ID);

        flag = 1;
    end

    fclose(fid21);

    if flag == 1
        % ===================== auto-split All_*.sh =====================
        if job_cnt >= MAX_JOBS_PER_ALL
            fclose(fid2);
            system(sprintf('chmod +x %s', all_name));

            all_idx = all_idx + 1;
            job_cnt = 0;

            all_name = sprintf('%s/All_%d.sh', codedir, all_idx);
            fid2 = fopen(all_name, 'w');
            fprintf(fid2,'#!/bin/bash\n');
            fprintf(fid2,'set -euo pipefail\n\n');
        end
        % ===================================================================

        fprintf(fid2,'sbatch %s/bat%i.pbs\n', codedir, kk);
        job_cnt = job_cnt + 1;

    else
        system(sprintf('rm -f %s/bat%i.pbs', codedir, kk));
    end

end

fclose(fid2);
system(sprintf('chmod +x %s', all_name));

fprintf('Done.\n');
fprintf('Generated All_*.sh scripts in: %s\n', codedir);
fprintf('Submit with: bash %s/All_0.sh (then All_1.sh, ... if they exist)\n', codedir);
