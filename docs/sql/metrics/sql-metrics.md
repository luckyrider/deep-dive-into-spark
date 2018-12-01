# SQL Metrics

## Overview


## Design and Implementation
![SQL metrics](sql-metrics.png)

`SQLMetric` is kind of `AccumulatorV2`, which holds `AccumulatorMetadata` including `id`, `name` and
etc. `SQLMetrics` is the static factory to create `SQLMetric`. It deals with details of size and
timing metrics, e.g. total, min, median, max.

Physical operators (`SparkPlan`) hold metrics of type `SQLMetric`. Different operators have
different collection of metrics. Some operators even have no metrics at all, e.g. `ProjectExec`.

When `SparkPlan` is mapped to `SparkPlanInfo`, which is further mapped to
`SparkPlanGraph` for Web Display, `SQLMetric` is mapped to `SQLMetricInfo`, which holds accumulator
id.

## Evolving

* [SPARK-26221 Improve Spark SQL instrumentation and metrics](https://issues.apache.org/jira/browse/SPARK-26221)

## Coding

* SQLMetricsSuite
* SQLListenerSuite
