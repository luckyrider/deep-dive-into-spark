# Cassandra Performance

## Overview
### Tips
https://community.hortonworks.com/questions/31827/what-to-do-for-performance-tuning-of-cassandra-dat.html

Give commit log an SSD

The simplest thing that you can which will yield a high performance boost is to give your commit log a dedicated SSD. Since cassandra utilises the commit log heavily, switching the commitlog_directory setting in cassandra.yaml to a dedicated SSd away from where you store sstables (the data files) will give much better write performances.

Heap space

Cassandra has a script that automatically allocates memory to each node, the script is very good in most usecases, but if you have lots of other tech running on the same machine which is likely in HDP, you probably want to check how much memory is assgined to your cassandra node. For cassandra 2.2.x the recomendation is between 2-8GB, for Cassandra 3+ you can extend the heap to 16GB and boost performance. This brings up another interesting point, heap overallocation. Remember that cassandra depends on GC for clearing up unused memtables and other datastructures, allocating too much memory will cause GC to slow down.

Enable JNA

Ensure that you have the JNA (Java Native Access) library enabled in your cluster. It allows java to use native C methods and gives it access to native memory which is utilised for offheap storage for many of the datastructures inside of cassandra. Check logs for the following two, the latter meaning JNA was able to get access to native memory: JNA link failure, one or more native method will be unavailable. CLibrary.java (line 121) JNA mlockall successful

Memtable = offheap

Configure memtables to be stored in native memory rather than the JVM's heap, in cassandra.yaml: memtable_allocation_type: offheap_objects

Compaction

Use the correct Compaction Strategy for your workload! Leveled compaction can really help READ heavy workloads since it guarantees that in 90% of reads you'll be able to retreive the row you want from an individual sstable once it has been compacted to levels higher than 0. Size-tiered compaction can heal deal with WRITE-burst type workloads where you expect there to be very high pressure peaks of writes.

Swap

Make sure you've disabled Swap, we dont wont cassandra going into swap space, performance will degrade very rapidly (and set /proc/sys/vm/swappiness to 1 just incase it gets re-enabled by accident).

## Select hardware

Memory:

* The more memory a DataStax or Cassandra node has, the better read performance. 
* Production: 32 GB to 512 GB; the minimum is 8 GB for Cassandra only.

CPU:

* Insert-heavy workloads are CPU-bound in Cassandra before becoming memory-bound.

Disk:

* Cassandra need at least two disks per node, one for the commit log and the other for the data directories. At a minimum the commit log should be on its own partition.
* It is generally not necessary to use RAID.
* Generally RAID is not needed for the commit log disk. Replication adequately prevents data loss.
* DataStax recommends deploying Cassandra on XFS or ext4.

Network:

* DataStax recommends binding your interfaces to separate Network Interface Cards (NIC).

Load balancers:

* Cassandra was designed to avoid the need for load balancers. Putting load balancers between Cassandra and Cassandra clients is harmful to performance, cost, availability, debugging, testing, and scaling. All high-level clients, such as the Java and Python drivers for Cassandra, implement load balancing directly.

References:

* http://docs.datastax.com/en/landing_page/doc/landing_page/planning/planningAbout.html
* http://docs.datastax.com/en/landing_page/doc/landing_page/planning/planningHardware.html
* http://docs.datastax.com/en/landing_page/doc/landing_page/planning/planningAntiPatterns.html
* http://docs.datastax.com/en/landing_page/doc/landing_page/recommendedSettingsLinux.html

## Testing

### cassandra-stress

http://docs.datastax.com/en/cassandra/3.x/cassandra/tools/toolsCStress.html

standard1:

