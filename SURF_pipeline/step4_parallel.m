%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%   cifti_vis_fmri batching on Longleaf (split All.sh)   %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Original: March 8, 2016 @ by CH
% Updated: split All.sh into All_*.sh, max 1000 sbatch lines each
%          use YOUR conda env (surf2) instead of Tengfei's env

clear all;

%% ====================== USER CONFIG ======================
Home = '/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf/';   % Home PATH

USE_ACCOUNT  = false;                 % <<< TOGGLE HERE
ACCOUNT_NAME = 'rc_htzhu_pi';         % Longleaf account with extra quota

conda_env = '/work/users/d/y/dyy12/BIG-S2/conda_envs/surf2';     % <<< IMPORTANT
time_str  = '00:19:59';
mem_str   = '32000';

outpath   = 'fMRI_out_method5';

N = 20;                               % subjects per job
MAX_JOBS_PER_ALL = 1000;              % max sbatch lines per All_*.sh
%% =========================================================

cd(Home);

codedir = fullfile(Home,'code5');
if ~exist(codedir, 'dir')
    mkdir(codedir);
else
    delete(fullfile(codedir,'*'));
end

datadir = sprintf('%s/data', Home);

subNames = dir(datadir);
subNames = {subNames.name}';
subNames = subNames(3:end); % remove '.' and '..'
nn = numel(subNames);

% ===================== split All.sh =====================
all_idx = 0;
job_cnt = 0;

all_name = sprintf('%s/All_%d.sh', codedir, all_idx);
fid2 = fopen(all_name, 'w');
fprintf(fid2,'#!/bin/bash\n');
fprintf(fid2,'set -euo pipefail\n\n');
% ========================================================

K = ceil(nn/N);

for kk = 1:K

    bat_name = sprintf('%s/bat%i.pbs', codedir, kk);
    fid21 = fopen(bat_name, 'w');

    fprintf(fid21,'#!/bin/bash\n');
    fprintf(fid21,'#SBATCH --ntasks=1\n');
    fprintf(fid21,'#SBATCH --time=%s\n', time_str);
    fprintf(fid21,'#SBATCH --mem=%s\n', mem_str);

    if USE_ACCOUNT
        fprintf(fid21,'#SBATCH --account=%s\n', ACCOUNT_NAME);
    end

    fprintf(fid21,'#SBATCH --wrap=bat_%i\n', kk);

    % ===== Base modules =====
    fprintf(fid21,'module purge; module load freesurfer/6.0.0; module load fsl/6.0.7;\n');

    % ===== conda environment (surf2) =====
    fprintf(fid21,'module load anaconda\n');
    fprintf(fid21,'source "$(conda info --base)/etc/profile.d/conda.sh"\n');
    fprintf(fid21,'conda activate %s\n\n', conda_env);

    fprintf(fid21,'export PYTHONNOUSERSITE=1\n');
    fprintf(fid21,'#unset PYTHONPATH\n');
    fprintf(fid21,'#hash -r\n\n');

    flag = 0;

    for ii = min(kk*N,nn)+((kk-1)*N+1)-(((kk-1)*N+1):min(kk*N,nn))
        ID = subNames{ii};

        % Skip if already done (same condition as original cifti_vis script)
        done_png = sprintf('%s/%s/T1_out/qc_fmri/%s_%s/SAL_conn.png', datadir, ID, ID, outpath);
        if exist(done_png, 'file')
            continue;
        end

        disp(ii);

        % ===== HCP pipelines setup =====
        fprintf(fid21,'cd %s; Subject=%s\n', Home, ID);
        fprintf(fid21,'HCPPIPEDIR=/work/users/t/e/tengfei/HCPpipelines/\n');

        fprintf(fid21,'source ${HCPPIPEDIR}/gradunwarp-1.2.1/gradunwarp.build/bin/activate\n');

        fprintf(fid21,'StudyFolder=%s/\n', datadir);
        fprintf(fid21,'EnvironmentScript=${HCPPIPEDIR}/Examples/Scripts/SetUpHCPPipeline.sh\n');
        fprintf(fid21,'source ${EnvironmentScript}\n');
        fprintf(fid21,'HCPPIPEDIR_Templates=${HCPPIPEDIR}/global/templates\n');
        fprintf(fid21,'fsdir=${StudyFolder}/${Subject}/T1w/freesurfer\n');
        fprintf(fid21,'export PATH=%s/MSM_HOCR_v2/Centos/:${PATH}\n', Home);
        fprintf(fid21,'cifti_vis_fmri subject %s ${Subject} --ciftify-work-dir ${StudyFolder}/${Subject}/T1_out\n', outpath);

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
        % ===============================================================

        fprintf(fid2,'sbatch %s/bat%i.pbs\n', codedir, kk);
        job_cnt = job_cnt + 1;

    else
        system(sprintf('rm -f %s', bat_name));
    end

end

fclose(fid2);
system(sprintf('chmod +x %s', all_name));

fprintf('Done.\n');
fprintf('Generated All_*.sh scripts in: %s\n', codedir);
fprintf('Submit with: bash %s/All_0.sh (then All_1.sh, ... if they exist)\n', codedir);
