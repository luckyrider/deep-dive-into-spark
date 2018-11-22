# Presto Study Notes

## overview

download:

* https://repo1.maven.org/maven2/com/facebook/presto/presto-server

## Presto Connectors

### Presto Cassandra Connector

(1) java driver和cassandra集群之间版本不兼容

报错：

```
com.datastax.driver.core.exceptions.InvalidQueryException: unconfigured table schema_keyspaces
```

* Cassandra 3 with Presto. https://groups.google.com/forum/#!topic/presto-users/SAOnYriaQzw
* http://stackoverflow.com/questions/34117374/com-datastax-driver-core-exceptions-invalidqueryexception-unconfigured-table-sc

java driver和cassandra版本的兼容性列表: http://datastax.github.io/java-driver/manual/native_protocol/

Older supported releases. http://cassandra.apache.org/download/

```
The following older Cassandra releases are still supported:

* Apache Cassandra 3.0 is supported until May 2017. The latest release is 3.0.8 (pgp, md5 and sha1), released on 2016-07-05.
* Apache Cassandra 2.2 is supported until November 2016. The latest release is 2.2.7 (pgp, md5 and sha1), released on 2016-07-05.
* Apache Cassandra 2.1 is supported until November 2016 with critical fixes only. The latest release is 2.1.15 (pgp, md5 and sha1), released on 2016-07-05.
```

For release date, see:

https://en.wikipedia.org/wiki/Apache_Cassandra

https://github.com/prestodb/presto/issues/4364. Add support for cassandra 3.+ #4364

总结来说，Presto从0.146开始采用java driver 3.0.0能够访问cassandra 3.x集群。

(2) Unable to connect to server xxx:9160

```
presto> select * from cassandra.my_keyspace.user;
Query 20160828_142416_00014_bammg failed: java.io.IOException: Unable to connect to server localhost:9160
```

https://github.com/scylladb/scylla/issues/1139. Presto会根据具体情况使用CQL port或者Thrift port，所以Thrift port必须打开，否则有可能报错。Cassandra有类似的问题。

> Look like Presto use both CQL and Thrift for some reason, and choose one base on the case.

解决办法：

```
$ nodetool enablethrift
```

(3) This connector does not support inserts

```
presto> insert into cassandra.my_keyspace.invites(ds,foo,bar) values('2008-08-07', 1000, 'val_1000');
Query 20160828_154431_00031_bammg failed: This connector does not support inserts
```

com.facebook.presto.spi.connector.ConnectorMetadata

```
    default ConnectorInsertTableHandle beginInsert(ConnectorSession session, ConnectorTableHandle tableHandle)
    {
        throw new PrestoException(NOT_SUPPORTED, "This connector does not support inserts");
    }
```

最新的（0.153-SNAPSHOT）cassandra connector代码，com.facebook.presto.cassandra CassandraMetadata没有覆盖父类ConnectorMetadata的beginInsert，所以可以确定即使是最新的cassandra connector也还不支持insert，所以cassandra connector目前不支持insert。

(4) create table

from cassandra to hive:

```
presto>
create table hive.default.users
WITH (format = 'ORC')
AS
SELECT * from cassandra.mykeyspace.users;

hive> show create table users;
OK
CREATE  TABLE `users`(
  `user_id` int,
  `fname` string,
  `lname` string)
COMMENT 'Created by Presto'
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  'hdfs://host1/user/hive/warehouse/users'
TBLPROPERTIES (
  'totalSize'='493',
  'numRows'='-1',
  'rawDataSize'='-1',
  'COLUMN_STATS_ACCURATE'='false',
  'numFiles'='1',
  'transient_lastDdlTime'='1472457201')
Time taken: 0.232 seconds, Fetched: 20 row(s)
```

from hive to cassandra:

```
create table cassandra.mykeyspace.users2
AS
SELECT * from hive.default.users;

cqlsh:mykeyspace> desc users2;

CREATE TABLE mykeyspace.users2 (
    id uuid PRIMARY KEY,
    fname text,
    lname text,
    user_id int
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = 'Presto Metadata: [{"name":"id","hidden":true},{"name":"user_id","hidden":false},{"name":"fname","hidden":false},{"name":"lname","hidden":false}]'
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

```
presto> SELECT * FROM system.metadata.table_properties;
 catalog_name | property_name  | default_value |      type      |            description
--------------+----------------+---------------+----------------+-----------------------------------
 hive         | bucket_count   | 0             | bigint         | Number of buckets
 hive         | clustered_by   | []            | array(varchar) | Bucketing columns
 hive         | format         | RCBINARY      | varchar        | Hive storage format for the table
 hive         | partitioned_by | []            | array(varchar) | Partition columns
(4 rows)
```

(5) join tables from different catalogs

* Join cassandra.table and hive.table with Presto. https://groups.google.com/forum/#!topic/presto-users/rb0ormCjorw. 

> Yes, you need to use the fully qualified table names including the catalog:
> 
> SELECT ...
> FROM hive.schema.table
> JOIN cassandra.schema.table ...
> 
> Doing joins across connectors is one of the most powerful and useful features of Presto.

* Can we use mysql and cassandra both in PrestoDB via connector? http://stackoverflow.com/questions/35569881/can-we-use-mysql-and-cassandra-both-in-prestodb-via-connector

> Yes, and presto is the perfect choice for this kind of query.
> Here is a tutorial of how to combine data in hive and mysql using presto, but combine data in cassandra and mysql should be similar.
> http://getindata.com/blog/tutorials/tutorial-using-presto-to-combine-data-from-hive-and-mysql-in-one-sql-like-query/

测试数据和查询例子：https://gist.github.com/tzach/7d3a4540264418fdb15aa9fa159e0188

```
cqlsh> 
CREATE KEYSPACE mykeyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
use mykeyspace ;
CREATE TABLE users (user_id int PRIMARY KEY, fname text, lname text);
insert into users (user_id , fname, lname) values (1, 'tzach', 'livyatan');
insert into users (user_id , fname, lname) values (2, 'dor', 'laor');                                                               
insert into users (user_id , fname, lname) values (3, 'shlomi', 'laor');                                                            
insert into users (user_id , fname, lname) values (4, 'shlomi', 'livne');                                                           
insert into users (user_id , fname, lname) values (6, 'avi', 'kivity'); 

CREATE TABLE address (user_id int PRIMARY KEY, number int, street text, city text);
insert into address (user_id , number, street, city) values (1, 100, 'dizingof', 'tel aviv');

presto>
SELECT * FROM cassandra.mykeyspace.users where user_id >= 2 and user_id <= 3;
 user_id | fname  | lname 
---------+--------+-------
       2 | dor    | laor  
       3 | shlomi | laor  

SELECT * FROM cassandra.mykeyspace.users limit 1;
 user_id | fname |  lname   
---------+-------+----------
       1 | tzach | livyatan 

select * from cassandra.mykeyspace.users us JOIN cassandra.mykeyspace.address ad ON us.user_id = ad.user_id;
 user_id | fname |  lname   | user_id |   city   | number |  street  
---------+-------+----------+---------+----------+--------+----------
       1 | tzach | livyatan |       1 | tel aviv |    100 | dizingof
```

## Resources

### Case Study

* https://www.facebook.com/notes/facebook-engineering/presto-interacting-with-petabytes-of-data-at-facebook/10151786197628920/
* Presto实现原理和美团的使用实践. http://tech.meituan.com/presto.html
* Using Presto in our Big Data Platform on AWS. http://techblog.netflix.com/2014/10/using-presto-in-our-big-data-platform.html
* A year of using Presto in production. http://labs.gree.jp/blog/2014/12/12838/
