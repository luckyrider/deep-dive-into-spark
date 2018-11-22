# Alluxio Study Notes

## Overview
* standalone cluster
* alluxio + hdfs
* alluxio + spark
* troubleshooting

## standalone cluster

install and config:

```
wget http://alluxio.org/downloads/files/1.3.0/alluxio-1.3.0-bin.tar.gz
tar xvfz alluxio-1.3.0-bin.tar.gz
cd alluxio
bin/alluxio bootstrapConf <alluxio_master_hostname>
bin/alluxio bootstrapConf localhost
```

format:

```
bin/alluxio format
```

start:

```
bin/alluxio-start.sh
bin/alluxio-start.sh master
bin/alluxio-start.sh worker
```

```
bin/alluxio runTests
```

webui: http://<alluxio_master_hostname>:19999

## alluxio + hdfs

org.apache.hadoop.fs.FileSystem:

```
  private static void loadFileSystems() {
    synchronized (FileSystem.class) {
      if (!FILE_SYSTEMS_LOADED) {
        ServiceLoader<FileSystem> serviceLoader = ServiceLoader.load(FileSystem.class);
        for (FileSystem fs : serviceLoader) {
          SERVICE_FILE_SYSTEMS.put(fs.getScheme(), fs.getClass());
        }
        FILE_SYSTEMS_LOADED = true;
      }
    }
  }
```

META-INF/services/org.apache.hadoop.fs.FileSystem:

```
alluxio.hadoop.FileSystem
alluxio.hadoop.FaultTolerantFileSystem
...
```

META-INF/services/alluxio.underfs.UnderFileSystemFactory:

```
alluxio.underfs.hdfs.HdfsUnderFileSystemFactory
alluxio.underfs.local.LocalUnderFileSystemFactory
...
```

## alluxio + spark

```
spark-shell --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 --conf spark.cassandra.connection.host=localhost --conf spark.executor.extraClassPath=$ZEPPELIN_HOME/interpreter/cassandra/guava-16.0.1.jar:$ALLUXIO_HOME/core/client/target/alluxio-core-client-1.3.0-jar-with-dependencies.jar --conf spark.driver.extraClassPath=$ZEPPELIN_HOME/interpreter/cassandra/guava-16.0.1.jar:$ALLUXIO_HOME/core/client/target/alluxio-core-client-1.3.0-jar-with-dependencies.jar 
```

```
val s = sc.textFile("alluxio://localhost:19998/LICENSE")
val double = s.map(line => line + line)
double.saveAsTextFile("alluxio://localhost:19998/LICENSE2")
```

