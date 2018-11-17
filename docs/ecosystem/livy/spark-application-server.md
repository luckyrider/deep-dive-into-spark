# Spark Application Server

## Overview
* Spark thrift server (STS)
* Apache Zeppelin (153 contributors, 2.0 supported)
* spark jobserver (ooyala, 82 contributors, 2.0 not supported yet, SJS)
* Livy REST server (cloudera hue, 13 contributors)
* Apache Toree (IBM, 22 contributors)

* http://www.slideshare.net/differentsachin/interactive-analytics-using-apache-spark
* http://www.bluedata.com/blog/2016/06/apache-spark-with-jupyter-spark-job-server/
* https://www.qubole.com/blog/product/share-rdds-across-jobs-with-quboles-spark-job-server/

## Spark Thrift Server (STS)

From Spark 1.6, by default the Thrift server runs in multi-session mode. Which means each JDBC/ODBC connection owns a copy of their own SQL configuration and temporary function registry. Cached tables are still shared though. If you prefer to run the Thrift server in the old single-session mode, please set option spark.sql.hive.thriftServer.singleSession to true. You may either add this option to spark-defaults.conf, or pass it to start-thriftserver.sh via --conf:

see more at: http://spark.apache.org/docs/latest/sql-programming-guide.html#upgrading-from-spark-sql-15-to-16

