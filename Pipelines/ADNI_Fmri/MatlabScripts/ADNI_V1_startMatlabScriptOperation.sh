#!/bin/sh
#THIS SCRIPT IS USED TO RUN ONE BEAST EXECUTION ON QSUB
####1 -> ID
####2 -> COMMAND
####3 -> NIAK OUTPUT LOCATION
####4 -> LOG DIR
#### FOR SEND MESSAGE TO HANDLER
####5 -> HOST
####6 -> PORT
#### ADDITIONAL FEATURES
####7+ -> GENERATED FILES
source /opt/minc-1.9.15/minc-toolkit-config.sh
id=$1
command=$2
outputFolder=$3
logDir=$4
host=$5
port=$6

#### SEND MESSAGE TO QSUB JOB HANLDER - JOB STARTING
echo ${id}_Start | nc -w 0 ${host} ${port}
#### SEND MESSAGE TO QSUB JOB HANDLER IN PIPELINE MANAGER
echo "/opt/matlab12b/bin/matlab -nodisplay -nosplash -r \"addpath('/home/sulantha/PycharmProjects/Processing_Pipeline/Config/../Pipelines/ADNI_Fmri/MatlabScripts');run('${command}');exit\""
export MATLABROOT=/opt/matlab12b
export MATLAB_JAVA=/opt/matlab12b/sys/java/jre/glnxa64/jre/
/opt/matlab12b/bin/matlab -nodisplay -nosplash -r "addpath('/home/sulantha/PycharmProjects/Processing_Pipeline/Config/../Pipelines/ADNI_Fmri/MatlabScripts');run('${command}');exit"


#### SEND MESSAGE TO QSUB JOB HANDLER IN PIPELINE MANAGER
if [[ -f ${outputFolder}/anat/func_subject1_mean_stereonl.mnc ]]
 then
    echo ${id}_Success | nc -w 0 ${host} ${port}
 else
    echo ${id}_Fail | nc -w 0 ${host} ${port}
fi

