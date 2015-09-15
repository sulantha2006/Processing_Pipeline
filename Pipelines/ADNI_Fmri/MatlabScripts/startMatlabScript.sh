#!/bin/sh
#THIS SCRIPT IS USED TO RUN ONE BEAST EXECUTION ON QSUB
#$1 -> ID
#$2 -> COMMAND
#$3 -> NIAK OUTPUT LOCATION
#$4 -> LOG DIR
#### FOR SEND MESSAGE TO HANDLER
#$5 -> HOST
#$6 -> PORT
#### ADDITIONAL FEATURES
#$7+ -> GENERATED FILES

queue=heavy.q
qsub -j y -o $4/BEAST_LOG_$1.log -V -cwd -q $queue -N BEAST_$1 <<END
#!/bin/sh

#### SEND MESSAGE TO QSUB JOB HANLDER - JOB STARTING
 echo #1_Start

echo "$2"
$2

#### SEND MESSAGE TO QSUB JOB HANDLER IN PIPELINE MANAGER
id="$1"
host="$5"
port="$6"

success=1
while [ $# < 7 ]; do
    # If file does not exist, then write failure and break
    if [ ! -f $7 ]; then
        echo ${id}_$7_Fail | nc -w 0 $host $port
        success=0
        break
    fi
    shift
done
if [ success -eq 1 ]; then
    echo ${id}_Success | nc -w 0 $host $port
fi

END