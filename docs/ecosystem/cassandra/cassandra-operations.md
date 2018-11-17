# Operations

## Overview


## nodetool

```
nodetool stopdaemon
nodetool status
nodetool gettimeout read
nodetool gettimeout range
```


## Add or remove nodes

### Add

* `bin/cassandra`
* Use `nodetool status` to verify that the node is fully bootstrapped and all other nodes are up (UN) and not in any other state.
* After all new nodes are running, run `nodetool cleanup` on each of the previously existing nodes to remove the keys that no longer belong to those nodes.

note:

* add node只能一个一个来，不能同时启动多个，否则报错：

```
ERROR [main] 2016-11-25 19:27:38,745 CassandraDaemon.java:731 - Exception encountered during startup
java.lang.UnsupportedOperationException: Other bootstrapping/leaving/moving nodes detected, cannot bootstrap while cassandra.consistent.rangemovement is true
        at org.apache.cassandra.service.StorageService.checkForEndpointCollision(StorageService.java:584) ~[apache-cassandra-3.7.jar:3.7]
        at org.apache.cassandra.service.StorageService.prepareToJoin(StorageService.java:855) ~[apache-cassandra-3.7.jar:3.7]
        at org.apache.cassandra.service.StorageService.initServer(StorageService.java:725) ~[apache-cassandra-3.7.jar:3.7]
        at org.apache.cassandra.service.StorageService.initServer(StorageService.java:625) ~[apache-cassandra-3.7.jar:3.7]
        at org.apache.cassandra.service.CassandraDaemon.setup(CassandraDaemon.java:370) [apache-cassandra-3.7.jar:3.7]
        at org.apache.cassandra.service.CassandraDaemon.activate(CassandraDaemon.java:585) [apache-cassandra-3.7.jar:3.7]
        at org.apache.cassandra.service.CassandraDaemon.main(CassandraDaemon.java:714) [apache-cassandra-3.7.jar:3.7]
```

* `nodetool cleanup`。Cleanup doesn't involve any other nodes so it is safe to run in parallel.

### remove

* use `nodetool status` to check node status,
* then
  * If the node is up, run `nodetool decommission`.
  * If the node is down, and If the cluster uses vnodes, remove the node using the `nodetool removenode` command.

decommission log:

```
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:38:59,468 StorageService.java:1411 - LEAVING: sleeping 30000 ms for batch processing and pending range setup
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:39:29,921 StorageService.java:1411 - LEAVING: replaying batch log and streaming data to other nodes
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:39:30,528 StreamResultFuture.java:90 - [Stream #0d709260-b5dd-11e6-b4c6-19dde366343a] Executing streaming plan for Unbootstrap
INFO  [StreamConnectionEstablisher:19] 2016-11-29 10:39:30,529 StreamSession.java:238 - [Stream #0d709260-b5dd-11e6-b4c6-19dde366343a] Starting streaming to /x.x.x.x
INFO  [StreamConnectionEstablisher:20] 2016-11-29 10:39:30,529 StreamSession.java:238 - [Stream #0d709260-b5dd-11e6-b4c6-19dde366343a] Starting streaming to /x.x.x.x
...
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:39:30,529 StorageService.java:1411 - LEAVING: streaming hints to other nodes
...
INFO  [HintsDispatcher:1494] 2016-11-29 10:39:30,540 HintsDispatchExecutor.java:140 - Transferring all hints to a5ef42e7-2507-40b1-b07b-3c3f6a4bc11d
INFO  [IndexSummaryManager:1] 2016-11-29 10:40:27,484 IndexSummaryRedistribution.java:75 - Redistributing index summaries
INFO  [STREAM-IN-/x.x.x.x:7000] 2016-11-29 10:49:30,100 StreamResultFuture.java:187 - [Stream #0d709260-b5dd-11e6-b4c6-19dde366343a] Session with /x.x.x.x is complete
...
INFO  [STREAM-IN-/x.x.x.x:7000] 2016-11-29 10:51:54,561 StreamResultFuture.java:219 - [Stream #0d709260-b5dd-11e6-b4c6-19dde366343a] All sessions completed
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:51:54,591 StorageService.java:2404 - Removing tokens [] for x.x.x.x
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:51:54,610 StorageService.java:3788 - Announcing that I have left the ring for 30000ms
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:52:24,610 ThriftServer.java:142 - Stop listening to thrift clients
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:52:24,625 Server.java:182 - Stop listening for CQL clients
WARN  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:52:24,625 Gossiper.java:1508 - No local state or state is in silent shutdown, not announcing shutdown
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:52:24,625 MessagingService.java:786 - Waiting for messaging service to quiesce
INFO  [ACCEPT-/x.x.x.x] 2016-11-29 10:52:24,626 MessagingService.java:1133 - MessagingService has terminated the accept() thread
INFO  [RMI TCP Connection(26057)-127.0.0.1] 2016-11-29 10:52:24,644 StorageService.java:1411 - DECOMMISSIONED
```

