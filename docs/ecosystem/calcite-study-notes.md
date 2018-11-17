# Calcite Study Notes

## Overview


## Fundamentals

## Elasticsearch Adaptoer

### Create Elasticsearch adapter for Calcite
https://issues.apache.org/jira/browse/CALCITE-1253

Resolved in release 1.8.0 (2016-06-13).

Can you briefly list what should be the next work? What are the bugs, missing features? They don't need to be fixed now, but I would like to know where the holes are.
* Enhance tests with foodmart dataset.
* Support aggregation operations. 

### Add support for aggregates in Calcite Elasticsearch adapter
https://issues.apache.org/jira/browse/CALCITE-1261


## 常见问题
### table not found
http://stackoverflow.com/questions/31118348/table-not-found-with-apache-calcite

The problem is case-sensitivity. Because you did not enclose the table name in double-quotes, Calcite's SQL parser converted it to upper case.