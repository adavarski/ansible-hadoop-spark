#!/bin/bash

spark_eventlog_dir=$1
username=`id -u -n`

echo "Check HDFS status ..."
until $HADOOP_HOME/bin/hdfs dfsadmin -report 2>/dev/null ; do
	echo "HDFS not running, waiting ..."
	sleep 5
done

$HADOOP_PREFIX/bin/hdfs dfs -mkdir $spark_eventlog_dir
$HADOOP_PREFIX/bin/hdfs dfs -chown ${username}:hadoop $spark_eventlog_dir
$HADOOP_PREFIX/bin/hdfs dfs -chmod 0775 $spark_eventlog_dir
