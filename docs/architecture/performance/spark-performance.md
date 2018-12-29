# Spark Performance

## Overview


## Performance Benchmark
HiBench features many benchmarks within it that exercise several components of Spark (great for stressing core, sql, MLlib capabilities), SparkSqlPerf features 99 TPC-DS queries (stressing the DataFrame API and therefore the Catalyst optimiser), both work well with Spark 2 

* HiBench: https://github.com/intel-hadoop/HiBench
* SparkSqlPerf: https://github.com/databricks/spark-sql-perf

micro benchmark:

* https://github.com/apache/spark/tree/master/sql/core/src/test/scala/org/apache/spark/sql/execution/benchmark

## Instrumentation, Monitoring and Profiling

* http://db-blog.web.cern.ch/blog/luca-canali/2017-03-measuring-apache-spark-workload-metrics-performance-troubleshooting
* https://db-blog.web.cern.ch/blog/luca-canali/2016-09-spark-20-performance-improvements-investigated-flame-graphs

## Performance Tuning and Improvements

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

### Too Many Small Files

* https://issues.apache.org/jira/browse/SPARK-13664
* https://issues.apache.org/jira/browse/SPARK-8813
* https://issues.apache.org/jira/browse/SPARK-8812

