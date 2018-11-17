# Spark Performance Test

## Overview
HiBench features many benchmarks within it that exercise several components of Spark (great for stressing core, sql, MLlib capabilities), SparkSqlPerf features 99 TPC-DS queries (stressing the DataFrame API and therefore the Catalyst optimiser), both work well with Spark 2 

* HiBench: https://github.com/intel-hadoop/HiBench
* SparkSqlPerf: https://github.com/databricks/spark-sql-perf

micro benchmark:

* https://github.com/apache/spark/tree/master/sql/core/src/test/scala/org/apache/spark/sql/execution/benchmark
