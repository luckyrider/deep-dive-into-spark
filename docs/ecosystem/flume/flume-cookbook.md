# Flume Cookbook

## Overview
Apache Flume is a distributed, reliable, and available system for efficiently collecting, aggregating and moving large amounts of log data from many different sources to a centralized data store. The use of Apache Flume is not only restricted to log data aggregation. Since data sources are customizable, Flume can be used to transport massive quantities of event data including but not limited to network traffic data, social-media-generated data, email messages and pretty much any data source possible.

References:

* http://archive.cloudera.com/cdh5/cdh/5/flume-ng/FlumeUserGuide.html
* http://flume.apache.org/FlumeUserGuide.html

## Architecture
### Data flow model
A Flume event is defined as a unit of data flow having a byte payload and an optional set of string attributes. A Flume agent is a (JVM) process that hosts the components through which events flow from an external source to the next destination (hop).

Agent = source + channel + sink

### Components
In order from source to sink:

* Source
* Interceptor for Source
* Channel Selector
* Channel
* Sink Processor
* Sink Group
* Sink
* Event Serializer

A source instance can specify multiple channels, but a sink instance can only specify one channel. (I guess, this is related to transaction semantics. If a single sink has more than one channels, distributed transaction should be required, which brings overkilling complexicy.)

```
<Agent>.sources.<Source>.channels = <Channel1> <Channel2> ...
<Agent>.sinks.<Sink>.channel = <Channel1>
```

### Network Streams
Flume supports the following mechanisms to read data from popular log stream types, such as:

* Avro
* Thrift
* Syslog
* Netcat

### Topology Design Considerations
If you need to ingest textual log data into Hadoop/HDFS then Flume is the right fit for your problem, full stop. The key property of an event is that they are generated in a continuous, streaming fashion. If your data is not regularly generated (i.e. you are trying to do a single bulk load of data into a Hadoop cluster) then Flume will still work, but it is probably overkill for your situation. 

Flume likes relatively stable topologies.

In general, disk-based channels should get 10’s of MB/s and memory based channels should get 100’s of MB/s or more. Performance will vary widely, however depending on hardware and operating environment.

### Flume-OG vs Flume-NG
* http://www.ibm.com/developerworks/cn/data/library/bd-1404flumerevolution/index.html

## Configuration

### Defining the flow
```
# list the sources, sinks and channels for the agent
<Agent>.sources = <Source>
<Agent>.sinks = <Sink>
<Agent>.channels = <Channel1> <Channel2>

# set channel for source
<Agent>.sources.<Source>.channels = <Channel1> <Channel2> ...

# set channel for sink
<Agent>.sinks.<Sink>.channel = <Channel1>
```

### Configuring individual components
```
# properties for sources
<Agent>.sources.<Source>.<someProperty> = <someValue>

# properties for channels
<Agent>.channel.<Channel>.<someProperty> = <someValue>

# properties for sinks
<Agent>.sources.<Sink>.<someProperty> = <someValue>
```

## Up and Running

### 
Run the agent:

```
bin/flume-ng agent --conf ./conf/ -f conf/flume.conf -Dflume.root.logger=DEBUG,console -n agent1
```

Run the avro client:

```
bin/flume-ng avro-client --conf conf -H localhost -p 41414 -F /etc/passwd -Dflume.root.logger=DEBUG,console
```

Log events are output in your first window, where the server is running.

### Sending Data to HDFS
an agent named agent_foo is reading data from an external avro client and sending it to HDFS via a memory channel.

