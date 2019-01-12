# Cassandra Data Modeling
## Overview
* concepts
* data types
* DDL
* basic rules
* secondary index
* materialized view
* misc

### Concepts

compound primary key

* http://docs.datastax.com/en/glossary/doc/glossary/gloss_compound_pk.html

composite partition key

* https://docs.datastax.com/en/cql/3.3/cql/cql_using/useCompositePartitionKeyConcept.html
* https://docs.datastax.com/en/cql/3.3/cql/cql_using/useCompositePartitionKey.html
* http://docs.datastax.com/en/glossary/doc/glossary/gloss_composite_pk.html

## data types

### text, varchar
text is just an alias for varchar:

```
cqlsh> CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
cqlsh> use test;
cqlsh:test> CREATE TABLE test ( empID int, first_name varchar, last_name varchar, PRIMARY KEY (empID) );
cqlsh:test> desc table test;

CREATE TABLE test.test (
    empid int PRIMARY KEY,
    first_name text,
    last_name text
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

* http://stackoverflow.com/questions/17530230/cassandra-text-vs-varchar
* http://stackoverflow.com/questions/38389957/what-is-the-difference-between-varchar-and-text-type-in-cassandra-cql

### float, double, decimal

```
CREATE TABLE decimaltest (
  pt int,
  ts timeuuid,
  price1 float,
  price2 double,
  price3 decimal,
  primary key ((pt), ts)
);

insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 888.888, 888.888, 888.888);
insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 8888.888, 8888.888, 8888.888);
insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 8888.8888, 8888.8888, 8888.8888);
insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 88888.8888, 88888.8888, 88888.8888);
insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 88888.88888, 88888.88888, 88888.88888);
insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 888888.88888, 888888.88888, 888888.88888);
insert into decimaltest(pt, ts, price1, price2, price3) values (1, now(), 888888.888888, 888888.888888, 888888.888888);

select * from decimaltest where pt = 1 order by ts;

 pt | ts                                   | price1      | price2      | price3
----+--------------------------------------+-------------+-------------+---------------
  1 | 5b69b160-7e22-11e6-8a9b-efe89d5bbf02 |     888.888 |     888.888 |       888.888
  1 | 5b6a2690-7e22-11e6-8a9b-efe89d5bbf02 |   8888.8877 |    8888.888 |      8888.888
  1 | 5b6ae9e0-7e22-11e6-8a9b-efe89d5bbf02 |  8888.88867 |   8888.8888 |     8888.8888
  1 | 5b6b8620-7e22-11e6-8a9b-efe89d5bbf02 | 88888.89062 |  88888.8888 |    88888.8888
  1 | 5b6c2260-7e22-11e6-8a9b-efe89d5bbf02 | 88888.89062 | 88888.88888 |   88888.88888
  1 | 5b6c9790-7e22-11e6-8a9b-efe89d5bbf02 |  8.8889e+05 |  8.8889e+05 |  888888.88888
  1 | 5b6e4540-7e22-11e6-8a9b-efe89d5bbf02 |  8.8889e+05 |  8.8889e+05 | 888888.888888
