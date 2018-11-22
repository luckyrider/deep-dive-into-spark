# Zeppelin Study Notes

## Overview

## Troubleshooting

### guava version problem
(1) try spark interpret alone, follow tutorial...succeed.

```
val bankText = sc.textFile("file:/Users/seanmao/dataplatform/data/bank/bank-full.csv")

case class Bank(age:Integer, job:String, marital : String, education : String, balance : Integer)

// split each line, filter out header (starts with "age"), and map it into Bank case class
val bank = bankText.map(s=>s.split(";")).filter(s=>s(0)!="\"age\"").map(
    s=>Bank(s(0).toInt, 
            s(1).replaceAll("\"", ""),
            s(2).replaceAll("\"", ""),
            s(3).replaceAll("\"", ""),
            s(5).replaceAll("\"", "").toInt
        )
)

// convert to DataFrame and create temporal table
bank.toDF().registerTempTable("bank")
```

(2) try spark cassandra connector, and...we encounter guava version issue.

```
import com.datastax.spark.connector._
import com.datastax.spark.connector.cql._

sqlc.sql("""
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

notebook messages:

```
java.lang.IllegalStateException: Detected Guava issue #1635 which indicates that a version of Guava less than 16.01 is in use.  This introduces codec resolution issues and potentially other incompatibility issues in the driver.  Please upgrade to Guava 16.01 or later.
	at com.datastax.driver.core.SanityChecks.checkGuava(SanityChecks.java:62)
	at com.datastax.driver.core.SanityChecks.check(SanityChecks.java:36)
	at com.datastax.driver.core.Cluster.<clinit>(Cluster.java:67)
```


google and find...: https://issues.apache.org/jira/browse/ZEPPELIN-1205


(3) add dependency via interpreter configuration page, but...NoSuchMethodError

reference: http://markmail.org/message/27vufhtzlvzfp4rp

/Users/seanmao/dataplatform/zeppelin-0.6.2-bin-all/interpreter/cassandra/guava-16.0.1.jar

```
java.lang.NoSuchMethodError: com.google.common.util.concurrent.Futures.withFallback(Lcom/google/common/util/concurrent/ListenableFuture;Lcom/google/common/util/concurrent/FutureFallback;Ljava/util/concurrent/Executor;)Lcom/google/common/util/concurrent/ListenableFuture;
	at com.datastax.driver.core.Connection.initAsync(Connection.java:177)
	at com.datastax.driver.core.Connection$Factory.open(Connection.java:731)
	at com.datastax.driver.core.ControlConnection.tryConnect(ControlConnection.java:251)
	at com.datastax.driver.core.ControlConnection.reconnectInternal(ControlConnection.java:199)
	at com.datastax.driver.core.ControlConnection.connect(ControlConnection.java:77)
	at com.datastax.driver.core.Cluster$Manager.init(Cluster.java:1414)
	at com.datastax.driver.core.Cluster.getMetadata(Cluster.java:393)
	at com.datastax.spark.connector.cql.CassandraConnector$.com$datastax$spark$connector$cql$CassandraConnector$$createSession(CassandraConnector.scala:155)
	at com.datastax.spark.connector.cql.CassandraConnector$$anonfun$3.apply(CassandraConnector.scala:148)
	at com.datastax.spark.connector.cql.CassandraConnector$$anonfun$3.apply(CassandraConnector.scala:148)
	at com.datastax.spark.connector.cql.RefCountedCache.createNewValueAndKeys(RefCountedCache.scala:31)
	at com.datastax.spark.connector.cql.RefCountedCache.acquire(RefCountedCache.scala:56)
	at com.datastax.spark.connector.cql.CassandraConnector.openSession(CassandraConnector.scala:81)
	at com.datastax.spark.connector.rdd.CassandraTableScanRDD.compute(CassandraTableScanRDD.scala:325)
```

(4) guava dependency version summary, what a mess!

```
cassandra java driver: 16.0.1
spark-cassandra-connector: guava 16.0.1
spark: guava 14 (until 2.1.0-SNAPSHOT still using 14.0.1)

zeppelin(0.6.2): 15.0(POM)
zeppelin(0.6.2)-cassandra: using guava 16.0.1
zeppelin(0.6.2)-spark: 14.0.1(POM)
zeppelin(0.6.2)-spark-dep:  16.0.1 for profile cassandra-spark-1.5, not defined for other profiles

zeppelin 0.6.2最终打包
zeppelin/lib/guava-15.0.jar
zeppelin/interpreter/spark/dep/zeppelin-spark-dependencies_2.11-0.6.2.jar <- guava 14.0.1

