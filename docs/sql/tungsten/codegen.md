# Whole Stage Codegen

## Overview


## design

https://jaceklaskowski.gitbooks.io/mastering-spark-sql/spark-sql-whole-stage-codegen.html

## Implementation
Decouple the generated codes of consuming rows in operators under whole-stage codegen
https://issues.apache.org/jira/browse/SPARK-21717

"distribute by" on multiple columns may lead to codegen issue
https://issues.apache.org/jira/browse/SPARK-25084

## Configuration

* spark.sql.codegen.wholeStage true
* spark.sql.codegen.useIdInClassName true
* spark.sql.codegen.maxFields 100
* spark.sql.codegen.factoryMode (for test only)
* spark.sql.codegen.fallback true
* spark.sql.codegen.logging.maxLines 1000

e.g.

```
/* 1000 */             project_inTmpResult_19 = -1; // project_isNull_172 = true;
/* 1001 */             [truncated to 1000 lines (total lines is 31751)]
```

* spark.sql.codegen.hugeMethodLimit 65535
* spark.sql.codegen.splitConsumeFuncByOperator true