```
16/11/02 19:09:58 INFO type: initialize(alluxio://localhost:19998/LICENSE2, Configuration: core-default.xml, core-site.xml, mapred-default.xml, mapred-site.xml, yarn-default.xml, yarn-site.xml, hdfs-default.xml, hdfs-site.xml). Connecting to Alluxio: alluxio://localhost:19998/LICENSE2
16/11/02 19:09:58 INFO type: alluxio://localhost:19998 alluxio://localhost:19998
16/11/02 19:09:58 INFO type: Loading Alluxio properties from Hadoop configuration: {}
16/11/02 19:09:58 INFO type: Starting sinks with config: {}.
16/11/02 19:09:58 INFO type: Sinks have already been started.
16/11/02 19:09:58 INFO type: getWorkingDirectory: /
16/11/02 19:09:58 INFO type: getWorkingDirectory: /
16/11/02 19:09:58 INFO type: getFileStatus(alluxio://localhost:19998/LICENSE2)
16/11/02 19:09:58 INFO type: Alluxio client (version 1.3.0) is trying to connect with FileSystemMasterClient master @ localhost/127.0.0.1:19998
16/11/02 19:09:58 INFO type: Client registered with FileSystemMasterClient master @ localhost/127.0.0.1:19998
16/11/02 19:09:58 INFO deprecation: mapred.tip.id is deprecated. Instead, use mapreduce.task.id
16/11/02 19:09:58 INFO deprecation: mapred.task.id is deprecated. Instead, use mapreduce.task.attempt.id
16/11/02 19:09:58 INFO deprecation: mapred.task.is.map is deprecated. Instead, use mapreduce.task.ismap
16/11/02 19:09:58 INFO deprecation: mapred.task.partition is deprecated. Instead, use mapreduce.task.partition
16/11/02 19:09:58 INFO deprecation: mapred.job.id is deprecated. Instead, use mapreduce.job.id
16/11/02 19:09:58 INFO FileOutputCommitter: File Output Committer Algorithm version is 1
16/11/02 19:09:58 INFO type: getWorkingDirectory: /
16/11/02 19:09:58 INFO type: mkdirs(alluxio://localhost:19998/LICENSE2/_temporary/0, rwxrwxrwx)
16/11/02 19:09:58 INFO type: getFileStatus(alluxio://localhost:19998/LICENSE)
16/11/02 19:09:58 INFO FileInputFormat: Total input paths to process : 1
16/11/02 19:09:58 INFO SparkContext: Starting job: saveAsTextFile at <console>:32
16/11/02 19:09:58 INFO DAGScheduler: Got job 0 (saveAsTextFile at <console>:32) with 2 output partitions
16/11/02 19:09:58 INFO DAGScheduler: Final stage: ResultStage 0 (saveAsTextFile at <console>:32)
16/11/02 19:09:58 INFO DAGScheduler: Parents of final stage: List()
16/11/02 19:09:58 INFO DAGScheduler: Missing parents: List()
16/11/02 19:09:58 INFO DAGScheduler: Submitting ResultStage 0 (MapPartitionsRDD[3] at saveAsTextFile at <console>:32), which has no missing parents
16/11/02 19:09:58 INFO MemoryStore: Block broadcast_1 stored as values in memory (estimated size 72.0 KB, free 163.9 KB)
16/11/02 19:09:58 INFO MemoryStore: Block broadcast_1_piece0 stored as bytes in memory (estimated size 25.2 KB, free 189.1 KB)
16/11/02 19:09:58 INFO BlockManagerInfo: Added broadcast_1_piece0 in memory on 10.101.51.115:55577 (size: 25.2 KB, free: 511.1 MB)
16/11/02 19:09:58 INFO SparkContext: Created broadcast 1 from broadcast at DAGScheduler.scala:1006
16/11/02 19:09:58 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 0 (MapPartitionsRDD[3] at saveAsTextFile at <console>:32)
16/11/02 19:09:58 INFO TaskSchedulerImpl: Adding task set 0.0 with 2 tasks
16/11/02 19:09:58 INFO TaskSetManager: Starting task 0.0 in stage 0.0 (TID 0, 10.101.51.115, partition 0,NODE_LOCAL, 3428 bytes)
16/11/02 19:09:58 INFO TaskSetManager: Starting task 1.0 in stage 0.0 (TID 1, 10.101.51.115, partition 1,NODE_LOCAL, 3428 bytes)
16/11/02 19:09:59 INFO BlockManagerInfo: Added broadcast_1_piece0 in memory on 10.101.51.115:55582 (size: 25.2 KB, free: 511.1 MB)
16/11/02 19:09:59 INFO BlockManagerInfo: Added broadcast_0_piece0 in memory on 10.101.51.115:55582 (size: 22.0 KB, free: 511.1 MB)
16/11/02 19:10:00 INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 2243 ms on 10.101.51.115 (1/2)
16/11/02 19:10:00 INFO TaskSetManager: Finished task 1.0 in stage 0.0 (TID 1) in 2231 ms on 10.101.51.115 (2/2)
16/11/02 19:10:00 INFO TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool
16/11/02 19:10:00 INFO DAGScheduler: ResultStage 0 (saveAsTextFile at <console>:32) finished in 2.253 s
16/11/02 19:10:00 INFO DAGScheduler: Job 0 finished: saveAsTextFile at <console>:32, took 2.336270 s
16/11/02 19:10:00 INFO type: listStatus(alluxio://localhost:19998/LICENSE2/_temporary/0)
16/11/02 19:10:01 INFO type: getFileStatus(alluxio://localhost:19998/LICENSE2)
16/11/02 19:10:01 INFO type: listStatus(alluxio://localhost:19998/LICENSE2/_temporary/0/task_201611021909_0000_m_000001)
16/11/02 19:10:01 INFO type: getFileStatus(alluxio://localhost:19998/LICENSE2/part-00001)
16/11/02 19:10:01 INFO type: rename(alluxio://localhost:19998/LICENSE2/_temporary/0/task_201611021909_0000_m_000001/part-00001, alluxio://localhost:19998/LICENSE2/part-00001)
16/11/02 19:10:01 INFO type: getFileStatus(alluxio://localhost:19998/LICENSE2)
16/11/02 19:10:01 INFO type: listStatus(alluxio://localhost:19998/LICENSE2/_temporary/0/task_201611021909_0000_m_000000)
16/11/02 19:10:01 INFO type: getFileStatus(alluxio://localhost:19998/LICENSE2/part-00000)
16/11/02 19:10:01 INFO type: rename(alluxio://localhost:19998/LICENSE2/_temporary/0/task_201611021909_0000_m_000000/part-00000, alluxio://localhost:19998/LICENSE2/part-00000)
16/11/02 19:10:01 INFO type: delete(alluxio://localhost:19998/LICENSE2/_temporary, true)
16/11/02 19:10:01 INFO type: create(alluxio://localhost:19998/LICENSE2/_SUCCESS, rw-r--r--, true, 65536, 1, 536870912, null)
```

## Troubleshooting

### java.lang.UnsatisfiedLinkError: no snappyjava in java.library.path

problem:

```
scala> val s = sc.textFile("alluxio://localhost:19998/LICENSE")
java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:497)
	at org.xerial.snappy.SnappyLoader.loadNativeLibrary(SnappyLoader.java:317)
	at org.xerial.snappy.SnappyLoader.load(SnappyLoader.java:219)
	at org.xerial.snappy.Snappy.<clinit>(Snappy.java:44)
    ...
Caused by: java.lang.UnsatisfiedLinkError: no snappyjava in java.library.path
	at java.lang.ClassLoader.loadLibrary(ClassLoader.java:1864)
	at java.lang.Runtime.loadLibrary0(Runtime.java:870)
	at java.lang.System.loadLibrary(System.java:1122)
	at org.xerial.snappy.SnappyNativeLoader.loadLibrary(SnappyNativeLoader.java:52)
	... 80 more
```

solution:

manually add libsnappyjava.jnilib (it's in the jar) to /Library/Java/Extensions/ (this is one of java.library.path)

see more:

* http://stackoverflow.com/questions/30039976/unsatisfiedlinkerror-no-snappyjava-in-java-library-path-when-running-spark-mlli
* https://www.chilkatsoft.com/java-loadLibrary-MacOSX.asp
