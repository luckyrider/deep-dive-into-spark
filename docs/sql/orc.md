# ORC

## Overview
SPARK-25132 adds support for case-insensitive field resolution when reading from Parquet files. We found ORC files have similar issues, but not identical to Parquet. Spark has two OrcFileFormat.

Since SPARK-2883, Spark supports ORC inside sql/hive module with Hive dependency. This hive OrcFileFormat always do case-insensitive field resolution regardless of case sensitivity mode. When there is ambiguity, hive OrcFileFormat always returns the first matched field, rather than failing the reading operation.
SPARK-20682 adds a new ORC data source inside sql/core. This native OrcFileFormat supports case-insensitive field resolution, however it cannot handle duplicate fields.
Besides data source tables, hive serde tables also have issues. If ORC data file has more fields than table schema, we just can't read hive serde tables. If ORC data file does not have more fields, hive serde tables always do field resolution by ordinal, rather than by name.

Both ORC data source hive impl and hive serde table rely on the hive orc InputFormat/SerDe to read table. I'm not sure whether we can change underlying hive classes to make all orc read behaviors consistent.

For ORC data source native impl, there are two read path:

Read through DataFrameReader. When hitting duplicated fields in case-insensitive mode, it will throw AnalysisException, the error message is something like WARN DataSource: Found duplicate column(s) in the data schema and the partition schema
Read through data source table (persisted in metastore). When hitting duplicated fields in case-insensitive mode, it will pick the first matched field.

## ORC tables

### data source native impl
```
org.apache.spark.sql.execution.datasources.orc.OrcFileFormat
org.apache.spark.sql.execution.datasources.orc.OrcUtils
```

respect `spark.sql.caseSensitive`. But do no handle ambiguity well, return the first matched column, rather than fail the resolution.

```
        val resolver = if (isCaseSensitive) caseSensitiveResolution else caseInsensitiveResolution
        Some(requiredSchema.fieldNames.map { name => orcFieldNames.indexWhere(resolver(_, name)) })
```

### data source hive impl
```
org.apache.spark.sql.hive.orc.OrcFileFormat
org.apache.hadoop.hive.ql.io.orc.SparkOrcNewRecordReader
org.apache.hadoop.hive.ql.io.orc.OrcStruct.OrcStructInspector
```

`OrcStructInspector#getStructFieldRef`:

```
    public StructField getStructFieldRef(String s) {
      for(StructField field: fields) {
        if (field.getFieldName().equalsIgnoreCase(s)) {
          return field;
        }
      }
      return null;
    }
```

Field resolution is always case insensitive.

### hive serde table

```
org.apache.spark.sql.hive.execution.HiveTableScanExec
org.apache.spark.sql.hive.HadoopTableReader (extendes org.apache.spark.sql.hive.TableReader)
org.apache.spark.rdd.HadoopRDD
org.apache.hadoop.hive.ql.io.orc.OrcInputFormat
org.apache.hadoop.hive.ql.io.orc.OrcInputFormat.NullKeyRecordReader (implements AcidRecordReader<NullWritable, OrcStruct>)
anonymous inner class RowReader (exntends org.apache.hadoop.hive.ql.io.AcidInputFormat.RowReader<OrcStruct>)
org.apache.hadoop.hive.ql.io.orc.OrcRawRecordMerger (implements AcidInputFormat.RawReader<OrcStruct>)
org.apache.hadoop.hive.ql.io.orc.OrcRawRecordMerger.OriginalReaderPair
org.apache.hadoop.hive.ql.io.orc.ReaderImpl (implements org.apache.hadoop.hive.ql.io.orc.Reader, created via OrcFile.createReader)
org.apache.hadoop.hive.ql.io.orc.RecordReaderImpl (implements org.apache.hadoop.hive.ql.io.orc.RecordReader)
```

```
spark.conf.set("spark.sql.caseSensitive", true)
spark.conf.set("spark.sql.hive.convertMetastoreOrc", false)
val data = spark.range(1).selectExpr("id + 1 as x", "id + 2 as y", "id + 3 as z")
data.write.format("orc").mode("overwrite").save("/user/hive/warehouse/orc_data_xyz")
sql("CREATE TABLE orc_table_ABC (A LONG, B LONG, C LONG) STORED AS orc LOCATION '/user/hive/warehouse/orc_data_xyz'")
sql("select B from orc_table_ABC").show
+---+
|  B|
+---+
|  2|
+---+
```

Field resolution is by ordinal, not by name.


Another issue: if ORC schema has more fields than table schema, `java.lang.IndexOutOfBoundsException` is thrown.

```
RecordReaderFactory#getSchemaOnRead
structTypeInfo.setAllStructFieldNames(Lists.newArrayList(columnNames.subList(0, numCols)));
```

Note:

* org.apache.hadoop.hive.ql.io.orc.OrcInputFormat.OrcRecordReader is irrelevant here.

