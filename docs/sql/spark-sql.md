# Spark SQL

## Overview

## TOC

### Framework
* [Catalyst](catalyst)
* [Tungsten](tungsten)

### SQL features
subquery

* https://issues.apache.org/jira/browse/SPARK-18455
* https://issues.apache.org/jira/browse/SPARK-18863
* https://issues.apache.org/jira/browse/SPARK-19047
* https://issues.apache.org/jira/browse/SPARK-16161


## References
* https://www.slideshare.net/databricks/deep-dive-into-spark-sql-with-advanced-performance-tuning-with-xiao-li-wenchen-fan

## Query

### create temporary view using/as

```
CREATE TEMPORARY VIEW user
USING org.apache.spark.sql.cassandra
OPTIONS (
    keyspace 'test',
    table 'user'
);

CREATE TEMPORARY VIEW temp1 AS SELECT * FROM user WHERE id >= 2;

CREATE TEMPORARY VIEW temp2 AS SELECT * FROM temp1 WHERE id <= 3;

select count(*) FROM temp2;
```

* https://issues.apache.org/jira/browse/SPARK-15674
* https://issues.apache.org/jira/browse/SPARK-16267

### CTE: common table expression

```
with q1 as (select... from... where...),
q2 as (select... from... where...)
select... from q1 join q2 where...;
```

```
with q1 as (...)
from q1
insert into table t1 select *
insert into table t2 select *;
```

后面定义的query可以引用前面定义的query:

```
with q1 as ()
q2 as (select from q1)
q3 as ( select from q2)
from q3 
insert 
insert
```

## DataFrame
```
cat /home/vagrant/dataplatform/spark/examples/src/main/resources/people.json
{"name":"Michael"}
{"name":"Andy", "age":30}
{"name":"Justin", "age":19}
```

```
val df = sqlContext.read.json("/home/vagrant/dataplatform/spark/examples/src/main/resources/people.json")
val path = "/home/vagrant/dataplatform/spark/examples/src/main/resources/people.txt"
val people = sc.textFile(path).map(_.split(",")).map(p => Person(p(0), p(1).trim.toInt)).toDF()
val df = sqlContext.read.load("/home/vagrant/dataplatform/spark/examples/src/main/resources/users.parquet")
df.select("name", "favorite_color").write.save("/home/vagrant/dataplatform/spark/namesAndFavColors.parquet")
val df = sqlContext.read.format("json").load("/home/vagrant/dataplatform/spark/examples/src/main/resources/people.json")
df.select("name", "age").write.format("parquet").save("/home/vagrant/dataplatform/spark/namesAndAges.parquet")
val df = sqlContext.sql("SELECT * FROM parquet.`/home/vagrant/dataplatform/spark/examples/src/main/resources/users.parquet`")
```

## HiveContext

* spark.sql.hive.metastore.version
* spark.sql.hive.metastore.jars
* hive-site.xml放到classpath下面

## Data Sources API

```
CREATE TEMPORARY TABLE tmpTable
USING org.apache.spark.sql.cassandra
OPTIONS (
  table "table",
  keyspace "keyspace",
  cluster "test_cluster",
  pushdown "true",
  spark.cassandra.input.fetch.size_in_rows "10",
  spark.cassandra.output.consistency.level "ONE",
  spark.cassandra.connection.timeout_ms "1000"
)
```

相关源码：

* org.apache.spark.sql.execution.datasources ddl.scala
  * CreateTableUsing
  * CreateTableUsingAsSelect
  * CreateTempViewUsing
* org.apache.spark.sql.hive.execution.SQLViewSuite

参考资料：

* https://databricks.com/blog/2015/01/09/spark-sql-data-sources-api-unified-data-access-for-the-spark-platform.html
* https://github.com/datastax/spark-cassandra-connector/blob/master/doc/14_data_frames.md
* https://github.com/datastax/spark-cassandra-connector/blob/master/spark-cassandra-connector/src/main/scala/org/apache/spark/sql/cassandra/DefaultSource.scala

## References
* https://docs.databricks.com/spark/latest/spark-sql/index.html
* Deep Dive into Spark SQL’s Catalyst Optimizer. https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html
* http://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf
* https://databricks.com/blog/2015/04/24/recent-performance-improvements-in-apache-spark-sql-python-dataframes-and-more.html
* https://databricks.com/blog/2015/04/28/project-tungsten-bringing-spark-closer-to-bare-metal.html
