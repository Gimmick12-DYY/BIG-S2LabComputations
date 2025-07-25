%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%   Process DTI data using FSL FDT toolbox on UNC Killdevil Sever   %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Jan    8, 2016 @ by TL

clear all;

FDTDir = '/work/users/d/y/dyy12/WORK_TBSS';         % directory containing the data folder and other files.  you need to change the directory accordingly
datadir= fullfile(FDTDir,'DWI');
codedir= fullfile(FDTDir,'code/');
subNames = dir(datadir);        % 'DWI': name of directory containing the imaging data files.  you need to change the directory accordingly
subNames = {subNames.name}';
subNames = subNames(3:end); % first two are sup-directory and current one
nn = size(subNames,1);
%remove empty folder
for ii=1:nn
    if  length(dir(fullfile(datadir,subNames{ii}))) < 3
	%rmdir(sprintf('%s/%s',datadir,subNames{ii}));
	end
end
subNames = dir(datadir);        
subNames = {subNames.name}';
subNames = subNames(3:end); 


nn = size(subNames,1);

mkdir(fullfile(FDTDir,'TBSS/FA'));
mkdir(fullfile(FDTDir,'TBSS/MD'));
mkdir(fullfile(FDTDir,'TBSS/V1'));
mkdir(fullfile(FDTDir,'TBSS/L1'));
mkdir(fullfile(FDTDir,'TBSS/MO'));
mkdir(fullfile(FDTDir,'TBSS/S0'));
mkdir(fullfile(FDTDir,'TBSS/V2'));
mkdir(fullfile(FDTDir,'TBSS/L2'));
mkdir(fullfile(FDTDir,'TBSS/L3'));
mkdir(fullfile(FDTDir,'TBSS/V3'));
mkdir(codedir);
delete(fullfile(codedir,'*'));

fid0 = fopen(sprintf('%s/FDT_batAll.sh',codedir),'w');
fprintf(fid0,'#!/bin/bash \n');

done=dir(fullfile(FDTDir,'TBSS/V3'));
done={done.name};
done=done(3:end);
done=cellfun(@(x)strsplit(x,'_V3.nii.gz'),done,'UniformOutput',0);
done=cellfun(@(x)x{1},done,'UniformOutput',0);

N=150;
K=ceil(nn/N);

for kk=1:K
    batNames = sprintf('%s/FDT_bat%i.sh',codedir,kk);
    fid = fopen(batNames,'w');
    fprintf(fid,'export FSLDIR=/nas/longleaf/apps/fsl/5.0.9/fsl/ \n');
    fprintf(fid,'source ${FSLDIR}/etc/fslconf/fsl.sh\n');
    fprintf(fid,'export PATH=${FSLDIR}/bin:${PATH}\n');
    flag=0;
	for ii=min(kk*N,nn)+((kk-1)*N+1)-(((kk-1)*N+1):min(kk*N,nn))
	if sum(strcmp(subNames{ii},done))~=0
	   continue;
	end 
	fprintf(fid,'cd %s/%s\n',datadir,subNames{ii});
	flag=1;
    % fprintf(fid,'gzip *.nii\n');                      % uncomment this line if the image file is unzipped
    % fprintf(fid,'mv *.nii.gz nodif.nii.gz\n');
    % fprintf(fid,'mv *.bvec bvecs\n');
    % fprintf(fid,'mv *.bval bvals\n');
    % fprintf(fid,'eddy_correct nodif.nii data.nii.gz 0\n');
    % fprintf(fid,'bet nodif.nii nodif_brain_mask.nii.gz -f .1\n');
    % fprintf(fid,'bet data.nii nodif_brain_mask.nii.gz -f .1\n');
    % fprintf(fid,'dtifit -k data.nii.gz -o dti -m nodif_brain_mask.nii.gz -r bvecs -b bvals\n');
    fprintf(fid,'cp %s/%s/dti_FA.nii.gz %s/TBSS/FA/%s_FA.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_MD.nii.gz %s/TBSS/MD/%s_MD.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_V1.nii.gz %s/TBSS/V1/%s_V1.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_L1.nii.gz %s/TBSS/L1/%s_L1.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_L2.nii.gz %s/TBSS/L2/%s_L2.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_L3.nii.gz %s/TBSS/L3/%s_L3.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_V2.nii.gz %s/TBSS/V2/%s_V2.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_V3.nii.gz %s/TBSS/V3/%s_V3.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_MO.nii.gz %s/TBSS/MO/%s_MO.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    fprintf(fid,'cp %s/%s/dti_S0.nii.gz %s/TBSS/S0/%s_S0.nii.gz\n',datadir,subNames{ii},FDTDir,subNames{ii});
    end
    fclose(fid);
	if flag==1
		fprintf(fid0,'sh FDT_bat%i.sh\n',kk);;
	end
end

fclose(fid0);


%% end of code

