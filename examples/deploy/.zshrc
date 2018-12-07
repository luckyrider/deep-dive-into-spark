# ......

ZSH_THEME="agnoster"

# ......

source /etc/profile
source ~/.bash_profile
source $ZSH/oh-my-zsh.sh

# ......

# Shadowsocks
alias setproxy="export socks5_proxy=socks5://127.0.0.1:1086;export http_proxy=http://127.0.0.1:1087;export https_proxy=http://127.0.0.1:1087;"
alias unsetproxy="unset socks5_proxy;unset http_proxy;unset https_proxy"
alias ip="curl -i https://ip.cn"

# Java
export JAVA_HOME=$(/usr/libexec/java_home)
export CLASSPATH=".:$CLASSPATH"

# Deploy Base
export DEPLOY_BASE=~/Workspace/deploy

# Spark Ecosystem
export PATH="/usr/local/opt/protobuf@2.5/bin:$PATH"
export PATH="/usr/local/opt/thrift@0.9/bin:$PATH"
export PATH="/usr/local/opt/sbt@0.13/bin:$PATH"
export CLASSPATH="/usr/local/Cellar/antlr/4.7.1/antlr-4.7.1-complete.jar:$CLASSPATH"
export SCALA_HOME=~/Workspace/deploy/scala
export HADOOP_HOME=$DEPLOY_BASE/hadoop
export HADOOP_CONF_DIR=$DEPLOY_BASE/hadoop-conf
export HIVE_HOME=$DEPLOY_BASE/hive
export HIVE_CONF_DIR=$DEPLOY_BASE/hive-conf
export PATH=$PATH:$SCALA_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$HIVE_HOME/bin:$DEPLOY_BASE/hive-utils
export LIVY_HOME=$DEPLOY_BASE/livy-0.5.0-incubating-bin
export LIVY_CONF_DIR=/$DEPLOY_BASE/livy-conf
export PATH=$LIVY_HOME/bin:$PATH
alias parquet-tools="java -jar ~/Workspace/projects/spark-friends/parquet-mr/parquet-tools/target/parquet-tools-1.10.1-SNAPSHOT.jar"
alias start-yarn="yarn-daemon.sh start resourcemanager && yarn-daemon.sh start nodemanager"
alias hive-1.2.1="export HIVE_HOME=$DEPLOY_BASE/apache-hive-1.2.1-bin"
alias hive-1.2.2="export HIVE_HOME=$DEPLOY_BASE/apache-hive-1.2.2-bin"
alias hive-2.3.3="export HIVE_HOME=$DEPLOY_BASE/apache-hive-2.3.3-bin"

# Spark
export SPARK_HOME=$DEPLOY_BASE/spark
export SPARK_CONF_DIR=$DEPLOY_BASE/spark-conf
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
alias spark-2.1.0="export SPARK_HOME=$DEPLOY_BASE/spark-2.1.0-bin-hadoop2.7"
alias spark-2.2.0="export SPARK_HOME=$DEPLOY_BASE/spark-2.2.0-bin-hadoop2.7"
alias spark-2.3.1="export SPARK_HOME=$DEPLOY_BASE/spark-2.3.1-bin-hadoop2.7"
alias spark-2.4.0="export SPARK_HOME=$DEPLOY_BASE/spark-2.4.0-bin-hadoop2.7"
alias spark-3.0.0="export SPARK_HOME=$DEPLOY_BASE/spark-3.0.0-bin-hadoop2.7"
