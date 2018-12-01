# Spark Bucket

## Overview


## Bucket Join
```
CREATE TABLE user_b_1 (
user_id int,
name string
)
USING PARQUET
CLUSTERED BY (user_id) INTO 3 buckets;

insert into user_b_1 values(1, '1');
insert into user_b_1 values(2, '2');
insert into user_b_1 values(3, '3');
insert into user_b_1 values(4, '4');
insert into user_b_1 values(5, '5');
insert into user_b_1 values(6, '6');
insert into user_b_1 values(7, '7');
insert into user_b_1 values(8, '8');


CREATE TABLE user_b_2 (
user_id int,
age int
)
USING PARQUET
CLUSTERED BY (user_id) INTO 3 buckets;

insert into user_b_2 values(1, 1);
insert into user_b_2 values(2, 2);
insert into user_b_2 values(3, 3);
insert into user_b_2 values(4, 4);
insert into user_b_2 values(5, 5);
insert into user_b_2 values(6, 6);
insert into user_b_2 values(7, 7);
insert into user_b_2 values(8, 8);

CREATE TABLE user_b_3 (
user_id int,
name string,
age int
)
USING PARQUET
CLUSTERED BY (user_id) INTO 3 buckets;

select a.user_id, a.name, b.age from user_b_1 a, user_b_2 b where a.user_id = b.user_id;

```

container log:

```
17/09/20 10:12:05 INFO executor.CoarseGrainedExecutorBackend: Got assigned task 168
17/09/20 10:12:05 INFO executor.Executor: Running task 1.0 in stage 142.0 (TID 168)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Started reading broadcast variable 159
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_159_piece0 stored as bytes in memory (estimated size 4.9 KB, free 365.4 MB)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Reading broadcast variable 159 took 3 ms
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_159 stored as values in memory (estimated size 10.6 KB, free 365.4 MB)
17/09/20 10:12:05 INFO codegen.CodeGenerator: Code generated in 19.127467 ms
17/09/20 10:12:05 INFO datasources.FileScanRDD: Reading File path: hdfs://localhost/user/hive/warehouse/user_b_2/part-00000-63e7b91f-95c6-4954-94c9-0cc0fb48d035_00001.snappy.parquet, range: 0-520, partition values: [empty row]
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Started reading broadcast variable 158
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_158_piece0 stored as bytes in memory (estimated size 24.9 KB, free 365.4 MB)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Reading broadcast variable 158 took 7 ms
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_158 stored as values in memory (estimated size 393.3 KB, free 365.0 MB)
17/09/20 10:12:05 INFO compat.FilterCompat: Filtering using predicate: noteq(user_id, null)
17/09/20 10:12:05 INFO datasources.FileScanRDD: Reading File path: hdfs://localhost/user/hive/warehouse/user_b_2/part-00000-6f83aed6-7086-4649-bd98-cf653753f6a0_00001.snappy.parquet, range: 0-520, partition values: [empty row]
17/09/20 10:12:05 INFO compat.FilterCompat: Filtering using predicate: noteq(user_id, null)
17/09/20 10:12:05 INFO executor.Executor: Finished task 1.0 in stage 142.0 (TID 168). 2526 bytes result sent to driver
17/09/20 10:12:05 INFO executor.CoarseGrainedExecutorBackend: Got assigned task 169
17/09/20 10:12:05 INFO executor.Executor: Running task 2.0 in stage 142.0 (TID 169)
17/09/20 10:12:05 INFO executor.Executor: Finished task 2.0 in stage 142.0 (TID 169). 1437 bytes result sent to driver
17/09/20 10:12:05 INFO executor.CoarseGrainedExecutorBackend: Got assigned task 171
17/09/20 10:12:05 INFO executor.Executor: Running task 1.0 in stage 143.0 (TID 171)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Started reading broadcast variable 162
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_162_piece0 stored as bytes in memory (estimated size 5.9 KB, free 365.9 MB)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Reading broadcast variable 162 took 3 ms
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_162 stored as values in memory (estimated size 13.2 KB, free 365.9 MB)
17/09/20 10:12:05 INFO codegen.CodeGenerator: Code generated in 28.043097 ms
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Started reading broadcast variable 160
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_160_piece0 stored as bytes in memory (estimated size 316.0 B, free 365.9 MB)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Reading broadcast variable 160 took 6 ms
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_160 stored as values in memory (estimated size 344.0 B, free 365.9 MB)
17/09/20 10:12:05 INFO datasources.FileScanRDD: Reading File path: hdfs://localhost/user/hive/warehouse/user_b_1/part-00000-52ece7b0-cbfa-4c1e-a082-01be72462de8_00001.snappy.parquet, range: 0-513, partition values: [empty row]
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Started reading broadcast variable 161
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_161_piece0 stored as bytes in memory (estimated size 24.9 KB, free 365.8 MB)
17/09/20 10:12:05 INFO broadcast.TorrentBroadcast: Reading broadcast variable 161 took 4 ms
17/09/20 10:12:05 INFO memory.MemoryStore: Block broadcast_161 stored as values in memory (estimated size 393.3 KB, free 365.5 MB)
17/09/20 10:12:05 INFO compat.FilterCompat: Filtering using predicate: noteq(user_id, null)
17/09/20 10:12:05 INFO datasources.FileScanRDD: Reading File path: hdfs://localhost/user/hive/warehouse/user_b_1/part-00000-c43105ec-5a84-4189-a68f-55d68c5db25f_00001.snappy.parquet, range: 0-513, partition values: [empty row]
17/09/20 10:12:05 INFO compat.FilterCompat: Filtering using predicate: noteq(user_id, null)
17/09/20 10:12:05 INFO executor.Executor: Finished task 1.0 in stage 143.0 (TID 171). 2809 bytes result sent to driver
17/09/20 10:12:05 INFO executor.CoarseGrainedExecutorBackend: Got assigned task 172
17/09/20 10:12:05 INFO executor.Executor: Running task 2.0 in stage 143.0 (TID 172)
17/09/20 10:12:05 INFO executor.Executor: Finished task 2.0 in stage 143.0 (TID 172). 1582 bytes result sent to driver
```