```
CREATE TABLE keyspace1.standard1 (
    key blob PRIMARY KEY,
    "C0" blob,
    "C1" blob,
    "C2" blob,
    "C3" blob,
    "C4" blob
) WITH COMPACT STORAGE
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'enabled': 'false'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

counter1:

```
CREATE TABLE keyspace1.counter1 (
    key blob,
    column1 text,
    "C0" counter static,
    "C1" counter static,
    "C2" counter static,
    "C3" counter static,
    "C4" counter static,
    value counter,
    PRIMARY KEY (key, column1)
) WITH COMPACT STORAGE
    AND CLUSTERING ORDER BY (column1 ASC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'enabled': 'false'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

References:

* http://docs.datastax.com/en/landing_page/doc/landing_page/planning/planningTesting.html
* https://docs.datastax.com/en/cassandra/3.x/cassandra/tools/toolsCStress.html
* http://stackoverflow.com/questions/31336753/usage-of-the-cassandra-tool-cassandra-stress
* http://www.datastax.com/1-million-writes
* http://techblog.netflix.com/2011/11/benchmarking-cassandra-scalability-on.html

## Cache
### overall
```
Memtable     : heap or off-heap
Row Cache    : off-heap
Bloom Filter : off-heep
Partition Key Cache    : off-heap
Partition Summary      : off-heap
Partition Index        : on-disk
Compression offset map : off-heap
```

cassandra.yaml:

```
# Total permitted memory to use for memtables. Cassandra will stop
# accepting writes when the limit is exceeded until a flush completes,
# and will trigger a flush based on memtable_cleanup_threshold
# If omitted, Cassandra will set both to 1/4 the size of the heap.
# memtable_heap_space_in_mb: 2048
# memtable_offheap_space_in_mb: 2048

# Specify the way Cassandra allocates and manages memtable memory.
# Options are:
#   heap_buffers:    on heap nio buffers
#   offheap_buffers: off heap (direct) nio buffers
#   offheap_objects: off heap objects
memtable_allocation_type: heap_buffers
```

```
memtable_allocation_type: offheap_objects
```

```
ALTER TABLE user WITH caching = { 'keys' : 'ALL', 'rows_per_partition' : 'ALL' };
```

### row cache
The row cache is not write-through. If a write comes in for the row, the cache for that row is invalidated and is not cached again until the row is read. Similarly, if a partition is updated, the entire partition is evicted from the cache.

## Tuning JVM

### How Cassandra uses memory 

Cassandra performs the following major operations within **JVM heap**:

* To perform **reads**, Cassandra maintains the following components in memory:
  * Bloom filters
  * Partition summary
  * Partition key cache
  * Compression offsets
  * SSTable index summary
* Cassandra **gathers** replicas for a read or for anti-entropy repair and compares the replicas in heap memory.
* Data **written** to Cassandra is first stored in memtables in heap memory. Memtables are flushed to SSTables on disk.

To improve performance, Cassandra also uses **off-heap memory** as follows:

* Page cache. Cassandra uses additional memory as page cache when reading files on disk.
* The Bloom filter and compression offset maps reside off-heap.
* Cassandra can store cached rows in native memory, outside the Java heap. This reduces JVM heap requirements, which helps keep the heap size in the sweet spot for JVM garbage collection performance.

see more at: http://docs.datastax.com/en/cassandra/3.x/cassandra/operations/opsTuneJVM.html

### OOM

(1) Out of memory error in MessagingService

https://issues.apache.org/jira/browse/CASSANDRA-12005

```
at org.apache.cassandra.db.Mutation$MutationSerializer.deserialize(Mutation.java:272) ~[apache-cassandra-2.2.5.jar:2.2.5]
at org.apache.cassandra.net.MessageIn.read(MessageIn.java:99) ~[apache-cassandra-2.2.5.jar:2.2.5]
at org.apache.cassandra.net.IncomingTcpConnection.receiveMessage(IncomingTcpConnection.java:200) ~[apache-cassandra-2.2.5.jar:2.2.5]
```

This happens when deserializing a mutation on a replica, and more precisely it seems to OOMs when allocating space for a value of that mutation.

solutions: reduced the number of `concurrent_compactors` and moved the `memtable_allocation_type` to `offheap_objects`

(2) JVM Crashed : Java Heap space

http://stackoverflow.com/questions/32098838/jvm-crashed-java-heap-space

```
at org.apache.cassandra.db.RangeSliceReply$RangeSliceReplySerializer.deserialize(RangeSliceReply.java:63) ~[apache-cassandra-2.1.8.jar:2.1.8]
at org.apache.cassandra.net.MessageIn.read(MessageIn.java:99) ~[apache-cassandra-2.1.8.jar:2.1.8]
at org.apache.cassandra.net.IncomingTcpConnection.receiveMessage(IncomingTcpConnection.java:188) ~[apache-cassandra-2.1.8.jar:2.1.8]
```

solutions: fixed this issue by configuring all nodes with MAX_HEAP_SIZE="4G" HEAP_NEWSIZE="1024M"
 
从上面两个问题，以及我们自己发生的问题，可以看到在不管是读还是写，JVM内存设置不当，都有可能导致OOM。

深入研究下读和写的路径：

* http://docs.datastax.com/en/cassandra/3.x/cassandra/dml/dmlAboutReads.html
* http://docs.datastax.com/en/cassandra/3.x/cassandra/dml/dmlHowDataWritten.html

### GC Pauses
https://support.datastax.com/hc/en-us/articles/204226199-Common-Causes-of-GC-pauses


### Tips

* Heap size is usually between 1/4 and 1/2 of system memory. Do not devote all memory to heap because it is also used for offheap cache and file system cache.
* Any pause of more than a second, or multiple pauses within a second that add to a large fraction of that second, should be avoided.
* G1 is recommended if Heap sizes from 14 GB to 64 GB.
* CMS is recommended if Heap sizes no larger than 14 GB.
* Properly tuning the OS page cache usually results in better performance than increasing the Cassandra row cache.

