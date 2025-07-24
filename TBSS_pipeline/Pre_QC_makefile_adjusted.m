%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%   Process DTI data using QC toolbox on UNC Killdevil Sever   %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Jan    8, 2016 @ by CH

clear all;


FDTDir = '/work/users/d/y/dyy12/WORK_TBSS/TBSS';   %PATH to change       

subNames = dir(fullfile(FDTDir,'V1/*.nii.gz'));
subNames = {subNames.name};
subNames = cellfun(@(x)strsplit(x,'_V1.nii.gz'),subNames,'UniformOutput',0);
subNames = cellfun(@(x)x{1},subNames,'UniformOutput',0);

subNames1 = dir(fullfile(FDTDir,'FA/*.nii.gz'));
subNames1 = {subNames1.name}';
subNames1 = cellfun(@(x)strsplit(x,'_FA.nii.gz'),subNames1,'UniformOutput',0);
subNames1 = cellfun(@(x)x{1},subNames1,'UniformOutput',0);

subNames=intersect(subNames,subNames1);
subNames1=dir(sprintf('%s/Pre_QC/QC_FA_V1',FDTDir));subNames1 = {subNames1.name}';
subNames1 = cellfun(@(x)strsplit(x,'.png'),subNames1,'UniformOutput',0);
subNames1 = cellfun(@(x)x{1},subNames1,'UniformOutput',0);
subNames=setdiff(subNames,subNames1)

nn = size(subNames,1);

mkdir(fullfile(FDTDir,'Pre_QC'));

done=dir(fullfile(FDTDir,'Pre_QC/QC_FA_V1'));
done={done.name}';
done=done(3:end);

fid1=fopen(sprintf('%s/Pre_QC/Subject_Path_Info.txt',FDTDir),'wt'); % Error here again missing a "/"
fprintf(fid1,'subjectID\tFAimage\tV1image\n');
for ii=1:nn
    if sum(strcmp(subNames{ii},done))~=0
	continue;
	end
    fprintf(fid1,'%s\t%s/FA/%s_FA.nii.gz\t%s/V1/%s_V1.nii.gz\n',subNames{ii},FDTDir,subNames{ii},FDTDir,subNames{ii});
end
fclose(fid1);

fprintf('+++++++Process DTI data: QC file generation is finished!!+++++++\n');


clear all;

%% end of code