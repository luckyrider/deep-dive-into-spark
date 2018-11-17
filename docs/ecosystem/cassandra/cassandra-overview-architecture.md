# Cassandra Overview and Architecture

## Overview
### benchmark

* http://www.datastax.com/nosql-databases/benchmarks-cassandra-vs-mongodb-vs-Hbase
* http://www.datastax.com/apache-cassandra-leads-nosql-benchmark
* https://www.linkedin.com/pulse/real-comparison-nosql-databases-hbase-cassandra-mongodb-sahu
* https://www.oreilly.com/ideas/apache-cassandra-for-analytics-a-performance-and-storage-analysis
* http://www.planetcassandra.org/nosql-performance-benchmarks/
* http://www.datastax.com/dev/blog/materialized-view-performance-in-cassandra-3-x
* https://www.instaclustr.com/blog/2016/01/07/multi-data-center-apache-spark-and-apache-cassandra-benchmark/
* https://www.instaclustr.com/blog/2016/04/21/multi-data-center-sparkcassandra-benchmark-round-2/

### Case Study
* http://planetcassandra.org/blog/revisiting-1-million-writes-per-second/
* Experience building an OLAP engine on Spark and Cassandra. http://engineering.ooyala.com/blog/experience-building-olap-engine-spark-and-cassandra
* 许鹏：使用Spark+Cassandra打造高性能数据分析平台
  * http://www.csdn.net/article/2014-10-24/2822278-how-to-bulida-spark-and-cassandra-based-high-performance-data-pipeline
  * http://www.csdn.net/article/2014-11-14/2822652-how-to-bulida-spark-and-cassandra-based-high-performance-data-pipeline-2
* integrate real time and batch
  * http://www.slideshare.net/MarkedUpAnalytics/real-time-analytics-with-cassandra-hive-and-solr
* FiloDB
  * http://www.infoq.com/cn/news/2015/11/FiloDB-API-NoSQL
  * https://github.com/tuplejump/FiloDB
* http://www.zhihu.com/question/49370798

### books/articles
* Cassandra: The Definitive Guide 2nd Edition. by Carpenter and Hewitt. 2016/6/27, second release. https://www.amazon.com/Cassandra-Definitive-Guide-Carpenter/dp/1491933666
* https://github.com/jeffreyscarpenter/cassandra-guide
* https://databricks.com/blog/2014/05/08/databricks-and-datastax.html


## Architecture

### Partitioner
https://docs.datastax.com/en/cassandra/3.x/cassandra/architecture/archPartitionerAbout.html
