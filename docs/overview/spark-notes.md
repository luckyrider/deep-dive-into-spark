# Spark Notes


## Overview

* Spark 1.x and 2.x
* configuration
* Core
* application server
* Performance tuning
* Toubleshooting
* reference

## Spark 1.x and 2.x

### spark 2.0
small files:

* https://issues.apache.org/jira/browse/SPARK-13664
* https://issues.apache.org/jira/browse/SPARK-8813
* https://issues.apache.org/jira/browse/SPARK-8812

## shell scripts

spark-shell:

```
org.apache.spark.deploy.SparkSubmit --master local --class org.apache.spark.repl.Main --name "Spark shell spark-shell"
```


## Configuration

### classpath
SPARK_CLASSPATH was deprecated. see more at org.apache.spark.SparkConf.

```
sys.env.get("SPARK_CLASSPATH").foreach { value =>
  val warning =
    s"""
      |SPARK_CLASSPATH was detected (set to '$value').
      |This is deprecated in Spark 1.0+.
      |
      |Please instead use:
      | - ./spark-submit with --driver-class-path to augment the driver classpath
      | - spark.executor.extraClassPath to augment the executor classpath
    """.stripMargin
  logWarning(warning)
```

```
org.apache.spark.launcher
  AbstractCommandBuilder
    SparkClassCommandBuilder
    SparkSubmitCommandBuilder
```

AbstractCommandBuilder#buildClassPath:

```
getenv("SPARK_CLASSPATH") <- 
appClassPath              <- 
getConfDir()              <- 
getenv("SPARK_PREPEND_CLASSES")
addToClassPath(cp, getenv("HADOOP_CONF_DIR"));
addToClassPath(cp, getenv("YARN_CONF_DIR"));
addToClassPath(cp, getenv("SPARK_DIST_CLASSPATH"));
```

SPARK_DIST_CLASSPATH的使用，见Using Spark's "Hadoop Free" Build. https://spark.apache.org/docs/latest/hadoop-provided.html

## Core

### Skipped stages
* http://stackoverflow.com/questions/34580662/what-does-stage-skipped-mean-in-apache-spark-web-ui
* https://github.com/apache/spark/pull/3009
* http://blog.csdn.net/u012684933/article/details/50378725

## Performance Tuning


## Troubleshooting

### OOM

```
[Stage 21:==>                                                   (9 + 120) / 200]16/09/23 10:53:46 WARN TaskSetManager: Lost task 33.0 in stage 21.0 (TID 5172, xxx): java.lang.OutOfMemoryError: Java heap space

[Stage 21:==>                                                  (10 + 120) / 200]16/09/23 10:53:52 WARN TaskSetManager: Lost task 46.0 in stage 21.0 (TID 5185, xxx): java.lang.OutOfMemoryError: error while calling spill() on org.apache.spark.util.collection.unsafe.sort.UnsafeExternalSorter@5d54d2e9 : /tmp/spark-394ef1fc-88a8-470a-bf2e-8e6b67d81e6d/executor-a516b4e7-3eb6-45ab-9be5-8f4e5837c071/blockmgr-59afdc25-ffc8-47e1-b5b4-ddfd2df65593/35/temp_local_3f707ca2-f252-4f4b-b00c-24d40ac848fa (No such file or directory)
        at org.apache.spark.memory.TaskMemoryManager.acquireExecutionMemory(TaskMemoryManager.java:165)
        at org.apache.spark.memory.TaskMemoryManager.allocatePage(TaskMemoryManager.java:249)
        ...
[Stage 21:===>                                                 (12 + 120) / 200]16/09/23 10:53:56 WARN TaskSetManager: Lost task 46.1 in stage 21.0 (TID 5275, xxx): FetchFailed(BlockManagerId(0, xxx, 14038), shuffleId=12, mapId=1, reduceId=46, message=
org.apache.spark.shuffle.FetchFailedException: java.io.FileNotFoundException: /tmp/spark-394ef1fc-88a8-470a-bf2e-8e6b67d81e6d/executor-a516b4e7-3eb6-45ab-9be5-8f4e5837c071/blockmgr-59afdc25-ffc8-47e1-b5b4-ddfd2df65593/35/shuffle_12_31_0.index (No such file or directory)
        at java.io.FileInputStream.open0(Native Method)
        at java.io.FileInputStream.open(FileInputStream.java:195)
        at java.io.FileInputStream.<init>(FileInputStream.java:138)
        at org.apache.spark.shuffle.IndexShuffleBlockResolver.getBlockData(IndexShuffleBlockResolver.scala:191)
        at org.apache.spark.storage.BlockManager.getBlockData(BlockManager.scala:298)
```

### Driver OOM

