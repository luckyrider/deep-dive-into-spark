# SparkConf

## Overview



## Troubleshooting

### classpath
SPARK_CLASSPATH was deprecated. see more at org.apache.spark.SparkConf.

```
sys.env.get("SPARK_CLASSPATH").foreach { value =>
  val warning =
    s"""
      |SPARK_CLASSPATH was detected (set to '$value').
      |This is deprecated in Spark 1.0+.
      |
      |Please instead use:
      | - ./spark-submit with --driver-class-path to augment the driver classpath
      | - spark.executor.extraClassPath to augment the executor classpath
    """.stripMargin
  logWarning(warning)
```

```
org.apache.spark.launcher
  AbstractCommandBuilder
    SparkClassCommandBuilder
    SparkSubmitCommandBuilder
```

AbstractCommandBuilder#buildClassPath:

```
getenv("SPARK_CLASSPATH") <- 
appClassPath              <- 
getConfDir()              <- 
getenv("SPARK_PREPEND_CLASSES")
addToClassPath(cp, getenv("HADOOP_CONF_DIR"));
addToClassPath(cp, getenv("YARN_CONF_DIR"));
addToClassPath(cp, getenv("SPARK_DIST_CLASSPATH"));
```

SPARK_DIST_CLASSPATH的使用，见Using Spark's "Hadoop Free" Build. https://spark.apache.org/docs/latest/hadoop-provided.html

## References
* http://spark.apache.org/docs/latest/configuration.html