# CBO

## Overview




## Statistics Collection Framework

### SQL Command

ANALYZE TABLE [db_name.]table_name COMPUTE STATISTICS [analyze_option];
ANALYZE TABLE [db_name.]table_name COMPUTE STATISTICS FOR COLUMNS col1 [, col2, ...];
DESCRIBE [EXTENDED] [db_name.]table_name column_name;

### Implementation

org.apache.spark.sql.catalyst.plans.logical
* Statistics
* ColumnStat
* Histogram
* HistogramBin

org.apache.spark.sql.execution.command
* AnalyzeTableCommand
* AnalyzePartitionCommand
* AnalyzeTableCommand


## Configuration

Property Default Description
* spark.sql.statistics.ndv.maxError	0.05	The maximum estimation error allowed in HyperLogLog++ algorithm when generating column level statistics.
* spark.sql.statistics.histogram.enabled	false	Generates histograms when computing column statistics if enabled. Histograms can provide better estimation accuracy. Currently, Spark only supports equi-height histogram. Note that collecting histograms takes extra cost. For example, collecting column statistics usually takes only one table scan, but generating equi-height histogram will cause an extra table scan.
* spark.sql.statistics.histogram.numBins	254	The number of bins when generating histograms.
* spark.sql.statistics.percentile.accuracy	10000	Accuracy of percentile approximation when generating equi-height histograms. Larger value means better accuracy. The relative error can be deduced by 1.0 / PERCENTILE_ACCURACY.
* spark.sql.statistics.size.autoUpdate.enabled	false	Enables automatic update for table size once table's data is changed. Note that if the total number of files of the table is very large, this can be expensive and slow down data change commands.
* spark.sql.cbo.enabled	false	Enables CBO for estimation of plan statistics when set true.
* spark.sql.cbo.joinReorder.enabled	false	Enables join reorder in CBO.
* spark.sql.cbo.joinReorder.dp.threshold	12	The maximum number of joined nodes allowed in the dynamic programming algorithm.
* spark.sql.cbo.joinReorder.card.weight	0.7	The weight of cardinality (number of rows) for plan cost comparison in join reorder: rows * weight + size * (1 - weight).
* spark.sql.cbo.joinReorder.dp.star.filter	false	Applies star-join filter heuristics to cost based join enumeration.
* spark.sql.cbo.starSchemaDetection	false	When true, it enables join reordering based on star schema detection.
* spark.sql.cbo.starJoinFTRatio	0.9	Specifies the upper limit of the ratio between the largest fact tables for a star join to be considered.


## Case Study

```
ANALYZE TABLE tpcds.store_sales COMPUTE STATISTICS NOSCAN;

DESCRIBE TABLE EXTENDED tpcds.store_sales;

Statistics	146440897 bytes
```

```
ANALYZE TABLE tpcds.store_sales COMPUTE STATISTICS;

DESCRIBE TABLE EXTENDED tpcds.store_sales;

Statistics	146440897 bytes, 2880404 rows
```

```
ANALYZE TABLE tpcds.store_sales COMPUTE STATISTICS FOR COLUMNS ss_item_sk;

DESCRIBE EXTENDED tpcds.store_sales ss_item_sk;

col_name	ss_item_sk
data_type	int
comment	NULL
min	1
max	18000
num_nulls	0
distinct_count	16971
avg_col_len	4
max_col_len	4
histogram	NULL
```

```
DESCRIBE EXTENDED tpcds.store_sales ss_item_sk;
col_name	ss_item_sk
data_type	int
comment	NULL
min	1
max	18000
num_nulls	0
distinct_count	16971
avg_col_len	4
max_col_len	4
histogram	height: 11340.173228346457, num_of_bins: 254
bin_0	lower_bound: 1.0, upper_bound: 70.0, distinct_count: 70
bin_1	lower_bound: 70.0, upper_bound: 143.0, distinct_count: 76
bin_2	lower_bound: 143.0, upper_bound: 213.0, distinct_count: 72
…
bin_251	lower_bound: 17791.0, upper_bound: 17860.0, distinct_count: 68
bin_252	lower_bound: 17860.0, upper_bound: 17931.0, distinct_count: 75
bin_253	lower_bound: 17931.0, upper_bound: 18000.0, distinct_count: 70
```

## References
1. [SPARK-16026] Cost-based Optimizer Framework
2. https://issues.apache.org/jira/secure/attachment/12823839/Spark_CBO_Design_Spec.pdf
3. https://databricks.com/blog/2017/08/31/cost-based-optimizer-in-apache-spark-2-2.html
4. Cost-Based Optimizer Framework for Spark SQL. Spark Summit East 2017. https://databricks.com/session/cost-based-optimizer-framework-for-spark-sql
5. Cost Based Optimizer in Apache Spark 2.2. Spark Summit 2017. 
6. [SPARK-21975] Histogram support in cost-based optimizer. Since 2.3.0
7. https://docs.databricks.com/spark/latest/spark-sql/cbo.html
8. https://docs.databricks.com/spark/latest/spark-sql/language-manual/analyze-table.html
9. https://jaceklaskowski.gitbooks.io/mastering-spark-sql/spark-sql-cost-based-optimization.html
10. Dynamic programming. https://en.wikipedia.org/wiki/Dynamic_programming
11. Selinger et al. Access path selection in a relational database management system. In SIGMOD 1979.