```

storm/cassandra集成有同样的问题: http://blog.csdn.net/bluishglc/article/details/50443205

错误纪录在spark interpreter的日志中zeppelin-interpreter-spark-<username>-<hostname>.log:

```
org.apache.spark.deploy.SparkSubmit --conf spark.cassandra.connection.host=localhost --conf spark.driver.extraClassPath=::/Users/seanmao/dataplatform/zeppelin/local-repo/2BYM1VV7D/*:/Users/seanmao/dataplatform/zeppelin/interpreter/spark/*::/Users/seanmao/dataplatform/zeppelin/lib/zeppelin-interpreter-0.6.2.jar:/Users/seanmao/dataplatform/zeppelin/interpreter/spark/zeppelin-spark_2.11-0.6.2.jar --conf spark.driver.extraJavaOptions= -Dfile.encoding=UTF-8 -Dlog4j.configuration=file:///Users/seanmao/dataplatform/zeppelin/conf/log4j.properties -Dzeppelin.log.file=/Users/seanmao/dataplatform/zeppelin/logs/zeppelin-interpreter-spark-seanmao-seanmaombp.local.log --class org.apache.zeppelin.interpreter.remote.RemoteInterpreterServer --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 /Users/seanmao/dataplatform/zeppelin/interpreter/spark/zeppelin-spark_2.11-0.6.2.jar 57030
```

(5) change driver/executor classpath

reference: http://ben-tech.blogspot.com/2016/04/how-to-resolve-spark-cassandra.html

将guava 16.0.1添加到driver classpath的头部。

```
org.apache.spark.deploy.SparkSubmit --conf spark.cassandra.connection.host=localhost --conf spark.driver.extraClassPath=/Users/seanmao/dataplatform/zeppelin-0.6.2-bin-all/interpreter/cassandra/guava-16.0.1.jar --conf spark.driver.extraJavaOptions= -Dfile.encoding=UTF-8 -Dlog4j.configuration=file:///Users/seanmao/dataplatform/zeppelin/conf/log4j.properties -Dzeppelin.log.file=/Users/seanmao/dataplatform/zeppelin/logs/zeppelin-interpreter-spark-seanmao-seanmaombp.local.log --class org.apache.zeppelin.interpreter.remote.RemoteInterpreterServer --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 /Users/seanmao/dataplatform/zeppelin/interpreter/spark/zeppelin-spark_2.11-0.6.2.jar 57688
```

notebook messages. 继续查看driver messages.

```
org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 4 times, most recent failure: Lost task 0.3 in stage 0.0 (TID 3, 10.101.51.115): ExecutorLostFailure (executor 1 exited caused by one of the running tasks) Reason: Remote RPC client disassociated. Likely due to containers exceeding thresholds, or network issues. Check driver logs for WARN messages.
Driver stacktrace:
	at org.apache.spark.scheduler.DAGScheduler.org$apache$spark$scheduler$DAGScheduler$$failJobAndIndependentStages(DAGScheduler.scala:1431)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$abortStage$1.apply(DAGScheduler.scala:1419)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$abortStage$1.apply(DAGScheduler.scala:1418)
	at scala.collection.mutable.ResizableArray$class.foreach(ResizableArray.scala:59)
	at scala.collection.mutable.ArrayBuffer.foreach(ArrayBuffer.scala:47)
	at org.apache.spark.scheduler.DAGScheduler.abortStage(DAGScheduler.scala:1418)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$handleTaskSetFailed$1.apply(DAGScheduler.scala:799)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$handleTaskSetFailed$1.apply(DAGScheduler.scala:799)
	at scala.Option.foreach(Option.scala:236)
	at org.apache.spark.scheduler.DAGScheduler.handleTaskSetFailed(DAGScheduler.scala:799)
	at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.doOnReceive(DAGScheduler.scala:1640)
	at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:1599)
	at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:1588)
	at org.apache.spark.util.EventLoop$$anon$1.run(EventLoop.scala:48)
	at org.apache.spark.scheduler.DAGScheduler.runJob(DAGScheduler.scala:620)
	at org.apache.spark.SparkContext.runJob(SparkContext.scala:1832)
```

driver(spark-submit) messages. executor使用了老的guava。

```
Caused by: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 1.0 failed 4 times, most recent failure: Lost task 0.3 in stage 1.0 (TID 7, 10.101.51.115): java.io.IOException: Failed to open native connection to Cassandra at {127.0.0.1}:9042
...
Caused by: java.lang.NoSuchMethodError: com.google.common.util.concurrent.Futures.withFallback(Lcom/google/common/util/concurrent/ListenableFuture;Lcom/google/common/util/concurrent/FutureFallback;Ljava/util/concurrent/Executor;)Lcom/google/common/util/concurrent/ListenableFuture;
```

将guava 16.0.1添加到executor classpath的头部。and..., mission accomplished!

```
org.apache.spark.deploy.SparkSubmit --conf spark.cassandra.connection.host=localhost --conf spark.executor.extraClassPath=/Users/seanmao/dataplatform/zeppelin-0.6.2-bin-all/interpreter/cassandra/guava-16.0.1.jar --conf spark.driver.extraClassPath=/Users/seanmao/dataplatform/zeppelin-0.6.2-bin-all/interpreter/cassandra/guava-16.0.1.jar --conf spark.driver.extraJavaOptions= -Dfile.encoding=UTF-8 -Dlog4j.configuration=file:///Users/seanmao/dataplatform/zeppelin/conf/log4j.properties -Dzeppelin.log.file=/Users/seanmao/dataplatform/zeppelin/logs/zeppelin-interpreter-spark-seanmao-seanmaombp.local.log --class org.apache.zeppelin.interpreter.remote.RemoteInterpreterServer --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 /Users/seanmao/dataplatform/zeppelin/interpreter/spark/zeppelin-spark_2.11-0.6.2.jar 57875
3305 org.apache.spark.deploy.master.Master --ip localhost --port 7077 --webui-port 8080
```


## References

总结介绍、架构:

* http://www.slideshare.net/doanduyhai/apache-zeppelin-the-missing-component-for-the-big-data-ecosystem
* Zeppelin wiki: https://cwiki.apache.org/confluence/display/ZEPPELIN/Zeppelin+Home

Zeppelin/Spark/Cassandra integration:

* Zeppelin/Spark/Cassandra integration tutorial. http://www.doanduyhai.com/blog/?p=2325
