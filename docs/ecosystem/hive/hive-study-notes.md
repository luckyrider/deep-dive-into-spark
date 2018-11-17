# Hive Study Notes

## 安装
使用apache hive 0.13.1

基本安装步骤包括：

* 安装requirements
* 安装和配置Metastore database and Metastore server
* 安装和配置Hiveserver2
* 使用客户端

### 安装requirements、二进制安装、从源码build安装等
References:

* https://cwiki.apache.org/confluence/display/Hive/AdminManual+Installation

build Hive using Maven (release 0.13 and later) or Ant (release 0.12 and earlier)

### Install metastore database and metastore server
References:

* https://cwiki.apache.org/confluence/display/Hive/AdminManual+MetastoreAdmin

### Install hiveserver2
references:

* https://cwiki.apache.org/confluence/display/Hive/Setting+Up+HiveServer2

### scripts

```
nohup hive --service metastore 2>&1 >$HIVE_HOME/metastore.out &
nohup hive --service hiveserver2 2>&1 >$HIVE_HOME/hiveserver2.out &
```

## Issues
### skew
HiveKey的hashCode使用31作为seed进行计算，例：join的on条件有两列col1,col2，那么hiveKey的hashCode是hashCode(col1)*31 + hashCode(col2)。恰好，这个job的reduce个数是31，这样，在决定当前记录所属reduce时，只有col2决定了。倾斜的作业中，col2的重复度很高，所以，导致最后的倾斜。

## Sourcecode

```
org.apache.hadoop.util.RunJar /home/vagrant/dataplatform/hive/lib/hive-cli-0.13.1.jar org.apache.hadoop.hive.cli.CliDriver
org.apache.hadoop.util.RunJar /home/vagrant/dataplatform/hive/lib/hive-service-0.13.1.jar org.apache.hadoop.hive.metastore.HiveMetaStore --hiveconf hive.log4j.file=/home/vagrant/dataplatform/hive/conf/hivemetastore-log4j.properties
org.apache.hadoop.util.RunJar /home/vagrant/dataplatform/hive/lib/hive-service-0.13.1.jar org.apache.hive.service.server.HiveServer2 --hiveconf hive.log4j.file=/home/vagrant/dataplatform/hive/conf/hiveserver2-log4j.properties
org.apache.hadoop.util.RunJar /home/vagrant/dataplatform/hive/lib/hive-cli-0.13.1.jar org.apache.hive.beeline.BeeLine
```