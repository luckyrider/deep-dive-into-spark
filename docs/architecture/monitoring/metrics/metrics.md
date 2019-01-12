# SQL Metrics

## Overview


## Design and Implementation

### Metrics System
![metrics system](metrics-system.png)

### Core Metrics

Task Metrics



### SQL Metrics
SQL metrics classes relationship:

![SQL metrics](sql-metrics.png)

`SQLMetric` is a metric used in a SQL query plan. This is implemented as an `AccumulatorV2`. Updates
on the executor side are automatically propagated and shown in the SQL UI through metrics. Updates
on the driver side must be explicitly posted using `SQLMetrics.postDriverMetricUpdates()`.

`SQLMetric` is kind of `AccumulatorV2`, which holds `AccumulatorMetadata` including `id`, `name` and
etc. `SQLMetrics` is the static factory to create `SQLMetric`. It deals with details of size and
timing metrics, e.g. total, min, median, max.

Physical operators (`SparkPlan`) hold metrics of type `SQLMetric`. Different operators have
different collection of metrics. Some operators even have no metrics at all, e.g. `ProjectExec`.
Physical operator metrics are updated during its execution within `doExecute` method.

When `SparkPlan` is mapped to `SparkPlanInfo`, which is further mapped to `SparkPlanGraph`,
`SQLMetric` is mapped to `SQLMetricInfo`, which holds accumulator id.

## Evolution
General

* [SPARK-8856 Better instrumentation and visualization for physical plan (Spark 1.5)](https://issues.apache.org/jira/browse/SPARK-8856)
* [SPARK-26221 Improve Spark SQL instrumentation and metrics](https://issues.apache.org/jira/browse/SPARK-26221)

Memory

* [SPARK-9103 Tracking spark's memory usage](https://issues.apache.org/jira/browse/SPARK-9103)
* [SPARK-23206 Additional Memory Tuning Metrics](https://issues.apache.org/jira/browse/SPARK-23206)


CPU

* [SPARK-12221 Add CPU time metric to TaskMetrics](https://issues.apache.org/jira/browse/SPARK-12221)
* [SPARK-25228 Add executor CPU Time metric](https://issues.apache.org/jira/browse/SPARK-25228)

## Misc

* SQLMetricsSuite
* SQLListenerSuite

## 3rd Party Libs

### Dropwizard Metrics

![dropwizard metrics](dropwizard-metrics.png)

`Metric` types:

* `Counter`: An incrementing and decrementing counter metric.
* `Gauge`: A gauge metric is an instantaneous reading of a particular value.
* `Metered`: An object which maintains mean and exponentially-weighted rate.
* `Histogram`: A metric which calculates the distribution of a value.
* `MetricSet`: A set of named metrics.

* https://github.com/dropwizard/metrics

