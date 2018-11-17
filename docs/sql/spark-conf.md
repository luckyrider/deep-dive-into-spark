# spark配置总结

## 1. Overview

### 1.1 三类配置

(1) Spark properties（Spark属性）
* 起什么作用：控制application的参数
* 如何设置：使用SparkConf，或者Java system properties（Java系统属性），每个application单独设置。

(2) Environment variables（环境变量）
* 起什么作用：用来控制每台机器的设置
* 怎么设置：通过conf/spark-env.sh

(3) Logging（日志配置）
* 怎么设置：log4j.properties

### 1.2 动态加载配置
Spark shell和spark-submit工具，支持两种动态加载配置的方式。
* (1) 命令行选项
* (2) conf/spark-defaults.conf

配置的优先级从高到低：直接在SparkConf中设置，其次是命令行选项，最后是spark-defaults.conf。

### 1.3 查看Spark属性
Application Web UI (http://<driver>:4040) -> "Environment" Tab

### 1.4 常用配置

(1) Application Properties

```
spark.app.name
spark.master
spark.submit.deployMode

spark.driver.cores
spark.driver.memory
spark.executor.memory

spark.local.dir
```

(2) Runtime Environment

```
spark.driver.extraClassPath
spark.driver.extraJavaOptions
spark.driver.extraLibraryPath

spark.executor.extraClassPath
spark.executor.extraJavaOptions
spark.executor.extraLibraryPath

spark.executorEnv.[EnvironmentVariableName]
```

(3) Shuffle Behavior


(4) Spark UI


(5) Compression and Serialization

```
spark.broadcast.compress
spark.rdd.compress

spark.io.compression.codec = lz4

spark.serializer
```

(6) Memory Management

```
spark.memory.fraction
spark.memory.storageFraction

spark.memory.offHeap.enabled
spark.memory.offHeap.size

spark.memory.useLegacyMode
The legacy mode rigidly partitions the heap space into fixed-size regions, potentially leading to excessive spilling if the application was not tuned.
```

(7) Execution Behavior

```
spark.executor.cores
spark.executor.heartbeatInterval
```

(8) ?



(9) Scheduling


(10) Dynamic Allocation


## 2. Hadoop


## 3. Hive

```
spark.sql.hive.metastore.version
spark.sql.hive.metastore.jars
```

## 4. Cassandra

guava version issue


## 5. Zeppelin



## 6. Alluxio


