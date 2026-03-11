%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%   Process FA data using FSL/TBSS_1 on BIOS Sever     %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% March  8, 2016 @ by CH
 
clear all;

%% ================= USER CONFIG ================= %%
Home = '/work/users/d/y/dyy12/BIG-S2/WORK_UKB-Shape/UKBSurf/';  % Home PATH

USE_ACCOUNT  = false;                 % <<< TOGGLE HERE
ACCOUNT_NAME = 'rc_htzhu_pi';         % Longleaf account with extra quota

conda_env = '/work/users/d/y/dyy12/BIG-S2/conda_envs/surf2';
time_str  = '6:59:59';
mem_str   = '20000';
N         = 1;                       % subjects per job
MAX_JOBS_PER_ALL = 1000;             % max sbatch lines per All_*.sh
%% =============================================== %%

cd(Home);

codedir = fullfile(Home, 'code');
if ~exist(codedir, 'dir')
    mkdir(codedir);
else
    delete(fullfile(codedir, '*'));
end

logdir = fullfile(Home, 'logs');
if ~exist(logdir, 'dir')
    mkdir(logdir);
end

datadir = fullfile(Home, 'data');

subNames = dir(datadir);
subNames = {subNames.name}';
subNames = subNames(3:end);   % remove '.' and '..'

nn = size(subNames, 1);
K  = ceil(nn / N);

%% master submit scripts (chunked if > MAX_JOBS_PER_ALL)
all_idx = 0;     % All_*.sh index
job_cnt = 0;     % sbatch lines in current All_*.sh

all_name = fullfile(codedir, sprintf('All_%d.sh', all_idx));
fid2 = fopen(all_name, 'w');
fprintf(fid2, '#!/bin/bash\n');
fprintf(fid2, 'set -euo pipefail\n\n');

for kk = 1:K

    pbsfile = sprintf('%s/bat%i.pbs', codedir, kk);
    fid21 = fopen(pbsfile, 'w');

    %% ---------------- Slurm header ---------------- %%
    fprintf(fid21, '#!/bin/bash\n');
    fprintf(fid21, '#SBATCH --job-name=ukbsurf_%i\n', kk);
    fprintf(fid21, '#SBATCH --ntasks=1\n');
    fprintf(fid21, '#SBATCH --time=%s\n', time_str);
    fprintf(fid21, '#SBATCH --mem=%s\n', mem_str);

    % >>> OPTIONAL ACCOUNT LINE <<<
    if USE_ACCOUNT
        fprintf(fid21, '#SBATCH --account=%s\n', ACCOUNT_NAME);
    end

    fprintf(fid21, '#SBATCH --output=%s/ukbsurf_%i_%%j.out\n', logdir, kk);
    fprintf(fid21, '#SBATCH --error=%s/ukbsurf_%i_%%j.err\n\n', logdir, kk);

    %% ---------------- Environment ---------------- %%
    fprintf(fid21, 'module purge\n');
    fprintf(fid21, 'module load anaconda\n');
    fprintf(fid21, 'module load freesurfer/6.0.0\n');
    fprintf(fid21, 'module load fsl/6.0.7\n\n');

    fprintf(fid21, 'source "$(conda info --base)/etc/profile.d/conda.sh"\n');
    fprintf(fid21, 'conda activate %s\n\n', conda_env);

    % optional sanity check
    fprintf(fid21, 'echo "Python: $(which python)"\n');
    fprintf(fid21, 'echo "ciftify: $(which ciftify_recon_all)"\n\n');

    %% ---------------- Run step0 ---------------- %%
    fprintf(fid21, 'cd %s\n', Home);
    fprintf(fid21, 'dos2unix step0.sh\n\n');

    flag = 0;

    start_idx = (kk - 1) * N + 1;
    end_idx   = min(kk * N, nn);

    for ii = start_idx:end_idx
        ID = subNames{ii};

        % skip completed subjects
        if exist(sprintf('%s/%s/T1_out/%s/MNINonLinear/fsaverage_LR32k/%s.BA_exvivo.32k_fs_LR.dlabel.nii', ...
                datadir, ID, ID, ID), 'file')
            continue;
        end

        fprintf(fid21, 'rm -rf %s/%s/T1_out\n', datadir, ID);
        fprintf(fid21, 'bash step0.sh %s\n\n', ID);

        flag = 1;
    end

    fclose(fid21);

    if flag == 1
        % If current All_*.sh already has MAX_JOBS_PER_ALL jobs, start a new one
        if job_cnt >= MAX_JOBS_PER_ALL
            fclose(fid2);
            system(sprintf('chmod +x %s', all_name));

            all_idx = all_idx + 1;
            job_cnt = 0;

            all_name = fullfile(codedir, sprintf('All_%d.sh', all_idx));
            fid2 = fopen(all_name, 'w');
            fprintf(fid2, '#!/bin/bash\n');
            fprintf(fid2, 'set -euo pipefail\n\n');
        end

        fprintf(fid2, 'sbatch %s\n', pbsfile);
        job_cnt = job_cnt + 1;
    else
        system(sprintf('rm -f %s', pbsfile));
    end
end

fclose(fid2);
system(sprintf('chmod +x %s', all_name));

fprintf('Done.\n');
fprintf('USE_ACCOUNT = %d (%s)\n', USE_ACCOUNT, ACCOUNT_NAME);
fprintf('Generated %d submit scripts: All_0.sh ... All_%d.sh\n', all_idx+1, all_idx);
fprintf('Submit jobs via:\n');
fprintf('  bash %s/All_0.sh\n', codedir);
if all_idx >= 1
    fprintf('  bash %s/All_1.sh\n', codedir);
    fprintf('  ...\n');
end

