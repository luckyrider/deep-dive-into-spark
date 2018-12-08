# Spark Thrift Server
## Overview

* https://jaceklaskowski.gitbooks.io/mastering-spark-sql/spark-sql-thrift-server.html

## Design and Implementation
### HTTP
Thrift JDBC server also supports sending thrift RPC messages over HTTP transport. Use the following setting to enable HTTP mode as system property or in hive-site.xml file in conf/:

```
hive.server2.transport.mode - Set this to value: http
hive.server2.thrift.http.port - HTTP port number to listen on; default is 10001
hive.server2.http.endpoint - HTTP endpoint; default is cliservice
```

* http://spark.apache.org/docs/latest/sql-programming-guide.html#running-the-thrift-jdbcodbc-server

### JDBC/ODBC
Using the Spark Thrift server, you can remotely access Spark SQL over JDBC (using the JDBC Beeline client) or ODBC (using the Simba driver).

* https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.5/bk_spark-component-guide/content/jdbc-odbc-access-sparksql.html

### User Impersonation

* https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.5/bk_spark-component-guide/content/config-sts-user-imp.html

## Misc

* http://www.russellspitzer.com/2017/05/19/Spark-Sql-Thriftserver/
* https://developer.ibm.com/hadoop/2016/08/22/how-to-run-queries-on-spark-sql-using-jdbc-via-thrift-server/