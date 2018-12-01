# Spark Develop Tips

## Environment

```
yarn-daemon.sh start resourcemanager
yarn-daemon.sh start nodemanager
hive-start-metastore.sh
start-history-server.sh

hadoop-daemon.sh stop namenode
hadoop-daemon.sh stop datanode
yarn-daemon.sh stop resourcemanager
yarn-daemon.sh stop nodemanager
```

## Build
maven:

```
./build/mvn -DskipTests clean package
./build/mvn -pl :spark-assembly_2.11 clean package
build/mvn -T 1C -DskipTests -Phadoop-2.7 -Pyarn -Phive -Phive-thriftserver package
build/mvn -T 1C -q -DskipTests -Phadoop-2.7 -Pyarn -Phive -Phive-thriftserver clean install
build/mvn -T 1C -o -q -Phadoop-2.7 -pl core verify
build/mvn -T 1C -o -q -Phadoop-2.7 -pl sql/catalyst verify
build/mvn -T 1C -o -q -Phadoop-2.7 -pl sql/core verify
build/mvn -T 1C -o -q -Phadoop-2.7 -Phive -pl sql/hive verify
build/mvn -T 1C -o -q -Phadoop-2.7 -Phive-thriftserver -pl sql/hive-thriftserver verify
build/mvn -T 1C -o -q -Phadoop-2.7 -pl sql/hive -Dsuites=org.apache.spark.sql.hive.HiveExternalCatalogVersionsSuite verify
build/mvn -T 1C -Phadoop-2.7 -pl sql/core -am -Dsuites=org.apache.spark.sql.execution.PlannerSuite clean test

```

sbt:

```
./build/sbt -Pyarn -Phadoop-2.7 -Phive -Phive-thriftserver -DskipTests clean compile package
./build/sbt -Pyarn -Phadoop-2.7 -Phive -Phive-thriftserver -DskipTests
```

make distribution:

```
./dev/make-distribution.sh --name custom-spark --pip --r --tgz -Psparkr -Phadoop-2.7 -Phive -Phive-thriftserver -Pmesos -Pyarn -Pkubernetes
./dev/make-distribution.sh --name custom-spark -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn
./dev/make-distribution.sh --name custom-spark --tgz -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn
./dev/make-distribution.sh --name spark-zeta --tgz -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn
./dev/make-distribution.sh --name SPARK-25132 --tgz  -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn -Phadoop-provided
```

## UT
### UT Infrastructure
ScalaTest

### Commands
Run specific test suites

```
build/sbt "sql/test-only *.ParquetSchemaSuite *.ParquetFileFormatSuite *.FileBasedDataSourceSuite *.ParquetQuerySuite *.OrcQuerySuite *.SQLQuerySuite"
build/sbt "hive/test-only *.ParquetSourceSuite *.ParquetMetastoreSuite *.HiveOrcQuerySuite *.HiveQuerySuite"
```

Run all test suites of a module

```
build/sbt "catalyst/test-only"
build/sbt "sql/test-only"
build/sbt "hive/test-only"
```

### logs
```
========================================================================
Running Spark unit tests
========================================================================
[info] Running Spark tests using SBT with these arguments:  -Phadoop-2.6 -Phive-thriftserver -Phive -Dtest.exclude.tags=org.apache.spark.tags.ExtendedHiveTest,org.apache.spark.tags.ExtendedYarnTest hive-thriftserver/test avro/test mllib/test hive/test repl/test examples/test sql/test sql-kafka-0-10/test

[success] Total time: 31 s, completed Aug 20, 2018 6:25:05 AM
```

```
========================================================================
Running PySpark tests
========================================================================
Running PySpark tests. Output is in /home/jenkins/workspace/SparkPullRequestBuilder/python/unit-tests.log
Will test against the following Python executables: ['python2.7', 'python3.4', 'pypy']
Will test the following Python modules: ['pyspark-sql', 'pyspark-mllib', 'pyspark-ml']
```