```
scala> t1.write.format("org.apache.spark.sql.cassandra").options(Map("table" -> "t1", "keyspace" -> "ks1")).save();
Exception in thread "qtp1831711067-742" java.lang.OutOfMemoryError: GC overhead limit exceeded
        at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.addConditionWaiter(AbstractQueuedSynchronizer.java:1855)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.awaitNanos(AbstractQueuedSynchronizer.java:2068)
        at org.spark-project.jetty.util.BlockingArrayQueue.poll(BlockingArrayQueue.java:342)
        at org.spark-project.jetty.util.thread.QueuedThreadPool.idleJobPoll(QueuedThreadPool.java:526)
        at org.spark-project.jetty.util.thread.QueuedThreadPool.access$600(QueuedThreadPool.java:44)
        at org.spark-project.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:572)
        at java.lang.Thread.run(Thread.java:745)
Exception in thread "broadcast-hash-join-6" java.lang.OutOfMemoryError: GC overhead limit exceeded
        at org.apache.spark.sql.execution.joins.UnsafeHashedRelation$.apply(HashedRelation.scala:402)
        at org.apache.spark.sql.execution.joins.HashedRelation$.apply(HashedRelation.scala:128)
        at org.apache.spark.sql.execution.joins.BroadcastHashOuterJoin$$anonfun$broadcastFuture$1$$anonfun$apply$1.apply(BroadcastHashOuterJoin.scala:92)
        at org.apache.spark.sql.execution.joins.BroadcastHashOuterJoin$$anonfun$broadcastFuture$1$$anonfun$apply$1.apply(BroadcastHashOuterJoin.scala:82)
        at org.apache.spark.sql.execution.SQLExecution$.withExecutionId(SQLExecution.scala:100)
        at org.apache.spark.sql.execution.joins.BroadcastHashOuterJoin$$anonfun$broadcastFuture$1.apply(BroadcastHashOuterJoin.scala:82)
        at org.apache.spark.sql.execution.joins.BroadcastHashOuterJoin$$anonfun$broadcastFuture$1.apply(BroadcastHashOuterJoin.scala:82)
        at scala.concurrent.impl.Future$PromiseCompletingRunnable.liftedTree1$1(Future.scala:24)
        at scala.concurrent.impl.Future$PromiseCompletingRunnable.run(Future.scala:24)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
        at java.lang.Thread.run(Thread.java:745)
16/09/22 15:21:52 ERROR ActorSystemImpl: exception on LARS’ timer thread
java.lang.OutOfMemoryError: GC overhead limit exceeded
        at akka.dispatch.AbstractNodeQueue.<init>(AbstractNodeQueue.java:22)
        at akka.actor.LightArrayRevolverScheduler$TaskQueue.<init>(Scheduler.scala:443)
        at akka.actor.LightArrayRevolverScheduler$$anon$8.nextTick(Scheduler.scala:409)
        at akka.actor.LightArrayRevolverScheduler$$anon$8.run(Scheduler.scala:375)
        at java.lang.Thread.run(Thread.java:745)
16/09/22 15:21:52 ERROR ActorSystemImpl: Uncaught fatal error from thread [sparkDriverActorSystem-scheduler-1] shutting down ActorSystem [sparkDriverActorSystem]
java.lang.OutOfMemoryError: GC overhead limit exceeded
        at akka.dispatch.AbstractNodeQueue.<init>(AbstractNodeQueue.java:22)
        at akka.actor.LightArrayRevolverScheduler$TaskQueue.<init>(Scheduler.scala:443)
        at akka.actor.LightArrayRevolverScheduler$$anon$8.nextTick(Scheduler.scala:409)
        at akka.actor.LightArrayRevolverScheduler$$anon$8.run(Scheduler.scala:375)
        at java.lang.Thread.run(Thread.java:745)
```

solution: increase driver heap memory

## References

Cluster Manager:

* http://stackoverflow.com/questions/28664834/which-cluster-type-should-i-choose-for-spark
* http://www.slideshare.net/SparkSummit/wampler-chen

Spark SQL:

* Deep Dive into Spark SQL’s Catalyst Optimizer. https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html
* http://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf

Performance:

* https://databricks.com/blog/2015/04/24/recent-performance-improvements-in-apache-spark-sql-python-dataframes-and-more.html
* https://databricks.com/blog/2015/04/28/project-tungsten-bringing-spark-closer-to-bare-metal.html

Job Server:

* https://github.com/spark-jobserver/spark-jobserver
* Using Apache Spark to serve real time web services queries. http://stackoverflow.com/questions/30653571/using-apache-spark-to-serve-real-time-web-services-queries
* http://www.slideshare.net/SparkSummit/productionizing-spark-and-the-rest-job-server-evan-chan

