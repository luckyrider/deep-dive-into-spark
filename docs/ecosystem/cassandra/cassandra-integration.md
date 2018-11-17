## Cassandra Integration

## Export/Import

bulk loading into cassandra

* http://www.slideshare.net/BrianHess4/bulk-loading-into-cassandra
* http://blog.sws9f.org/nosql/2016/02/11/import-csv-to-cassandra.html

(1) front door (cql insert)

* http://www.datastax.com/dev/blog/simple-data-importing-and-exporting-with-cassandra
* https://moshimon.wordpress.com/2015/01/19/export-data-from-cassandra-to-csv/
* https://github.com/brianmhess/cassandra-loader

```
copy users(user_id, fname, lname) to '/home/vagrant/users.csv';
copy users(user_id, fname, lname) to '/home/vagrant/users2.csv' WITH DELIMITER = '|' AND QUOTE = '''' AND ESCAPE = '''' AND NULL = '<null>';
```

(2) side door (sstable)

* http://www.planetcassandra.org/blog/bulk-loading-options-for-cassandra/
* http://www.datastax.com/dev/blog/bulk-loading
* http://www.datastax.com/dev/blog/using-the-cassandra-bulk-loader-updated
* https://github.com/yukim/cassandra-bulkload-example/
* https://docs.datastax.com/en/cassandra/3.x/cassandra/tools/toolsBulkloader.html

There are two primary use cases for this new tool:

* Bulk loading external data into a cluster: for this you will have to first generate sstables for the data to load, as we will see later in this post.
* Loading pre-existing sstables, typically snapshots, into another cluster with different node counts or replication strategy.

There are two alternative techniques used for bulk loading into Cassandra: “copy-the-sstables” and sstableloader.

sstable writer:

* SSTableSimpleUnsortedWriter
* CQLSSTableWriter

(3) other

* BinaryMemtable. Although Cassandra has had the BinaryMemtable interface from the very beginning, BinaryMemtable is hard to use and provides a relatively minor throughput improvement over normal client writes.
* Consider deprecating sstable2json/json2sstable in 2.2. https://issues.apache.org/jira/browse/CASSANDRA-9618
* BulkOutputFormat. http://www.solveitinjava.com/2015/05/bulkload-to-cassandra-with-hadoop.html

## Hadoop Integration

source:

* https://github.com/apache/cassandra/tree/trunk/src/java/org/apache/cassandra/hadoop

## Hive Integration
总结来看，Hive Cassandra integration的支持不好。

Articles/Open sources

* http://stackoverflow.com/questions/20833308/how-to-convert-cassandra-to-hdfs-file-system-for-shark-hive-query. 提到了下面的几个链接。
  * https://github.com/richardalow/cassowary. Hive storage handler for Cassandra and Shark that reads the SSTables directly. 不活跃（last update is over 3 years ago）. 直接读sstable。
  * https://github.com/tuplejump/cash/tree/master/cassandra-handler. 不活跃（last update is over 2 years ago）.支持Cassandra 1.2.x。
  * https://github.com/2013Commons/hive-cassandra. Hive Cassandra storage handler with Hadoop2 and for Shark. 不活跃（last update is over 2 years ago）.
  * https://github.com/dvasilen/Hive-Cassandra. Hive Storage Handler for Cassandra (cloned from https://github.com/riptano/hive/tree/hive-0.8.1-merge/cassandra-handler, which is now https://github.com/riptano/hive_old), Use the branch dropdown to select a release for the particular combination of the Hadoop, Hive and Cassandra versions. 目前能找到的为数不多的、开源社区支持Cassandra 3.x的HiveStorageHandler，从riptano早期的版本fork而来。
* Cassandra integration with Hadoop. http://stackoverflow.com/questions/20019087/cassandra-integration-with-hadoop. 提到下面几个链接：
  * 链接已经不存在。https://github.com/milliondreams/hive.git
  * http://www.planetcassandra.org/blog/hive-support-for-cassandra-cql3/. September 5th, 2013。Though the code includes support for both CQL3 tables and thrift tables separately by CqlStorageHandler and CassandraStorageHandler, this blog covers using CqlStorageHandler for creating CQL3 tables in cassandra through hive. 文中提到了上面这个链接https://github.com/milliondreams/hive.git，已经没有了。
  * http://wiki.apache.org/cassandra/HadoopSupport. Apache Hive support was done as part of a DataStax development effort. See https://github.com/riptano/hive for details. There are plans to integrate this support into the Cassandra core source tree (see CASSANDRA-4131). 实际上Cassandra社区没有人维护Hive-Cassandra集成，特别是在3.0以后，对Hive的支持已经deprecated，详见CASSANDRA-4131。
* http://planetcassandra.org/blog/support-cql3-tables-in-hadoop-pig-and-hive/. July 24th, 2013。文中提到The evolutions of Cassandra querying mechanism。

Hive JIRA

* https://issues.apache.org/jira/browse/HIVE-1434. Cassandra Storage Handler. relates to CASSANDRA-913. Edward Capriolo (Programming Hive的作者). Resolution: Won't Fix.

Cassandra JIRA

* https://issues.apache.org/jira/browse/CASSANDRA-913. Add Hive support. closing in favor of HIVE-1434.
* https://issues.apache.org/jira/browse/CASSANDRA-4131. Integrate Hive support to be in core cassandra. Aleksey Yeschenko added a comment - 18/Mar/16: Resolving as Not A Problem, for essentially the same reason that CASSANDRA-10542 (remove Pig support) happened. Cassandra核心开发者中没人维护Pig support，所以对Pig的support deprecated，Hive的情况类似。
* https://issues.apache.org/jira/browse/CASSANDRA-10542. Deprecate Pig support in 2.2 and remove it in 3.0. Created:	16/Oct/15.

DSE支持Hive和Cassandra的集成，但是DSE需要license，并且在最新版中Hadoop的集成也deprecated。

* http://www.planetcassandra.org/cassandra/
* http://www.datastax.com/2014/04/what-you-can-get-for-free-from-datastax
* http://docs.datastax.com/en/datastax_enterprise/5.0/datastax_enterprise/ana/dsehadoop/dseHadoopTOC.html
* http://docs.datastax.com/en/datastax_enterprise/5.0/datastax_enterprise/ana/dsehadoop/creatingCqlDataHive.html. 里面提到的`org.apache.hadoop.hive.cassandra.cql3.CqlStorageHandler`，没有找到Cassandra官方开源版本。

```
Analyzing data using DSE Hadoop (deprecated)
You can run analytics on Cassandra data using Hadoop that is integrated into DataStax Enterprise. The Hadoop component in DataStax Enterprise enables analytics to be run across the DataStax Enterprise distributed, shared-nothing architecture. Hadoop is deprecated for use with DataStax Enterprise. DSE Hadoop and BYOH (Bring Your Own Hadoop) are also deprecated.
```

## Presto integration



## Spark Integraion


