# Spark Logging

## Overview


## log4j 1.2

spark/pom.xml (as of 2.4)

```
<log4j.version>1.2.17</log4j.version>
```


## log4j2

* SPARK-6305. Add support for log4j 2.x to Spark.
* https://logging.apache.org/log4j/2.x/manual/migration.html
* https://logging.apache.org/log4j/2.x/manual/architecture.html

## FAQ

### guard statement and performance
* https://stackoverflow.com/questions/963492/in-log4j-does-checking-isdebugenabled-before-logging-improve-performance
* https://stackoverflow.com/questions/105852/conditional-logging-with-minimal-cyclomatic-complexity/105908#105908