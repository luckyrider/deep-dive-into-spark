# Kudu Study Notes

## 1. Overview

fast analytics on fast data

官网上说处于beta，not production-ready，版本release比较快，2到3个月发布一个新版本，最新版0.9.0（2016.6.9），下一个版本是1.0.0

Cloudera官方blog：http://blog.cloudera.com/blog/2015/09/kudu-new-apache-hadoop-storage-for-fast-analytics-on-fast-data/

作者Todd Lipcon，Hadoop PMC，HBase Committer，Thrift Committer

* http://blog.cloudera.com/blog/2012/10/meet-the-engineer-todd-lipcon/

2016.7.25 成为Apache Top Level Project

* The Apache Software Foundation Announces Apache® Kudu™ as a Top-Level Project. https://blogs.apache.org/foundation/entry/apache_software_foundation_announces_apache

Much Ado about Kudu. https://www.mapr.com/blog/much-ado-about-kudu. MapR的广告贴，说Kudu只是MapR-DB的子集，并且MapR在6年前就意识到了所以有了MapR-DB，从侧面证明了Kudu的价值所在。下面两点说得倒挺有道理，In short, Kudu seems to be aimed at:

* Reducing architectural complexity
* Performance (for table-based operations)

https://www.quora.com/Does-Clouderas-new-storage-engine-Kudu-support-joins

Jean-Daniel Cryans, I've been working on Kudu at Cloudera for the past two years.

Kudu is just a storage engine, apart from simple insert/update/delete/scans operations it won't start doing SQL for you. In order to join tables you need to use a query engine. Kudu is already integrated in Cloudera Impala, and it is documented here[1]. With this combination you can join Kudu tables together, or Kudu tables with Parquet tables, etc

You could do the same with Apache Drill, Presto, and others once they are able to use Kudu.


## 2. Fundamentals



## 3. Ecosystem

### Impala Integration


### Spark Integration
Kudu社区官方支持，还在开发中，目标是1.0.0

* Add Integration points for Spark, Spark Streaming, and Spark SQL. https://issues.apache.org/jira/browse/KUDU-1214


### Flume Integration

* https://issues.apache.org/jira/browse/KUDU-431
* https://issues.apache.org/jira/browse/KUDU-1416

### Presto Integration
没有官方支持。有一个非官方的，详见下面这个JIRA，Kotlin编写，作者不打算长期维护。

* Integrate with Presto. https://issues.apache.org/jira/browse/KUDU-446

### Other

* Drill

## 4. Case Study

### 4.1 Xiaomi


### 4.2 Build a Prediction Engine using Spark, Kudu, and Impala

* How-to: Build a Prediction Engine using Spark, Kudu, and Impala. http://blog.cloudera.com/blog/2016/05/how-to-build-a-prediction-engine-using-spark-kudu-and-impala/


### 4.3 Kudu as a Kafka replacement

* http://blog.rodeo.io/2016/01/24/kudu-as-a-more-flexible-kafka.html
* https://news.ycombinator.com/item?id=10974305

讨论里面也提到了Elasticsearch和Kudu的选型问题。

