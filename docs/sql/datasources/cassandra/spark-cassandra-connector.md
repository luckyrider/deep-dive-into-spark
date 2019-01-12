# Spark Cassandra Connector Study Notes

## overview
* build from source
* spark shell

nice references

* https://academy.datastax.com/resources/how-spark-cassandra-connector-reads-data
* https://databricks.com/blog/2015/06/16/zen-and-the-art-of-spark-maintenance-with-cassandra.html

## Building

### build with sbt

```
sbt -Dscala-2.11=true package
```

### import into intellij idea
problems: `/Users/seanmao/Library/Logs/IdeaIC15/sbt.last.log`

```
[error] 1 not found
[error]   /Users/seanmao/.m2/repository/org/apache/httpcomponents/httpcore/4.2.4/httpcore-4.2.4.jar
[trace] Stack trace suppressed: run 'last cassandra-server/*:update' for the full output.
[error] (cassandra-server/*:update) java.lang.Exception: Encountered 1 errors (see above messages)
```

solution:

```
mvn dependency:get -DgroupId=org.apache.httpcomponents -DartifactId=httpcore -Dversion=4.2.4 -Dpackaging=jar
```

## spark shell

```
SPARK_MASTER_IP=localhost start-master.sh
start-slave.sh spark://localhost:7077
spark-shell --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 --conf spark.cassandra.connection.host=localhost

// resolve guava version issue, prepend guava 16.0.1 to driver and executor classpath
spark-shell --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 --conf spark.cassandra.connection.host=localhost --conf spark.executor.extraClassPath=/path/to/guava-16.0.1.jar --conf spark.driver.extraClassPath=/path/to/guava-16.0.1.jar
```

spark sql

```
spark-sql --packages datastax:spark-cassandra-connector:1.6.0-s_2.10 --conf spark.cassandra.connection.host=localhost --conf spark.executor.extraClassPath=/path/to/guava-16.0.1.jar --conf spark.driver.extraClassPath=/path/to/guava-16.0.1.jar
```

resolve dependencies

* 根据`--packages`，从ivy2解析并下载，共16个包。不但下载到ivy的cache中(`.ivy2/cache`)，还单独保存到`.ivy2/jars`方便使用。

```
Ivy Default Cache set to: /home/vagrant/.ivy2/cache
The jars for the packages stored in: /home/vagrant/.ivy2/jars
:: loading settings :: url = jar:file:/home/vagrant/dataplatform/spark-1.6.2-bin-hadoop2.6/lib/spark-assembly-1.6.2-hadoop2.6.0.jar!/org/apache/ivy/core/settings/ivysettings.xml
datastax#spark-cassandra-connector added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent;1.0
	confs: [default]
	found datastax#spark-cassandra-connector;1.6.0-s_2.10 in spark-packages
	found org.apache.cassandra#cassandra-clientutil;3.0.2 in central
	found com.datastax.cassandra#cassandra-driver-core;3.0.0 in central
	found io.netty#netty-handler;4.0.33.Final in central
	found io.netty#netty-buffer;4.0.33.Final in central
	found io.netty#netty-common;4.0.33.Final in central
	found io.netty#netty-transport;4.0.33.Final in central
	found io.netty#netty-codec;4.0.33.Final in central
	found io.dropwizard.metrics#metrics-core;3.1.2 in central
	found org.slf4j#slf4j-api;1.7.7 in central
	found org.apache.commons#commons-lang3;3.3.2 in central
	found com.google.guava#guava;16.0.1 in central
	found org.joda#joda-convert;1.2 in central
	found joda-time#joda-time;2.3 in central
	found com.twitter#jsr166e;1.1.0 in central
	found org.scala-lang#scala-reflect;2.10.5 in central
:: resolution report :: resolve 1240ms :: artifacts dl 42ms
	:: modules in use:
	com.datastax.cassandra#cassandra-driver-core;3.0.0 from central in [default]
	com.google.guava#guava;16.0.1 from central in [default]
	com.twitter#jsr166e;1.1.0 from central in [default]
	datastax#spark-cassandra-connector;1.6.0-s_2.10 from spark-packages in [default]
	io.dropwizard.metrics#metrics-core;3.1.2 from central in [default]
	io.netty#netty-buffer;4.0.33.Final from central in [default]
	io.netty#netty-codec;4.0.33.Final from central in [default]
	io.netty#netty-common;4.0.33.Final from central in [default]
	io.netty#netty-handler;4.0.33.Final from central in [default]
	io.netty#netty-transport;4.0.33.Final from central in [default]
	joda-time#joda-time;2.3 from central in [default]
	org.apache.cassandra#cassandra-clientutil;3.0.2 from central in [default]
	org.apache.commons#commons-lang3;3.3.2 from central in [default]
	org.joda#joda-convert;1.2 from central in [default]
	org.scala-lang#scala-reflect;2.10.5 from central in [default]
	org.slf4j#slf4j-api;1.7.7 from central in [default]
	---------------------------------------------------------------------
	|                  |            modules            ||   artifacts   |
	|       conf       | number| search|dwnlded|evicted|| number|dwnlded|
	---------------------------------------------------------------------
	|      default     |   16  |   0   |   0   |   0   ||   16  |   0   |
	---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent
	confs: [default]
	0 artifacts copied, 16 already retrieved (0kB/36ms)
```

## Dev with Sparkc

### column mapping

overview:

* https://github.com/datastax/spark-cassandra-connector/blob/master/doc/5_saving.md
* https://github.com/datastax/spark-cassandra-connector/blob/master/doc/6_advanced_mapper.md

about tuples: By default, Tuple fields will be paired in order with Cassandra Columns but using a custom mapper is also supported with tuples.

* Example Saving an RDD of Tuples with Default Mapping
* Example Saving an RDD of Tuples with Custom Mapping

about user-defined class: When saving a collection of objects of a user-defined class, the items to be saved must provide appropriately named public property accessors for getting every column to be saved.

* Example Saving an RDD of Scala Objects
* Example Saving an RDD of Scala Objects with Custom Mapping


