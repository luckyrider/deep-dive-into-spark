# Parquet

## Overview
TOC:

* parquet format
* parquet data source table
  * read path
  * write path
* hive parquet table
  * read path
  * hive dependencies
* Config

References:

* https://www.slideshare.net/RyanBlue3/parquet-performance-tuning-the-missing-guide
* https://db-blog.web.cern.ch/blog/luca-canali/2017-06-diving-spark-and-parquet-workloads-example

## Parquet format

parquet-tools:

```
hadoop jar /path/to/parquet-tools/parquet-tools-1.8.2.jar meta /path/to/table/part-00000-be26af2b-9aff-4901-ab73-d6f6cc12d3bc_00000.snappy.parquet
```

Decimal:

* https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#decimal


## Parquet data source table
### read path
org.apache.spark.sql.execution.datasources.parquet.ParquetReadSupport

## read path
Physical Plan

```
scala> sql("select a from parquet_data_source").explain
== Physical Plan ==
*(1) Project [a#22L]
+- *(1) FileScan parquet default.parquet_data_source[a#22L] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/Users/cmao/Workspace/temp/parquet_casesensitive], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<a:bigint>
```

ParquetFileFormat instantiation:

```
FileSourceStrategy.apply
FileSourceScanExec()
```

ParquetFileFormat execution:

```
SparkPlan.execute
SparkPlan.doExecute
DataSourceScanExec.doExecute
FileSourceScanExec.inputRDD
ParquetFileFormat.buildReaderWithPartitionValues
VectorizedParquetRecordReader.initialize
SpecificParquetRecordReaderBase.initialize
ParquetReadSupport.init
```

`DataFrameReader`, Duplicated fields resolution:

```
org.apache.spark.sql.AnalysisException: Found duplicate column(s) in the data schema: `c`;
  at org.apache.spark.sql.util.SchemaUtils$.checkColumnNameDuplication(SchemaUtils.scala:85)
  at org.apache.spark.sql.util.SchemaUtils$.checkColumnNameDuplication(SchemaUtils.scala:67)
  at org.apache.spark.sql.execution.datasources.DataSource.resolveRelation(DataSource.scala:421)
  at org.apache.spark.sql.DataFrameReader.loadV1Source(DataFrameReader.scala:239)
  at org.apache.spark.sql.DataFrameReader.load(DataFrameReader.scala:227)
  at org.apache.spark.sql.DataFrameReader.parquet(DataFrameReader.scala:622)
  at org.apache.spark.sql.DataFrameReader.parquet(DataFrameReader.scala:606)
```

### write path
DataFrameWriter.saveAsTable

```
val data = spark.range(5).selectExpr("id as a", "id * 2 as B", "id * 3 as c", "id * 4 as C")
data.write.format("parquet").mode("overwrite").saveAsTable("spark_tests.parquet_table")

18/08/23 15:02:01 INFO HiveExternalCatalog: Persisting file based data source table `default`.`parquet_table` into Hive metastore in Hive compatible format.
18/08/23 15:02:01 WARN HiveExternalCatalog: Could not persist `default`.`parquet_table` in a Hive compatible way. Persisting it into Hive metastore in Spark SQL specific format.
org.apache.hadoop.hive.ql.metadata.HiveException: org.apache.hadoop.hive.ql.metadata.HiveException: Duplicate column name c in the table definition.
	at org.apache.hadoop.hive.ql.metadata.Hive.createTable(Hive.java:720)
    ...
	at org.apache.spark.sql.hive.client.HiveClientImpl.createTable(HiveClientImpl.scala:466)
	at org.apache.spark.sql.hive.HiveExternalCatalog.saveTableIntoHive(HiveExternalCatalog.scala:479)
	at org.apache.spark.sql.hive.HiveExternalCatalog.org$apache$spark$sql$hive$HiveExternalCatalog$$createDataSourceTable(HiveExternalCatalog.scala:367)
	...
	at org.apache.spark.sql.hive.HiveExternalCatalog.doCreateTable(HiveExternalCatalog.scala:216)
	at org.apache.spark.sql.catalyst.catalog.ExternalCatalog.createTable(ExternalCatalog.scala:119)
	at org.apache.spark.sql.catalyst.catalog.SessionCatalog.createTable(SessionCatalog.scala:304)
	at org.apache.spark.sql.execution.command.CreateDataSourceTableAsSelectCommand.run(createDataSourceTables.scala:184)
	...
	at org.apache.spark.sql.execution.command.DataWritingCommandExec.doExecute(commands.scala:122)
	...
	at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:151)
	at org.apache.spark.sql.execution.SparkPlan.executeQuery(SparkPlan.scala:152)
	at org.apache.spark.sql.execution.SparkPlan.execute(SparkPlan.scala:127)
	at org.apache.spark.sql.execution.QueryExecution.toRdd$lzycompute(QueryExecution.scala:80)
	...
	at org.apache.spark.sql.execution.SQLExecution$.withNewExecutionId(SQLExecution.scala:77)
	at org.apache.spark.sql.DataFrameWriter.runCommand(DataFrameWriter.scala:654)
	at org.apache.spark.sql.DataFrameWriter.createTable(DataFrameWriter.scala:458)
	at org.apache.spark.sql.DataFrameWriter.saveAsTable(DataFrameWriter.scala:437)
	at org.apache.spark.sql.DataFrameWriter.saveAsTable(DataFrameWriter.scala:393)
Caused by: org.apache.hadoop.hive.ql.metadata.HiveException: Duplicate column name c in the table definition.
	at org.apache.hadoop.hive.ql.metadata.Table.validateColumns(Table.java:952)
	at org.apache.hadoop.hive.ql.metadata.Table.checkValidity(Table.java:216)
	at org.apache.hadoop.hive.ql.metadata.Hive.createTable(Hive.java:698)
```

