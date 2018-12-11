#!/bin/bash
this_dir=`dirname $0`
source ${this_dir}/set_spark_property.sh
source ${this_dir}/set_hadoop_property.sh

function enableLocalFsEventLog(){
	local default_spark_history_fs_logDirectory=/tmp/spark-events
	local ld=$default_spark_history_fs_logDirectory
	echo "WILL ENABLE LOCAL FS EVENTLOG @ $ls"

	if [ ! -d "$ld" ]; then
	    mkdir -p $ld
	    chown spark:hadoop $ld
	    chmod 0775 $ld
	fi

	set_spark_property "spark.eventLog.enabled=true"
}

function enableRemoteFsEventLog(){
	local spark_eventlog_dir=/spark_eventlog
	fs=$1
	local path=$fs$spark_eventlog_dir
	echo "WILL ENABLE REMOTE FS EVENTLOG @ $path"

	su - spark -l -c "${this_dir}/create-remote-dir.sh $spark_eventlog_dir"

	set_spark_property "spark.eventLog.enabled=true"
	set_spark_property "spark.eventLog.dir=$path"
	set_spark_property "spark.history.fs.logDirectory=$path"
}

function enableEventLog(){
	local fs=`${this_dir}/conf_editor.py $HADOOP_CONF_DIR print core:fs.defaultFS`
	if [ -n "$fs" ] ; then
		enableRemoteFsEventLog $fs
	else
		enableLocalFsEventLog
	fi
}

# on_options=(on yes true enable)
# eventlog_switch=`echo "$SPARK_EVENTLOG_ENABLE" | awk '{print tolower($0)}'`
# for key in ${on_options[*]}
# do
# 	if [[ ${key}"" == ${eventlog_switch}"" ]] ; then
# 		enableEventLog
# 		break
# 	fi
# done

