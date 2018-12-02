# interactive query
## Overview
* http://www.dbms2.com/2012/11/05/do-you-need-an-analytic-rdbms/
* https://info.jethro.io/blog/dont-forget-that-fast-queries-can-hide-stale-data-demystifying-real-time-and-interactive-for-big-data

## Industry
Databricks:
* https://databricks.com/product/databricks-delta

> Delta automatically indexes, compacts and caches data helping achieve up to 100x improved performance over Apache Spark. Delta delivers performance optimizations by automatically capturing statistics and applying various techniques to data for efficient querying.

Qubole:
* https://www.qubole.com/product/architecture/best-of-breed-engines/

> Qubole’s Spark implementation greatly improves the performance of Spark workloads with enhancements such as fast storage, distributed caching, advanced indexing, and metadata caching capabilities.

Oracle (SparkLineData):
* https://blogs.oracle.com/bigdata/interactive-data-lake-queries-at-scale
* https://www.linkedin.com/pulse/integrated-business-intelligence-big-data-stacks-harish-butani
* https://databricks.com/session/interactive-business-intelligence-and-olap-on-big-data-lakes-using-a-spark-native-fast-datamart
* Interactive Business Intelligence and OLAP on Big Data Lakes. spark summit session. https://www.youtube.com/watch?v=2UeskhLh87E

Snapdeal (India e-commerce):
* https://databricks.com/session/indicium-interactive-querying-at-scale-using-apache-spark-zeppelin-and-spark-job-server

Spark Summit other:
* https://databricks.com/session/writing-and-deploying-interactive-applications-based-on-spark
* https://databricks.com/session/spark-interactive-to-production

Snowflake:
* https://www.snowflake.com/blog/snowflake-spark-part-2-pushing-query-processing/
* http://info.snowflake.net/rs/252-RFO-227/images/Snowflake_SIGMOD.pdf

Alibaba:
* 基于Druid和Drill的OLAP引擎. 阿里巴巴. http://strata.oreilly.com.cn/hadoop-big-data-cn/hadoop-big-data-cn/public/schedule/detail/52345

Talking Data:
* 海量数据OLAP分析实践—-TD Atom Cube. http://chinahadoop.com/archives/2096

## Indexing
* https://databricks.com/session/apache-carbondata-an-indexed-columnar-file-format-for-interactive-query-with-spark-sql

## Caching

## JDBC/ODBC Server
* http://www.russellspitzer.com/2017/05/19/Spark-Sql-Thriftserver/

## Misc
* vectorization (columnar reads)
* predicate pushdown
* lazy materialization on read (lazy reads)

References:

* https://code.facebook.com/posts/370832626374903/even-faster-data-at-the-speed-of-presto-orc/
* http://techblog.netflix.com/2014/10/using-presto-in-our-big-data-platform.html
