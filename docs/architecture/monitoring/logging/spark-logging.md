# Spark Logging

## Overview


## Design and Implementation

spark/pom.xml (as of 2.4)

```
<log4j.version>1.2.17</log4j.version>
```

`Logging` is initialized in 2 ways:

1. non-interpreter
    * `Logging.initializeLogIfNecessary(false)`
2. interpreter
    * `org.apache.spark.repl.Main.initializeLogIfNecessary(true)`
    * `org.apache.spark.api.python.PythonGatewayServer.initializeLogIfNecessary(true)`
    * `org.apache.spark.api.r.RBackend.initializeLogIfNecessary(true)`

## Evolution

### Persist Driver Logs in Client mode to HDFS
[SPARK-25118](https://issues.apache.org/jira/browse/SPARK-25118)

### log4j2

* [SPARK-6305](https://issues.apache.org/jira/browse/SPARK-6305). Add support for log4j 2.x to Spark.
* https://logging.apache.org/log4j/2.x/manual/migration.html
* https://logging.apache.org/log4j/2.x/manual/architecture.html

## FAQ

### guard statement and performance
* https://stackoverflow.com/questions/963492/in-log4j-does-checking-isdebugenabled-before-logging-improve-performance
* https://stackoverflow.com/questions/105852/conditional-logging-with-minimal-cyclomatic-complexity/105908#105908