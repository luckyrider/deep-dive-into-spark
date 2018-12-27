# Spark App Performance Tuning

## Overview
workflow
1. profile and locate bottleneck
2. look for options and try options
3. evaluate

## Performance Tuning

### Resource Management and Job Scheduling
* spark.dynamicAllocation.enabled
* speculative execution
* data locality

### Memory Management
* GC tuning, G1GC

spark.executor.memory
spark.memory.fraction
spark.memory.offHeap.enabled

### Data Management
* Parquet (vectorized reading, splittable)
* File based data source (partitioning and bucketing)
* File size, Too many small files
* Filtering, Predicate Pushdown
* Cache
* Data Skew

### Join Optimization
* Broadcast vs Sort-merge-join
* spark.sql.autoBroadcastJoinThreshold
* Hint
* Shuffle, shuffle partitions

### Tungsten Execution
* Avoid UDF
* spark.sql.codegen.hugeMethodLimit


### Misc
* Object Serialization
spark.serializer = org.apache.spark.serializer.KryoSerializer

## References

### Spark performance tuning from the trenches. 
Docs:

* https://medium.com/teads-engineering/spark-performance-tuning-from-the-trenches-7cbde521cf60
* https://medium.com/teads-engineering/spark-from-the-trenches-part-2-f2ff9ab67ea1

Key points:

* How to leverage Tungsten
  * Use Dataset structures rather than RDD
  * Avoid User-Defined Functions (UDFs) as much as possible, use Spark SQL built-in functions 
    whenever possible, implement and extend Catalyst’s (Spark’s SQL optimizer) expression class if
    needed.
  * Avoid User-Defined Aggregate Functions (UDAFs). A UDAF generates SortAggregate operations which
    are significantly slower than HashAggregate. using a built-in equivalent
  * Avoid UDFs or UDAFs that perform more than one thing
* Execution plan analysis
  * CBO
  * Hint
  * AE
* Data management (caching, broadcasting)
  * Highly imbalanced datasets, aka data skew. check stage page
  * Inappropriate use of caching. check storage page
  * Broadcasting. Hive table or file data source only.
* Cloud-related optimizations (including S3)
  * A few precautions using S3
    * spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version 2
    * spark.speculation false
    * Netflix s3committer: https://github.com/rdblue/s3committer
    * Spark supports predicate pushdown with Parquet
* Operation tricks
  * monitoring spark applications
    * Spark MetricsSystem
    * CPU: https://github.com/criteo/babar
  * Log management
    * log4j appender
  * Troubleshooting with logs
    * gc log analysis
* Using external data sources with JDBC
  * JDBC data source tips

### Optimizing Spark jobs for maximum performance
Docs:

* https://michalsenkyr.github.io/2018/01/spark-performance

Key points:

* Development of Spark jobs seems easy enough on the surface and for the most part it really is. The
  provided APIs are pretty well designed and feature-rich. Unfortunately, to implement your jobs in
  an optimal way, you have to know quite a bit about Spark and its internals.
* Transformation
  * RDD
    * The rule of thumb here is to always work with the minimal amount of data at transformation boundaries.
    * There is another rule of thumb that can be derived from this: use rich transformations, i.e.
      always do as much as possible in the context of a single transformation. A useful tool for
      that is the combineByKeyWithClassTag method.
  * DataFrame
    * optimization
  * Dataset
    * type safety
* Partitioning
  * data skew. common keys (e.g. null keys are a common special case). An efficient solution is to
    separate the relevant records, introduce a salt (random value) to their keys and perform the
    subsequent action (e.g. reduce) for them in multiple stages to get the correct result. using
    map-side joins if one of the datasets is small enough.
  * partitioning of input data: spark.sql.files.maxPartitionBytes, spark.sql.files.openCostInBytes
  * partitioning of shuffle: spark.sql.shuffle.partitions
* Serialization
  * data serialization
    * always use spark.serializer=org.apache.spark.serializer.KryoSerializer instead of Java
      serialization. In very rare cases, Kryo can fail to serialize some classes, which is the sole
      reason why it is still not Spark’s default.
    * Tungsten
  * closure serialization
    * As closures can be quite complex, a decision was made to only support Java serialization there
* Memory management
  * driver memory: spark.driver.memory
  * executor memory
    * execution memory + storage memory + user memory + reserved + overhead
    * spark.executor.memory, spark.memory.fraction, spark.memory.storageFraction
    * keep in mind that your custom objects have to fit into the user memory.
  * Tungsten. This results in great reuse of allocated memory, effectively eliminating the need for
    garbage collection in execution memory. This optimization actually works so well that enabling
    off-heap memory has very little additional benefit (although there is still some).
* Cluster resources
  * data locality
    * spark.locality.wait
    * for HDFS I/O the number of cores per executor is thought to peak in performance at about five.
  * dynamic allocation
    * spark.dynamicAllocation.enabled
    * external shuffle service
  * speculative execution
* Additionally, there are many other techniques that may help improve performance of your Spark jobs
  even further. Namely GC tuning, proper hardware provisioning and tweaking Spark’s numerous
  configuration options.

### Diving into Spark and Parquet Workloads, by Example
Docs:

* https://db-blog.web.cern.ch/blog/luca-canali/2017-06-diving-spark-and-parquet-workloads-example

Key points:

* ...

### More
User
* Tuning Spark. Spark official documentation. http://spark.apache.org/docs/latest/tuning.html
* https://spark.apache.org/docs/latest/monitoring.html
* Chapter 19. Performance Tuning. Spark: The Definitive Guide. https://www.safaribooksonline.com/library/view/spark-the-definitive/9781491912201/ch19.html
* Apache Spark Tuning and Best Practices. Databricks Academy. https://databricks.com/training/instructor-led-training/courses/apache-spark-tuning-and-best-practices
* Optimize Apache Spark jobs. https://docs.microsoft.com/en-us/azure/hdinsight/spark/apache-spark-perf
* https://blog.cloudera.com/blog/2015/03/how-to-tune-your-apache-spark-jobs-part-1/
* https://blog.cloudera.com/blog/2015/03/how-to-tune-your-apache-spark-jobs-part-2/
* https://data-flair.training/blogs/apache-spark-performance-tuning/
* https://www.waitingforcode.com/apache-spark-sql/predicate-pushdown-spark-sql/read

Deeper
* Apache Spark 2.0 Performance Improvements Investigated With Flame Graphs. https://db-blog.web.cern.ch/blog/luca-canali/2016-09-spark-20-performance-improvements-investigated-flame-graphs
* Deep Dive into Spark SQL with Advanced Performance Tuning. https://www.slideshare.net/databricks/deep-dive-into-spark-sql-with-advanced-performance-tuning-with-xiao-li-wenchen-fan

