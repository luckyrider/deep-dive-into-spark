#!/usr/bin/env bash
# ......

# http://spark.apache.org/docs/latest/hadoop-provided.html
SPARK_DIST_CLASSPATH=$(hadoop classpath):~/Workspace/deploy/hadoop-conf:~/Workspace/deploy/hive-conf
# http://spark.apache.org/docs/latest/running-on-yarn.html. When running with master 'yarn' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.
HADOOP_CONF_DIR=~/Workspace/deploy/hadoop-conf
