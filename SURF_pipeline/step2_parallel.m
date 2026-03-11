%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%   Process FA data using FSL/TBSS_1 on BIOS Sever     %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% March  8, 2016 @ by CH
% Modified: conda env activation for ciftify (Shilin)
% Modified: split All.sh into All_*.sh with <=1000 jobs each (Yuyang)

clear all;

USE_ACCOUNT  = false;                 % <<< TOGGLE HERE
ACCOUNT_NAME = 'rc_htzhu_pi';         % Longleaf account with extra quota

Home = '/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf';
cd(Home);

codedir = fullfile(Home,'code');
if ~exist(codedir, 'dir')
    mkdir(codedir);
end
system(sprintf('rm -f %s/*', codedir));   % clear old generated files

datadir  = sprintf('%s/data', Home);
subNames = dir(datadir);
subNames = {subNames.name}';
subNames = subNames(3:end);   % remove . and ..

nn = size(subNames,1);

% ===================== split All.sh =====================
MAX_JOBS_PER_ALL = 1000;   % max sbatch lines per All_*.sh
all_idx = 0;
job_cnt = 0;

all_name = sprintf('%s/All_%d.sh', codedir, all_idx);
fid2 = fopen(all_name, 'w');
fprintf(fid2, '#!/bin/bash\n');
fprintf(fid2, 'set -euo pipefail\n\n');
% =============================================================

N = 60;
K = ceil(nn/N);

for kk = 1:K
    fid21 = fopen(sprintf('%s/bat%i.pbs', codedir, kk), 'w');

    fprintf(fid21,'#!/bin/bash\n');
    fprintf(fid21,'#SBATCH --ntasks=1\n');
    fprintf(fid21,'#SBATCH --time=02:59:59\n');
    fprintf(fid21,'#SBATCH --mem=32000\n');

    if USE_ACCOUNT
        fprintf(fid21,'#SBATCH --account=%s\n', ACCOUNT_NAME);
    end

    fprintf(fid21,'#SBATCH --wrap=bat_%i\n', kk);

    % ===== Base modules =====
    fprintf(fid21,'module purge\n');
    fprintf(fid21,'module load anaconda\n');
    fprintf(fid21,'module load freesurfer/6.0.0\n');
    fprintf(fid21,'module load fsl/6.0.7\n');

    % ===== Activate conda env with working ciftify =====
    fprintf(fid21,'source "$(conda info --base)/etc/profile.d/conda.sh"\n');
    fprintf(fid21,'conda activate /work/users/s/h/shiliny/conda_envs/surf2\n\n');

    flag = 0;

    for ii = min(kk*N,nn)+((kk-1)*N+1)-(((kk-1)*N+1):min(kk*N,nn))
        ID = subNames{ii};

        % prerequisite exists
        if ~exist(sprintf('%s/%s/T1_out/%s/MNINonLinear/fsaverage_LR32k/%s.BA_exvivo.32k_fs_LR.dlabel.nii',...
                datadir,ID,ID,ID), 'file')
            continue;
        end

        % already finished qc
        if exist(sprintf('%s/%s/T1_out/qc_recon_all/%s/thickness.png',...
                datadir,ID,ID), 'file')
            continue;
        end

        disp(ii);

        fprintf(fid21,'cd %s\n', Home);
        fprintf(fid21,'Subject=%s\n', ID);
        fprintf(fid21,'HCPPIPEDIR=/work/users/t/e/tengfei/HCPpipelines/\n');
        fprintf(fid21,'source ${HCPPIPEDIR}/gradunwarp-1.2.1/gradunwarp.build/bin/activate\n');
        fprintf(fid21,'StudyFolder=%s/\n', datadir);
        fprintf(fid21,'EnvironmentScript=${HCPPIPEDIR}/Examples/Scripts/SetUpHCPPipeline.sh\n');
        fprintf(fid21,'source ${EnvironmentScript}\n');
        fprintf(fid21,'HCPPIPEDIR_Templates=${HCPPIPEDIR}/global/templates\n');
        fprintf(fid21,'fsdir=${StudyFolder}/${Subject}/T1w/freesurfer\n');
        fprintf(fid21,'export PATH=%s/MSM_HOCR_v2/Centos/:${PATH}\n', Home);

        % ===== ciftify visualization =====
        fprintf(fid21,'cifti_vis_recon_all subject ${Subject} --ciftify-work-dir ${StudyFolder}/${Subject}/T1_out\n\n');

        flag = 1;
    end

    fclose(fid21);

    if flag == 1
        % ===================== auto-split =====================
        if job_cnt >= MAX_JOBS_PER_ALL
            fclose(fid2);
            system(sprintf('chmod +x %s', all_name));

            all_idx = all_idx + 1;
            job_cnt = 0;

            all_name = sprintf('%s/All_%d.sh', codedir, all_idx);
            fid2 = fopen(all_name, 'w');
            fprintf(fid2, '#!/bin/bash\n');
            fprintf(fid2, 'set -euo pipefail\n\n');
        end
        % ===========================================================

        fprintf(fid2,'sbatch %s/bat%i.pbs\n', codedir, kk);
        job_cnt = job_cnt + 1;
    end
end

% close + chmod the last All_*.sh
fclose(fid2);
system(sprintf('chmod +x %s', all_name));

fprintf('Done.\n');
fprintf('Submit jobs via: bash %s/All_0.sh (then All_1.sh, ... if created)\n', codedir);
