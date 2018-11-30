# Hive Table

## Overview

### Conversion

```
HiveSessionStateBuilder
analyzer: Analyzer
postHocResolutionRules: Seq[Rule[LogicalPlan]]
RelationConversions.convert
HiveMetastoreCatalog.convertToLogicalRelation
HiveTableRelation -> LogicalRelation
```

## Tests

### parquet_hive_serde_upper
DDL with spark-sql:

```
CREATE TABLE parquet_hive_serde_upper (A LONG, B LONG, C LONG) STORED AS parquet LOCATION '/user/hive/warehouse/parquet_data'
```

Metastore database (MySQL):

```
467	spark.sql.sources.schema.part.0	{"type":"struct","fields":[{"name":"A","type":"long","nullable":true,"metadata":{}},{"name":"B","type":"long","nullable":true,"metadata":{}},{"name":"C","type":"long","nullable":true,"metadata":{}}]}
```

hive client:

```
hive> desc extended parquet_hive_serde_upper;
OK
a                   	bigint
b                   	bigint
c                   	bigint

Detailed Table Information	Table(tableName:parquet_hive_serde_upper, dbName:default, ..., retention:0, sd:StorageDescriptor(cols:[FieldSchema(name:a, type:bigint, comment:null), FieldSchema(name:b, type:bigint, comment:null), FieldSchema(name:c, type:bigint, comment:null)], location:file:/user/hive/warehouse/parquet_data, inputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat, compressed:false, numBuckets:-1, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe, parameters:{serialization.format=1}), bucketCols:[], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), partitionKeys:[], parameters:{totalSize=0, numRows=-1, rawDataSize=-1, EXTERNAL=TRUE, COLUMN_STATS_ACCURATE=false, spark.sql.sources.schema.part.0={"type":"struct","fields":[{"name":"A","type":"long","nullable":true,"metadata":{}},{"name":"B","type":"long","nullable":true,"metadata":{}},{"name":"C","type":"long","nullable":true,"metadata":{}}]}, numFiles=0, transient_lastDdlTime=1535035196, spark.sql.sources.schema.numParts=1, spark.sql.create.version=2.3.1}, viewOriginalText:null, viewExpandedText:null, tableType:EXTERNAL_TABLE)
```

spark-sql client:

```
spark-sql> desc extended parquet_hive_serde_upper;
A	bigint	NULL
B	bigint	NULL
C	bigint	NULL

# Detailed Table Information
Database	default
Table	parquet_hive_serde_upper
...
Created By	Spark 2.3.1
Type	EXTERNAL
Provider	hive
Table Properties	[transient_lastDdlTime=1535035196]
Location	file:/user/hive/warehouse/parquet_data
Serde Library	org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe
InputFormat	org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat
OutputFormat	org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat
Storage Properties	[serialization.format=1]
Partition Provider	Catalog
```

### parquet_hive_serde_lower
DDL with spark-sql:

```
CREATE TABLE parquet_hive_serde_lower (a LONG, b LONG, c LONG) STORED AS parquet LOCATION '/user/hive/warehouse/parquet_data'
```

Metastore database (MySQL)

```
466	spark.sql.sources.schema.part.0	{"type":"struct","fields":[{"name":"a","type":"long","nullable":true,"metadata":{}},{"name":"b","type":"long","nullable":true,"metadata":{}},{"name":"c","type":"long","nullable":true,"metadata":{}}]}
```

hive client:

```
hive> desc extended parquet_hive_serde_lower;
OK
a                   	bigint
b                   	bigint
c                   	bigint

Detailed Table Information	Table(tableName:parquet_hive_serde_lower, dbName:default, ..., retention:0, sd:StorageDescriptor(cols:[FieldSchema(name:a, type:bigint, comment:null), FieldSchema(name:b, type:bigint, comment:null), FieldSchema(name:c, type:bigint, comment:null)], location:file:/user/hive/warehouse/parquet_data, inputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat, compressed:false, numBuckets:-1, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe, parameters:{serialization.format=1}), bucketCols:[], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), partitionKeys:[], parameters:{totalSize=0, numRows=-1, rawDataSize=-1, EXTERNAL=TRUE, COLUMN_STATS_ACCURATE=false, spark.sql.sources.schema.part.0={"type":"struct","fields":[{"name":"a","type":"long","nullable":true,"metadata":{}},{"name":"b","type":"long","nullable":true,"metadata":{}},{"name":"c","type":"long","nullable":true,"metadata":{}}]}, numFiles=0, transient_lastDdlTime=1535035180, spark.sql.sources.schema.numParts=1, spark.sql.create.version=2.3.1}, viewOriginalText:null, viewExpandedText:null, tableType:EXTERNAL_TABLE)
```