## hive parquet table

### read path
Physical Plan

```
scala> sql("select a from parquet_hive_serde").explain
== Physical Plan ==
HiveTableScan [a#187L], HiveTableRelation `default`.`parquet_hive_serde`, org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe, [a#187L, b#188L]
```

Invocation chain:

```
org.apache.spark.sql.hive.execution.HiveTableScanExec
org.apache.spark.sql.hive.HadoopTableReader (extendes org.apache.spark.sql.hive.TableReader)
org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat (extends org.apache.hadoop.mapred.FileInputFormat)
org.apache.hadoop.hive.ql.io.parquet.read.ParquetRecordReaderWrapper (extends org.apache.hadoop.mapred.RecordReader)
parquet.hadoop.ParquetRecordReader
parquet.hadoop.InternalParquetRecordReader
org.apache.hadoop.hive.ql.io.parquet.read.DataWritableReadSupport (extends parquet.hadoop.api.ReadSupport)
```

`DataWritableReadSupport#getFieldTypeIgnoreCase`
> Searchs for a fieldName into a parquet GroupType by ignoring string case.


HiveTableScanExec instantiation:

```
HiveTableScanExec()
hadoopReader
hadoopConf
addColumnMetadataToConf
```

HiveTableScanExec execution:

```
SparkPlan.execute
SparkPlan.doExecute
HiveTableScanExec.doExecute
```

### hive dependencies
```
org.apache.hadoop.hive.ql = org.spark-project.hive:hive-exec:1.2.1.spark2
parquet.hadoop = com.twitter:parquet-hadoop-bundle:1.6.0
```

```
org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe
```

Spark -> Parquet:

```
2.4 -> 1.10.0
2.3 -> 1.8.3
2.1 -> 1.8.1
```

hive -> parquet:

```
hive.parquet == 1.6.0
```

## Config

### spark.sql.parquet.writeLegacyFormat
https://github.com/apache/spark/pull/6617#issue-36865469

> ... it generates standard Parquet schemas conforming to the most updated Parquet format spec. Converting to old style Parquet schemas is also supported via feature flag spark.sql.parquet.followParquetFormatSpec ...
>
> It implements backwards-compatibility rules described in the most updated Parquet format spec. Thus can recognize more schema patterns generated by other/legacy systems/tools.

https://github.com/apache/spark/pull/8566#issue-43960214

> We introduced SQL option spark.sql.parquet.followParquetFormatSpec while working on implementing Parquet backwards-compatibility rules in SPARK-6777. It indicates whether we should use legacy Parquet format adopted by Spark 1.4 and prior versions or the standard format defined in parquet-format spec to write Parquet files.
> Would be nice to rename it to spark.sql.parquet.writeLegacyFormat, and invert its default value (the two option names have opposite meanings).

https://github.com/apache/spark/pull/7679#issuecomment-125654243

> Another important fact to notice is that we've recently removed unlimited decimal type and restricted max decimal precision to 38.

