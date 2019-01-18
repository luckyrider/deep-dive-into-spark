# Spark Dev Environment

## System Variables
`~/.zshrc`

```
# System preferences
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1086"
alias unsetproxy="unset ALL_PROXY"
alias ip="curl -i http://ip.cn"

# Java
export JAVA_HOME=$(/usr/libexec/java_home)
export CLASSPATH=".:$CLASSPATH"

# Deploy base
export DEPLOY_BASE=~/Workspace/deploy

# 3rd party frameworks/tools
export PATH="/usr/local/opt/mysql@5.7/bin:$PATH"
# export PATH="/usr/local/opt/protobuf@2.5/bin:$PATH"
export PATH="/usr/local/opt/thrift@0.9/bin:$PATH"
export HADOOP_HOME=$DEPLOY_BASE/hadoop
export HADOOP_CONF_DIR=$DEPLOY_BASE/hadoop-conf
export HIVE_HOME=$DEPLOY_BASE/hive
export HIVE_CONF_DIR=$DEPLOY_BASE/hive-conf
export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$HIVE_HOME/bin:$PATH
alias parquet-tools="java -jar ~/Workspace/projects/parquet-mr/parquet-tools/target/parquet-tools-1.10.1-SNAPSHOT.jar"
export CLASSPATH="/usr/local/Cellar/antlr/4.7.1/antlr-4.7.1-complete.jar:$CLASSPATH"

# Spark
export SPARK_HOME=$DEPLOY_BASE/spark
export SPARK_CONF_DIR=$DEPLOY_BASE/spark-conf
PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
```

## Hadoop
`hadoop-env.sh`:

```
export JAVA_HOME=$(/usr/libexec/java_home)
```

`core-site.xml`:

```
<configuration>
<property>
  <name>fs.defaultFS</name>
  <value>file:///</value>
</property>
<property>
  <name>hadoop.tmp.dir</name>
  <value>${user.home}/Workspace/deploy/hadoop-tmp</value>
</property>
</configuration>
```

`hdfs-site.xml`:

```
<configuration>
<property>
  <name>dfs.replication</name>
  <value>1</value>
</property>
</configuration>
```

`yarn-site.xml`:

```
<configuration>

<!-- Site specific YARN configuration properties -->
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle,spark_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.spark_shuffle.class</name>
  <value>org.apache.spark.network.yarn.YarnShuffleService</value>
</property>
</configuration>
```

mapred-site.xml

```
<configuration>
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
</property>
</configuration>
```

## Hive
`hive-site.xml`:

```
<configuration>
  <property>  
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://localhost:3306/metastore?createDatabaseIfNotExist=true</value>  
  </property>  
   
  <property>  
    <name>javax.jdo.option.ConnectionDriverName</name>  
    <value>com.mysql.jdbc.Driver</value>  
  </property>  
   
  <property>  
    <name>javax.jdo.option.ConnectionUserName</name>  
    <value>root</value>
  </property>  
   
  <property>  
    <name>javax.jdo.option.ConnectionPassword</name>  
    <value>123456</value>
  </property>

  <property>
    <name>hive.metastore.uris</name>
    <value>thrift://localhost:9083</value>
  </property>

  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
  </property>
</configuration>
```

`hive-start-metastore.sh`:

```
nohup hive --service metastore --hiveconf hive.log4j.file=$HIVE_CONF_DIR/hive-metastore-log4j.properties >$HIVE_HOME/metastore.out 2>&1 &
```

`hive-start-hiveserver2.sh`

```
nohup hive --service hiveserver2 --hiveconf hive.log4j.file=$HIVE_CONF_DIR/hive-hiveserver2-log4j.properties >$HIVE_HOME/hiveserver2.out 2>&1 &
```

## Spark
`spark-env.sh`

```
# http://spark.apache.org/docs/latest/hadoop-provided.html
SPARK_DIST_CLASSPATH=$(hadoop classpath):~/Workspace/deploy/hadoop-conf:~/Workspace/deploy/hive-conf
# http://spark.apache.org/docs/latest/running-on-yarn.html. When running with master 'yarn' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.
HADOOP_CONF_DIR=~/Workspace/deploy/hadoop-conf
```

spark-defaults.conf

```
spark.serializer                 org.apache.spark.serializer.KryoSerializer
spark.eventLog.enabled           true
spark.eventLog.dir               file:///Users/seanmao/Workspace/deploy/spark-eventlog
spark.history.fs.logDirectory    file:///Users/seanmao/Workspace/deploy/spark-eventlog
spark.yarn.historyServer.address localhost:18080
```