References:

* https://docs.datastax.com/en/cassandra/3.x/cassandra/operations/opsAddingRemovingNodeTOC.html
* https://docs.datastax.com/en/cassandra/3.x/cassandra/operations/opsAddNodeToCluster.html
* http://www.datastax.com/dev/blog/virtual-nodes-in-cassandra-1-2
* https://docs.datastax.com/en/cassandra/3.x/cassandra/operations/opsRemoveNode.html
* https://docs.datastax.com/en/cassandra/3.x/cassandra/architecture/archDataDistributeVnodesUsing.html
* https://docs.datastax.com/en/cassandra/3.x/cassandra/architecture/archDataDistributeDistribute.html

## Troubleshooting
### can not use jps

* https://issues.apache.org/jira/browse/CASSANDRA-9242
* https://issues.apache.org/jira/browse/CASSANDRA-9483
* https://support.datastax.com/hc/en-us/articles/208269876-Java-utilities-such-as-jps-or-jstat-unable-to-monitor-DSE-processes

### node start error
```
INFO  09:36:18 Starting Messaging Service on /192.168.1.11:7000 (eth1)
Exception (java.lang.RuntimeException) encountered during startup: Unable to gossip with any seeds
java.lang.RuntimeException: Unable to gossip with any seeds
	at org.apache.cassandra.gms.Gossiper.doShadowRound(Gossiper.java:1386)
	at org.apache.cassandra.service.StorageService.checkForEndpointCollision(StorageService.java:561)
	at org.apache.cassandra.service.StorageService.prepareToJoin(StorageService.java:855)
	at org.apache.cassandra.service.StorageService.initServer(StorageService.java:725)
	at org.apache.cassandra.service.StorageService.initServer(StorageService.java:625)
	at org.apache.cassandra.service.CassandraDaemon.setup(CassandraDaemon.java:370)
	at org.apache.cassandra.service.CassandraDaemon.activate(CassandraDaemon.java:585)
	at org.apache.cassandra.service.CassandraDaemon.main(CassandraDaemon.java:714)
ERROR 09:36:49 Exception encountered during startup
java.lang.RuntimeException: Unable to gossip with any seeds
	at org.apache.cassandra.gms.Gossiper.doShadowRound(Gossiper.java:1386) ~[apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.StorageService.checkForEndpointCollision(StorageService.java:561) ~[apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.StorageService.prepareToJoin(StorageService.java:855) ~[apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.StorageService.initServer(StorageService.java:725) ~[apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.StorageService.initServer(StorageService.java:625) ~[apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.CassandraDaemon.setup(CassandraDaemon.java:370) [apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.CassandraDaemon.activate(CassandraDaemon.java:585) [apache-cassandra-3.7.jar:3.7]
	at org.apache.cassandra.service.CassandraDaemon.main(CassandraDaemon.java:714) [apache-cassandra-3.7.jar:3.7]
```

解决办法是：cassandra.yaml正确设置seeds

```
seed_provider:
    # Addresses of hosts that are deemed contact points.
    # Cassandra nodes use this list of hosts to find each other and learn
    # the topology of the ring.  You must change this if you are running
    # multiple nodes!
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "xxx,xxx"
```

### opscenter
6.0开始支持cassandra 3.x。但是从6.0开始不支持apache版本的cassandra了。只好弃用opscenter。

see more at:

* http://docs.datastax.com/en/landing_page/doc/landing_page/compatibility.html#compatibilityDocument__opsc-compatibility
* http://docs.datastax.com/en/opscenter/6.0/opsc/opscPolicyChanges.html


```
curl --user dsa_email_address:password -L http://downloads.datastax.com/enterprise/opscenter.tar.gz | tar xz
```

### Adding a node failed
* `nodetool bootstrap resume` does not work.
* `drop materialized view` resolved the problem.

hardware issues:

* http://stackoverflow.com/questions/27583311/cassandra-adding-a-node-is-taking-too-long

big sstable issues:

* http://stackoverflow.com/questions/36719592/cant-add-a-new-cassandra-datacenter-due-to-streaming-errors
* https://issues.apache.org/jira/browse/CASSANDRA-11345