```
# list the sources, sinks and channels for the agent
agent_foo.sources = avro-appserver-src-1
agent_foo.sinks = hdfs-sink-1
agent_foo.channels = mem-channel-1

# set channel for source
agent_foo.sources.avro-appserver-src-1.channels = mem-channel-1

# set channel for sink
agent_foo.sinks.hdfs-sink-1.channel = mem-channel-1

# properties of avro-appserver-source
agent_foo.sources.avro-appserver-src-1.type = avro
agent_foo.sources.avro-appserver-src-1.bind = localhost
agent_foo.sources.avro-appserver-src-1.port = 10000

# properties of mem-channel-1
agent_foo.channels.mem-channel-1.type = memory
agent_foo.channels.mem-channel-1.capacity = 1000
agent_foo.channels.mem-channel-1.transactionCapacity = 100

# properties of hdfs-sink-1
agent_foo.sinks.hdfs-sink-1.type = hdfs
agent_foo.sinks.hdfs-sink-1.hdfs.path = hdfs://localhost:8020/flume/weblog
# fileType = SequenceFile (default), DataStream or CompressedStream
agent_foo.sinks.hdfs-sink-1.hdfs.fileType = DataStream
```

Run the agent:

```
bin/flume-ng agent --conf ./conf/ -f ./conf/weblog.conf -n agent_foo
```

Run the avro client:

```
bin/flume-ng avro-client --conf conf -H localhost -p 10000 -F /etc/passwd
```

Data is sent to HDFS as sequence files in /flume/weblog

## Cloudera Manager Deploy Flume
通过Cloudera Manager的add service增加Flume，并且通过Cloudera Manager启动service，会生成Flume进程对应的目录，包括add service时指定的依赖组件的配置，如HDFS和HBase。
```
sudo ls /opt/cloudera-manager/cm-5.3.0/run/cloudera-scm-agent/process/41-flume-AGENT
cloudera-monitor.properties	   event-filter-rules.json  flume.keytab	  hbase-conf	    logs
cloudera-stack-monitor.properties  flume.conf		    grok-dictionary.conf  jaas.conf	    morphlines.conf
custom-mimetypes.xml		   flume-env.sh		    hadoop-conf		  log4j.properties
```
hadoop的配置示例如下：
```
sudo ls /opt/cloudera-manager/cm-5.3.0/run/cloudera-scm-agent/process/41-flume-AGENT/hadoop-conf
core-site.xml  hadoop-env.sh  hdfs-site.xml  log4j.properties  ssl-client.xml  topology.map  topology.py
```

查看Flume对应的进程，可以看到是以flume:flume用户运行的。
```
ps aux | grep flume
flume    29248  0.3  1.0 6153868 347848 ?      Sl   15:16   0:32 /usr/java/jdk1.8.0_11/bin/java
ps -eo user,pid,cmd | grep flume
flume    29248 /usr/java/jdk1.8.0_11/bin/java
```

脚本在：`/opt/cloudera-manager/cm-5.3.0/lib64/cmf/service/flume/flume.sh`

## Flume Kafka HDFS Integration
Prepare HDFS directories:
```
sudo -u hdfs hadoop fs -mkdir -p /user/flume/log
sudo -u hdfs hadoop fs -chown -R flume:flume /user/flume
```

