%cd /pine/scr/h/t/htzhu/UKB_restfMRI/data1;module load matlab/2020a;matlab -nodesktop -nosplash
%gencor('data1','/pine/scr/h/t/htzhu/UKB_restfMRI/',)
%'data','/work/users/t/e/tengfei/UKBRetest_HCP_Surface/','1041997_1'
function [yy]=gencor(data1,path0,ID,FWHM)
addpath /work/users/t/e/tengfei/Matlab_package/L1precision            
addpath /work/users/t/e/tengfei/Matlab_package/FSLNets   
addpath(sprintf('%s/etc/matlab',getenv('FSLDIR')))
addpath(sprintf('%s/bb_functional_pipeline/',getenv('BB_BIN_DIR')))
subj_dir=sprintf('%s/%s/%s/',path0,data1,ID);
D='360'
fmriPATH='fMRI_out_method5'
ts_dir=strcat(subj_dir,'T1_out/',ID,'/MNINonLinear/Results/',fmriPATH,'/');
disp(sprintf('%s/%s_Atlas_s%s_T.txt',ts_dir,fmriPATH,FWHM))
if ~exist(sprintf('%s/%s_Atlas_s%s_T.txt',ts_dir,fmriPATH,FWHM))
	disp('Wrong!Wrong!Wrong!')
	system(sprintf('mkdir %s/failed/',path0));
	system(sprintf('ln -s %s/%s/%s %s/failed/%s',path0,data1,ID,path0,ID));
else
	disp('Correct!!!')
	Atemp=dlmread(sprintf('%s/%s_Atlas_s%s_T.txt',ts_dir,fmriPATH,FWHM));
	system(sprintf('mkdir %s/trash;mv %s/*.txt %s/trash; mv %s/trash/%s_Atlas_s%s_T.txt %s/',ts_dir,ts_dir,ts_dir,ts_dir,fmriPATH,FWHM,ts_dir));
	ts=nets_load(ts_dir,0.735,0,1,size(Atemp,1)); 
	ts.DD=1:360;
	r2zFULL=19.7177;
	r2zPARTIAL=18.8310;
	ts=nets_tsclean(ts,1);
	netmats1=  nets_netmats(ts,-r2zFULL,'corr');
	netmats2=  nets_netmats(ts,-r2zPARTIAL,'ridgep',0.5);
	clear NET; 
	grot=reshape(netmats1(1,:),ts.Nnodes,ts.Nnodes); 
	NET(1,:)=grot(triu(ones(ts.Nnodes),1)==1); 
	
	po=fopen(strcat(subj_dir, '/rfMRI/', sprintf('restfMRI_d%s_fullcorr_v1.txt',D)),'w');
	fprintf(po,[ num2str(NET(1,:),'%14.8f') '\n']);  
	fclose(po);

	clear NET; 

	grot=reshape(netmats2(1,:),ts.Nnodes,ts.Nnodes); 
	NET(1,:)=grot(triu(ones(ts.Nnodes),1)==1); 

	po=fopen(strcat(subj_dir, '/rfMRI/', sprintf('restfMRI_d%s_partialcorr_v1.txt',D)),'w'); 
	fprintf(po,[num2str(NET(1,:),'%14.8f') '\n']);  
	fclose(po);

	ts_std=std(ts.ts);

	po=fopen(strcat(subj_dir, '/rfMRI/', sprintf('restfMRI_d%s_NodeAmplitudes_v1.txt',D)),'w');

	fprintf(po,[num2str(ts_std(1,:),'%14.8f') '\n']);  
	fclose(po);
end
clear all
close all
clc
exit
return
end
% cd /pine/scr/t/e/tengfei/ukb_taskfmri/Phase12
% ss=dir('failed');
% ss={ss.name}';
% ss=ss(3:end);
% l=length(ss);
% for i=1:l
% if exist(sprintf('failed/%s/fMRI/unusable',ss{i}))
% disp(i)
% system(sprintf('rm -r failed/%s',ss{i}))
% end
% end