MV issues:

* https://www.mail-archive.com/user@cassandra.apache.org/msg50194.html
* https://issues.apache.org/jira/browse/CASSANDRA-12905

### startup message
?

```
CompilerOracle: dontinline org/apache/cassandra/db/Columns$Serializer.deserializeLargeSubset (Lorg/apache/cassandra/io/util/DataInputPlus;Lorg/apache/cassandra/db/Columns;I)Lorg/apache/cassandra/db/Columns;
CompilerOracle: dontinline org/apache/cassandra/db/Columns$Serializer.serializeLargeSubset (Ljava/util/Collection;ILorg/apache/cassandra/db/Columns;ILorg/apache/cassandra/io/util/DataOutputPlus;)V
CompilerOracle: dontinline org/apache/cassandra/db/Columns$Serializer.serializeLargeSubsetSize (Ljava/util/Collection;ILorg/apache/cassandra/db/Columns;I)I
CompilerOracle: dontinline org/apache/cassandra/db/transform/BaseIterator.tryGetMoreContents ()Z
CompilerOracle: dontinline org/apache/cassandra/db/transform/StoppingTransformation.stop ()V
CompilerOracle: dontinline org/apache/cassandra/db/transform/StoppingTransformation.stopInPartition ()V
CompilerOracle: dontinline org/apache/cassandra/io/util/BufferedDataOutputStreamPlus.doFlush (I)V
CompilerOracle: dontinline org/apache/cassandra/io/util/BufferedDataOutputStreamPlus.writeExcessSlow ()V
CompilerOracle: dontinline org/apache/cassandra/io/util/BufferedDataOutputStreamPlus.writeSlow (JI)V
CompilerOracle: dontinline org/apache/cassandra/io/util/RebufferingInputStream.readPrimitiveSlowly (I)J
CompilerOracle: inline org/apache/cassandra/io/util/Memory.checkBounds (JJ)V
CompilerOracle: inline org/apache/cassandra/io/util/SafeMemory.checkBounds (JJ)V
CompilerOracle: inline org/apache/cassandra/utils/AsymmetricOrdering.selectBoundary (Lorg/apache/cassandra/utils/AsymmetricOrdering/Op;II)I
CompilerOracle: inline org/apache/cassandra/utils/AsymmetricOrdering.strictnessOfLessThan (Lorg/apache/cassandra/utils/AsymmetricOrdering/Op;)I
CompilerOracle: inline org/apache/cassandra/utils/ByteBufferUtil.compare (Ljava/nio/ByteBuffer;[B)I
CompilerOracle: inline org/apache/cassandra/utils/ByteBufferUtil.compare ([BLjava/nio/ByteBuffer;)I
CompilerOracle: inline org/apache/cassandra/utils/ByteBufferUtil.compareUnsigned (Ljava/nio/ByteBuffer;Ljava/nio/ByteBuffer;)I
CompilerOracle: inline org/apache/cassandra/utils/FastByteOperations$UnsafeOperations.compareTo (Ljava/lang/Object;JILjava/lang/Object;JI)I
CompilerOracle: inline org/apache/cassandra/utils/FastByteOperations$UnsafeOperations.compareTo (Ljava/lang/Object;JILjava/nio/ByteBuffer;)I
CompilerOracle: inline org/apache/cassandra/utils/FastByteOperations$UnsafeOperations.compareTo (Ljava/nio/ByteBuffer;Ljava/nio/ByteBuffer;)I
CompilerOracle: inline org/apache/cassandra/utils/vint/VIntCoding.encodeVInt (JI)[B
```

### Maximum memory usage reached
?

```
INFO  [CompactionExecutor:14178] 2016-11-29 01:55:25,662 NoSpamLogger.java:91 - Maximum memory usage reached (512.000MiB), cannot allocate chunk of 1.000MiB
```

### add node message
?

```
ERROR [main] 2016-11-29 01:06:10,524 MigrationManager.java:164 - Migration task failed to complete
```

## Monitoring
JMX + Zabbix

* http://stackoverflow.com/questions/36323659/cassandra-cluster-monitoring
* https://github.com/tcpcloud/Zabbix-Template-CassandraDB
* https://github.com/yubu/zabbix-cassandra-template

jmx http bridge:

* https://www.pythian.com/blog/two-easy-ways-poll-apache-cassandra-metrics-using-jmx-http-bridge/
* http://stackoverflow.com/questions/35318593/jolokia-agent-for-cassandra
