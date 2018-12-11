#!/bin/sh
cluster_name=$1

$HADOOP_PREFIX/bin/hdfs namenode -format $cluster_name
