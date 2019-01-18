# dataplatform singlenode

## MySQL
```
sudo service mysql start
```

Enable access from host OS:

```
CREATE USER 'root'@'10.0.2.2' IDENTIFIED BY '123456';
GRANT ALL ON *.* TO 'root'@'10.0.2.2';
DROP USER 'root'@'10.0.2.2'
```

## Zookeeper
```
zkServer.sh start
zkCli.sh -server 127.0.0.1:2181
```

## Hadoop

HDFS format:

```
hdfs namenode -format
```

Start/stop HDFS:

```
hadoop-daemon.sh start namenode
hadoop-daemon.sh start datanode

hadoop-daemon.sh stop datanode
hadoop-daemon.sh stop namenode
```

Start/stop YARN:

```
yarn-daemon.sh start resourcemanager
yarn-daemon.sh start nodemanager

yarn-daemon.sh stop nodemanager
yarn-daemon.sh stop resourcemanager
```

MapReduce on YARN:

```
hadoop jar /opt/dataplatform/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.5.0-cdh5.3.2.jar pi 1 10
```

## Hive

start MetaStore and HiveServer2

```
hive-start-hiveserver2.sh
hive-start-metastore.sh
```

```
nohup hive --service metastore --hiveconf hive.log4j.file=$HIVE_HOME/conf/hivemetastore-log4j.properties >$HIVE_HOME/metastore.out 2>&1 &
nohup hive --service hiveserver2 --hiveconf hive.log4j.file=$HIVE_HOME/conf/hiveserver2-log4j.properties >$HIVE_HOME/hiveserver2.out 2>&1 &
```

Hive CLI

```
cd $HIVE_HOME
hive
CREATE TABLE pokes (foo INT, bar STRING);
CREATE TABLE invites (foo INT, bar STRING) PARTITIONED BY (ds STRING);
LOAD DATA LOCAL INPATH './examples/files/kv1.txt' OVERWRITE INTO TABLE pokes;
LOAD DATA LOCAL INPATH './examples/files/kv2.txt' OVERWRITE INTO TABLE invites PARTITION (ds='2008-08-15');
LOAD DATA LOCAL INPATH './examples/files/kv3.txt' OVERWRITE INTO TABLE invites PARTITION (ds='2008-08-08');
```

Beeline:

```
beeline
!connect jdbc:hive2://localhost:10000 admin admin
show databases;
show tables;
!quit
```

## Presto
start server:

```
launcher start
```

CLI:

```
presto --server localhost:8081

show catalogs;

show schemas from hive;
show tables from hive.default;
describe hive.default.pokes;
select count(1) from hive.default.pokes;

show schemas from cassandra;
```

## Cassandra

start cassandra:

```
cassandra
```

cqlsh:

```
source ~/.virtualenv/python-2.7.10/bin/activate
cqlsh
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
use test;
CREATE TABLE user ( id int, first_name text, last_name text, PRIMARY KEY (id));
INSERT INTO user(id, first_name, last_name) VALUES(1, 'aaa', 'bbb');
```

## Kafka

```
cd $KAFKA_HOME
bin/kafka-server-start.sh -daemon config/server.properties
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
bin/kafka-topics.sh --list --zookeeper localhost:2181
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
```

## Elasticsearch

```
elasticsearch -d
curl 'http://localhost:9200/?pretty'

curl -XPUT 'http://localhost:9200/megacorp/employee/1' -d '
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}'

curl -XPUT 'http://localhost:9200/megacorp/employee/2' -d '
{
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}'

curl -XPUT 'http://localhost:9200/megacorp/employee/3' -d '
{
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}'

curl 'http://localhost:9200/megacorp/employee/1'
curl 'http://localhost:9200/megacorp/employee/2'
curl 'http://localhost:9200/megacorp/employee/3'

curl 'http://localhost:9200/megacorp/employee/_search'
```

## Spark
```
SPARK_MASTER_IP=localhost start-master.sh
start-slave.sh spark://localhost:7077
```

### Spark Hive Integration


### Spark Cassandra Integration

```
spark-shell --master spark://localhost:7077 --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 --conf spark.cassandra.connection.host=localhost

import com.datastax.spark.connector._
import com.datastax.spark.connector.cql._

sqlContext.sql("""
CREATE TEMPORARY TABLE user
USING org.apache.spark.sql.cassandra
OPTIONS (
  table "user",
  keyspace "test",
  cluster "Test Cluster",
  pushdown "true")
""".stripMargin)

val dfUser = sqlContext.sql("SELECT * FROM user")

dfUser.show
```

