# Cassandra Client

## cqlsh
### python版本问题

CentOS 6.6使用2.6.6，cqlsh需要2.7以上，使用virtualenv解决问题。

* https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4

3.7及以下版本，必须使用2.7.10及以下版本的python。

* https://issues.apache.org/jira/browse/CASSANDRA-11850. cannot use cql since upgrading python to 2.7.11+

### OperationTimedOut: errors={}, last_host=xxx

两种方法，经过试验，Cassandra 3.7上都有效。

* Modify the cqlshrc file:

```
vi ~/.cassandra/cqlshrc
[connection]
request_timeout = 60
```

timeout值有多个，在cqlsh.py定义了默认值，`~/.cassandra/cqlshrc`定义的值会覆盖默认值。

* 命令行参数

```
cqlsh --request-timeout 120 myhost
```

还有一种方法是直接把cqlsh.py里面的默认值改了，这个方法不灵活。

参考：

* http://stackoverflow.com/questions/35390883/cassandra-count-query-error-operationtimedout-errors-last-host-127-0-0
* http://stackoverflow.com/questions/29394382/operation-time-out-error-in-cqlsh-console-of-cassandra/29394935
* https://issues.apache.org/jira/browse/CASSANDRA-7516

### newline inside string

```
Failed to import 5000 rows: Error - newline inside string,  given up after 1 attempts
Exceeded maximum number of insert errors 1000
```

escape with '\\'


### field larger than field limit (131072)

```
Failed to import 5000 rows: Error - field larger than field limit (131072),  given up after 1 attempts
Exceeded maximum number of insert errors 1000 Avg. rate:   26140 rows/s
```

* http://stackoverflow.com/questions/24168235/cassandra-cqlsh-text-field-limit-on-copy-from-csv-field-larger-than-field-limit
* http://docs.datastax.com/en/cql/3.3/cql/cql_reference/cqlshUsingCqlshrc.html
* https://issues.apache.org/jira/browse/CASSANDRA-8675

### copy

```
copy tablex from xxx.csv
copy tablex from dirxxx/*
```

from后面的参数只能是一个，要么是具体的文件路径，要么是python glob expressions.

## Java Driver


### Overview

4 simple rules:

* Use one Cluster instance per (physical) cluster (per application lifetime)
* Use at most one Session per keyspace, or use a single Session and explicitely specify the keyspace in your queries
* If you execute a statement more than once, consider using a PreparedStatement
* You can reduce the number of network roundtrips and also have atomic operations by using Batches

* https://datastax.github.io/java-driver/manual/
* http://www.datastax.com/dev/blog/4-simple-rules-when-using-the-datastax-drivers-for-cassandra

### Prepared statements

http://docs.datastax.com/en/developer/java-driver/3.1/manual/statements/prepared/

* Prepared statements
* Preparing on multiple nodes (It is enabled by default. see javadoc for details)
* Avoid preparing ‘SELECT *’ queries

### connection pooling

* http://docs.datastax.com/en/developer/java-driver/3.1/manual/pooling/
* https://github.com/datastax/java-driver/blob/3.1.0/driver-core/src/main/java/com/datastax/driver/core/PoolingOptions.java
* https://groups.google.com/a/lists.datastax.com/forum/#!topic/java-driver-user/-VnYQIPgorw

