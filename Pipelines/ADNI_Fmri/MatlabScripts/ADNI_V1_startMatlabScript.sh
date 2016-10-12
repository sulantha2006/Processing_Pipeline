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

queue=veryfast.q
echo "qsub -j y -o $4/FMRI_LOG_$1.log -V -cwd -q $queue -N FMRI_$1 Pipelines/ADNI_Fmri/MatlabScripts/ADNI_V1_startMatlabScriptOperation.sh $1 $2 $3 $4 $5 $6"
export MATLABROOT=/opt/matlab12b
export MATLAB_JAVA=/opt/matlab12b/sys/java/jre/glnxa64/jre/
qsub -j y -o $4/FMRI_LOG_$1.log -V -cwd -q $queue -N FMRI_$1 Pipelines/ADNI_Fmri/MatlabScripts/ADNI_V1_startMatlabScriptOperation.sh $1 $2 $3 $4 $5 $6