for a bucket table (no matter partitioned or not): task num = bucket num

## Bucket and Partition
bucket only (no partition)

```
CREATE TABLE user_b (
user_id int,
name string
)
USING PARQUET
CLUSTERED BY (user_id) INTO 3 buckets;

insert into user_b values(1, 'sh-1');
insert into user_b values(2, 'sh-2');
insert into user_b values(3, 'sea-3');
insert into user_b values(4, 'sea-4');
insert into user_b values(5, 'sea-5');
insert into user_b values(6, 'sea-6');
insert into user_b values(7, 'lvc-7');
insert into user_b values(8, 'lvc-8');

select * from user_b;
4.1 KB
select * from user_b where user_id=1;
3.5 KB
```

bucket and partition:

```
CREATE TABLE user_p_b (
city string,
user_id int,
name string
)
USING PARQUET
PARTITIONED BY (city)
CLUSTERED BY (user_id) INTO 3 buckets;

insert into user_p_b values(1, 'sh-1', 'sh');
insert into user_p_b values(2, 'sh-2', 'sh');
insert into user_p_b values(3, 'sea-3', 'sea');
insert into user_p_b values(4, 'sea-4', 'sea');
insert into user_p_b values(5, 'sea-5', 'sjc');
insert into user_p_b values(6, 'sea-6', 'sjc');
insert into user_p_b values(7, 'lvc-7', 'lvc');
insert into user_p_b values(8, 'lvc-8', 'lvc');

select * from user_p_b;
4.1 KB
select * from user_p_b where city='sh';
1048.0 B
select * from user_p_b where user_id=1;
3.5 KB
select * from user_p_b where city='sh' and user_id=1;
966.0 B
```

## bucket pruning