Example flume.conf
```
# Business Activity
activity.sources  = kafka-source-1
activity.channels = file-channel-1
activity.sinks    = hdfs-sink-1

# source
activity.sources.kafka-source-1.type = org.apache.flume.source.kafka.KafkaSource
activity.sources.kafka-source-1.zookeeperConnect = <zookeeper host>:2181
activity.sources.kafka-source-1.topic = business-activity
activity.sources.kafka-source-1.batchSize = 100
activity.sources.kafka-source-1.channels = file-channel-1

activity.sources.kafka-source-1.interceptors = i1 i2
activity.sources.kafka-source-1.interceptors.i1.type = regex_extractor
activity.sources.kafka-source-1.interceptors.i1.regex = SYSTEM_ID:(\\d\\d)
activity.sources.kafka-source-1.interceptors.i1.serializers = s1
activity.sources.kafka-source-1.interceptors.i1.serializers.s1.name = system
activity.sources.kafka-source-1.interceptors.i2.type = regex_extractor
activity.sources.kafka-source-1.interceptors.i2.regex = TIMESTAMP:(\\d\\d\\d\\d-\\d\\d-\\d\\d)
activity.sources.kafka-source-1.interceptors.i2.serializers = s1
activity.sources.kafka-source-1.interceptors.i2.serializers.s1.type = org.apache.flume.interceptor.RegexExtractorInterceptorMillisSerializer
activity.sources.kafka-source-1.interceptors.i2.serializers.s1.name = timestamp
activity.sources.kafka-source-1.interceptors.i2.serializers.s1.pattern = yyyy-MM-dd

# channel
activity.channels.file-channel-1.type   = file
activity.channels.file-channel-1.checkpointDir = /data/flume-ng/activity-agent/channels/file-channel-1/checkpoint
activity.channels.file-channel-1.dataDirs = /data/flume-ng/activity-agent/channels/file-channel-1/data

# sink
activity.sinks.hdfs-sink-1.channel = file-channel-1
activity.sinks.hdfs-sink-1.type = hdfs
activity.sinks.hdfs-sink-1.hdfs.writeFormat = Text
activity.sinks.hdfs-sink-1.hdfs.fileType = DataStream
activity.sinks.hdfs-sink-1.hdfs.filePrefix = %{topic}
activity.sinks.hdfs-sink-1.hdfs.fileSuffix = .txt
activity.sinks.hdfs-sink-1.hdfs.path = /user/flume/log/%{topic}/%{system}/%Y-%m-%d
activity.sinks.hdfs-sink-1.hdfs.rollCount=10
activity.sinks.hdfs-sink-1.hdfs.rollSize=1024
activity.sinks.hdfs-sink-1.hdfs.rollInterval=30
 
# Other properties
activity.channels.file-channel-1.capacity = 10000
activity.channels.file-channel-1.transactionCapacity = 1000
```

Note:
* Value of Agent Name should match `[a-zA-Z0-9_]+`

exmaple message:
```
TIMESTAMP:2015-02-04 SYSTEM_ID:11 user 1 do something aaa
```

### Kafka Bug
Kafka source throws NPE if Kafka record has null key
* https://issues.apache.org/jira/browse/FLUME-2578

```
2015-02-04 18:56:54,019 ERROR org.apache.flume.source.kafka.KafkaSource: KafkaSource EXCEPTION, {}
java.lang.NullPointerException
	at java.lang.String.<init>(String.java:554)
	at org.apache.flume.source.kafka.KafkaSource.process(KafkaSource.java:105)
	at org.apache.flume.source.PollableSourceRunner$PollingRunner.run(PollableSourceRunner.java:139)
	at java.lang.Thread.run(Thread.java:745)
```

References:
* http://blog.cloudera.com/blog/2014/11/flafka-apache-flume-meets-apache-kafka-for-event-processing

## Trouble Shooting

### NoSuchMethodException on HDFS(local) Sink
```
(SinkRunner-PollingRunner-DefaultSinkProcessor) [WARN - org.apache.flume.sink.hdfs.BucketWriter.getRefIsClosed(BucketWriter.java:210)] isFileClosed is not available in the version of HDFS being used. Flume will not attempt to close files if the close fails on the first attempt
java.lang.NoSuchMethodException: org.apache.hadoop.fs.LocalFileSystem.isFileClosed(org.apache.hadoop.fs.Path)
	at java.lang.Class.getMethod(Class.java:1786)
	at org.apache.flume.sink.hdfs.BucketWriter.getRefIsClosed(BucketWriter.java:207)
	at org.apache.flume.sink.hdfs.BucketWriter.open(BucketWriter.java:295)
	at org.apache.flume.sink.hdfs.BucketWriter.append(BucketWriter.java:554)
	at org.apache.flume.sink.hdfs.HDFSEventSink.process(HDFSEventSink.java:426)
	at org.apache.flume.sink.DefaultSinkProcessor.process(DefaultSinkProcessor.java:68)
	at org.apache.flume.SinkRunner$PollingRunner.run(SinkRunner.java:147)
	at java.lang.Thread.run(Thread.java:745)
```

related issue:

* https://issues.apache.org/jira/browse/FLUME-2427

## References
* http://blog.cloudera.com/blog/2014/09/apache-kafka-for-beginners/
* https://cwiki.apache.org/confluence/display/FLUME/Getting+Started