spark-sql client:

```
spark-sql> desc extended parquet_hive_serde_lower;
a	bigint	NULL
b	bigint	NULL
c	bigint	NULL

# Detailed Table Information
Database	default
Table	parquet_hive_serde_lower
...
Created By	Spark 2.3.1
Type	EXTERNAL
Provider	hive
Table Properties	[transient_lastDdlTime=1535035180]
Location	file:/user/hive/warehouse/parquet_data
Serde Library	org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe
InputFormat	org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat
OutputFormat	org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat
Storage Properties	[serialization.format=1]
Partition Provider	Catalog
```

### DDL with Hive CLI

```
hive> CREATE TABLE hive_lower(a BIGINT, b BIGINT) STORED AS parquet;

hive> desc extended hive_lower;
OK
a                   	bigint
b                   	bigint

Detailed Table Information	Table(tableName:hive_lower, dbName:default, ..., retention:0, sd:StorageDescriptor(cols:[FieldSchema(name:a, type:bigint, comment:null), FieldSchema(name:b, type:bigint, comment:null)], location:file:/user/hive/warehouse/hive_lower, inputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat, compressed:false, numBuckets:-1, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe, parameters:{serialization.format=1}), bucketCols:[], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), partitionKeys:[], parameters:{transient_lastDdlTime=1535338117}, viewOriginalText:null, viewExpandedText:null, tableType:MANAGED_TABLE)
```

```
hive> CREATE TABLE hive_upper(A BIGINT, B BIGINT) STORED AS parquet;

hive> desc extended hive_upper;
OK
a                   	bigint
b                   	bigint

Detailed Table Information	Table(tableName:hive_upper, dbName:default, ..., retention:0, sd:StorageDescriptor(cols:[FieldSchema(name:a, type:bigint, comment:null), FieldSchema(name:b, type:bigint, comment:null)], location:file:/user/hive/warehouse/hive_upper, inputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat, compressed:false, numBuckets:-1, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe, parameters:{serialization.format=1}), bucketCols:[], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), partitionKeys:[], parameters:{transient_lastDdlTime=1535338124}, viewOriginalText:null, viewExpandedText:null, tableType:MANAGED_TABLE)
```

## Configuration

### SQLConf
spark.sql.hive.caseSensitiveInferenceMode:

```
  val HIVE_CASE_SENSITIVE_INFERENCE = buildConf("spark.sql.hive.caseSensitiveInferenceMode")
    .doc("Sets the action to take when a case-sensitive schema cannot be read from a Hive " +
      "table's properties. Although Spark SQL itself is not case-sensitive, Hive compatible file " +
      "formats such as Parquet are. Spark SQL must use a case-preserving schema when querying " +
      "any table backed by files containing case-sensitive field names or queries may not return " +
      "accurate results. Valid options include INFER_AND_SAVE (the default mode-- infer the " +
      "case-sensitive schema from the underlying data files and write it back to the table " +
      "properties), INFER_ONLY (infer the schema but don't attempt to write it to the table " +
      "properties) and NEVER_INFER (fallback to using the case-insensitive metastore schema " +
      "instead of inferring).")
    .stringConf
    .transform(_.toUpperCase(Locale.ROOT))
    .checkValues(HiveCaseSensitiveInferenceMode.values.map(_.toString))
    .createWithDefault(HiveCaseSensitiveInferenceMode.INFER_AND_SAVE.toString)
```

### HiveUtils

spark.sql.hive.convertMetastoreParquet:

```
  val CONVERT_METASTORE_PARQUET = buildConf("spark.sql.hive.convertMetastoreParquet")
    .doc("When set to true, the built-in Parquet reader and writer are used to process " +
      "parquet tables created by using the HiveQL syntax, instead of Hive serde.")
    .booleanConf
    .createWithDefault(true)
```

spark.sql.hive.convertMetastoreParquet.mergeSchema:

```
  val CONVERT_METASTORE_PARQUET_WITH_SCHEMA_MERGING =
    buildConf("spark.sql.hive.convertMetastoreParquet.mergeSchema")
      .doc("When true, also tries to merge possibly different but compatible Parquet schemas in " +
        "different Parquet data files. This configuration is only effective " +
        "when \"spark.sql.hive.convertMetastoreParquet\" is true.")
      .booleanConf
      .createWithDefault(false)
```

spark.sql.hive.convertMetastoreOrc:

```
  val CONVERT_METASTORE_ORC = buildConf("spark.sql.hive.convertMetastoreOrc")
    .doc("When set to true, the built-in ORC reader and writer are used to process " +
      "ORC tables created by using the HiveQL syntax, instead of Hive serde.")
    .booleanConf
    .createWithDefault(true)
```