```

## DDL

### create
```
CREATE KEYSPACE my_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
CREATE TABLE user ( first_name text, last_name text, PRIMARY KEY (first_name)) ;
```

### Alter type issues

alter column type会引起不少问题，在将来的版本可能会禁用alter column type这个功能。

修改字段类型后，查询报错：

```
java.io.IOException: Exception during execution of SELECT ... An unexpected error occurred server side on ... java.io.IOError: java.io.EOFException: EOF after 47998 bytes out of 34155505
```

或者：

```
java.io.IOException: Exception during execution of SELECT ... An unexpected error occurred server side on ... java.io.IOError: java.lang.ArrayIndexOutOfBoundsException
```

* CASSANDRA-10309. Avoid always looking up column type. https://issues.apache.org/jira/browse/CASSANDRA-10309. 如果CASSANDRA-12443上线，这个也就没有必要了。
* CASSANDRA-11820. Altering a column's type causes EOF. Fix Version: 3.8. int -> blob, int -> varint，都有这个问题。
* CASSANDRA-12397. Altering a column's type breaks commitlog replay. https://issues.apache.org/jira/browse/CASSANDRA-12397
* CASSANDRA-12443. Remove alter type support. https://issues.apache.org/jira/browse/CASSANDRA-12443. 这个改变会加到CQL 3.4.3.


## Basic Rules of Cassandra Data Modeling
* http://www.datastax.com/dev/blog/basic-rules-of-cassandra-data-modeling

Non-Goals

* Minimize the Number of Writes
* Minimize Data Duplication

Basic Goals

* Spread data evenly around the cluster. pick a good primary key
* Minimize the number of partitions read

Model Around Your Queries

* Step 1: Determine What Queries to Support. Don’t model around relations. Don’t model around objects. Model around your queries.
* Step 2: Try to create a table where you can satisfy your query by reading (roughly) one partition. In practice, this generally means you will use roughly one table per query pattern.


### WHERE clause restrictions
* http://www.datastax.com/dev/blog/a-deep-look-to-the-cql-where-clause
* http://www.datastax.com/dev/blog/allow-filtering-explained-2


Partition keys restrictions

* The partition key columns support only two operators: = and IN
* you can use the IN operator on any partition key column
* Cassandra will require that you either restrict all the partition key columns, or none of them unless the query can use a secondary index.
* Cassandra does not support >, >=, <= and < operator directly on the partition key. Instead, it allows you to use the >, >=, <= and < operator on the partition key through the use of the token function.
* If you use a ByteOrderedPartitioner, you will then be able to perform some range queries over multiple partitions. You should nevertheless be careful. Using a ByteOrderedPartitioner is not recommended as it can result in unbalanced clusters.

Clustering column restrictions

* Clustering columns support the =, IN, >, >=, <=, <, CONTAINS and CONTAINS KEY operators in single-column restrictions and the =, IN, >, >=, <= and < operators in multi-column restrictions.
* You can see that in order to retrieve data in an efficient way without a secondary index, you need to know all the clustering key columns for you selection.
* the IN restriction can be used on any column
* Single column slice restrictions are allowed only on the last clustering column being restricted.

Regular column restrictions

* Regular columns can be restricted by =, >, >=, <= and <, CONTAINS or CONTAINS KEY restrictions if the query is a secondary index query.
* Secondary index queries allow you to restrict the returned results using the =, >, >=, <= and <, CONTAINS and CONTAINS KEY restrictions on non-indexed columns using filtering.

Partition key restrictions and Secondary indices

* When Cassandra must perform a secondary index query, it will contact all the nodes to check the part of the secondary index located on each node. If all the partition key components are restricted, Cassandra will use that information to
query only the nodes that contains the specified partition keys, which will make the query more efficient.

In UPDATE and DELETE statements all the primary key columns must be restricted and the only allowed restrictions are:

* the single-column = on any partition key or clustering columns
* the single-column IN restriction on the last partition key column


## Secondary Index


## Materialized Views

* https://docs.datastax.com/en/cql/3.3/cql/cql_using/useCreateMV.html
* http://www.datastax.com/dev/blog/new-in-cassandra-3-0-materialized-views
* http://www.datastax.com/dev/blog/materialized-view-performance-in-cassandra-3-x
* https://docs.datastax.com/en/cql/3.3/cql/cql_reference/refCreateMV.html

queries are optimized by primary key definition. Standard practice is to create the table for the query, and create a new table if a different query is needed. Until Cassandra 3.0, these additional tables had to be updated manually in the client application. A materialized view automatically receives the updates from its source table.

Secondary indexes are suited for low cardinality data. Queries of high cardinality columns on secondary indexes require Cassandra to access all nodes in a cluster, causing high read latency.

Materialized views are suited for high cardinality data. The data in a materialized view is arranged serially based on the view's primary key. Materialized views cause hotspots when low cardinality data is inserted.

Requirements for a materialized view:

* The columns of the source table's primary key must be part of the materialized view's primary key.
* Only one new column can be added to the materialized view's primary key. Static columns are not allowed.

目前（2016.8.31），presto cassandra connector还不支持materialized view，而Spark cassandra connector从1.6开始已经支持materialized view。

```
presto> SELECT user, score FROM cassandra.mykeyspace.scores WHERE user = 'pcmanus' LIMIT 1;
OK
presto> SELECT user, score FROM cassandra.mykeyspace.alltimehigh WHERE game = 'Coup' LIMIT 1;
Query 20160831_150412_00009_yr3hk failed: line 1:25: Table cassandra.mykeyspace.alltimehigh does not exist
cqlsh> SELECT user, score FROM mykeyspace.alltimehigh WHERE game = 'Coup' LIMIT 1;
OK
```

DataStax Spark Connector for Apache Cassandra, SPARKC-326, Add support for Materialized View. https://datastax-oss.atlassian.net/browse/SPARKC-326

## Misc

### Compaction Strategy

http://docs.datastax.com/en/cassandra/3.0/cassandra/dml/dmlHowDataMaintain.html#dmlHowDataMaintain__dml_which_compaction_strategy_is_best

### partition size
a good rule of thumb is to keep the maximum number of rows below 100,000 items and the disk size under 100 MB.

http://docs.datastax.com/en/landing_page/doc/landing_page/planning/planningPartitionSize.html

### about the "in" keyword

https://lostechies.com/ryansvihla/2014/09/22/cassandra-query-patterns-not-using-the-in-query-for-multiple-partitions/

The “in” keyword has it’s place such as when querying INSIDE of a partition, but by and large it’s something I wish wasn’t doable across partitions, I fixed a good dozen performance problems with it so far, and I’ve yet to see it be faster than separate queries plus async.

### Join
no join operator.

### Like
There is no LIKE operator in cassandra. It's "by design". You must use elasticsearch (Solr, Lucene) or similar solutions beside cassandra to develop search abilities.

* http://stackoverflow.com/questions/32614868/like-operator-in-cassandra-cql
* https://github.com/Stratio/cassandra-lucene-index

### Group by
目前（3.7）还不支持group by，社区已经解决，将在3.10发布。

https://issues.apache.org/jira/browse/CASSANDRA-10707

> Now that Cassandra support aggregate functions, it makes sense to support GROUP BY on the SELECT statements. It should be possible to group either at the partition level or at the clustering column level.
