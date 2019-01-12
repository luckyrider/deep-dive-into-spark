# Cassandra Delete

## Overview

* https://docs.datastax.com/en/cassandra/3.x/cassandra/dml/dmlAboutDeletes.html, 官方文档。
* http://thelastpickle.com/blog/2016/07/27/about-deletes-and-tombstones.html, 这篇文章把Cassandra的delete机制（tombstone）讲得非常清楚，可以跟着作者的例子进行实际操练。
* http://www.datastax.com/dev/blog/cassandra-anti-patterns-queues-and-queue-like-datasets

## Delete
LSM-tree

delete with tombstone:

* cell delete
* row delete
* partition delete

This gc_grace_seconds parameters is the minimal time that tombstones will be kept on disk after data has been deleted. We need to make sure that all the replicas also received the delete and have tombstone stored to avoid having some zombie data issues. Our only way to achieve that is a full repair. After gc_grace_seconds, the tombstone will eventually be evicted.

## TTL

* http://docs.datastax.com/en/cql/3.3/cql/cql_using/useTTL.html
* http://docs.datastax.com/en/cql/3.1/cql/cql_using/use_expire_c.html
* https://docs.datastax.com/en/cql/3.3/cql/cql_reference/tabProp.html, default_time_to_live


ttl on column, not ttl on row:

* http://cjwebb.github.io/blog/2015/03/02/cassandra-ttl-is-per-column/
* https://issues.apache.org/jira/browse/CASSANDRA-7534
* http://stackoverflow.com/questions/16544051/cassandra-ttl-on-a-row

### Column TTL

```
INSERT INTO user(id, age, first_name, last_name) VALUES (6, 6, '6f', '6l') USING TTL 60;

select TTL(age) from user where id = 6;

select TTL(id) from user where id = 6;
InvalidRequest: code=2200 [Invalid query] message="Cannot use selection function ttl on PRIMARY KEY part id"

UPDATE user USING TTL 300 SET age = 1 where id = 1;
```

Cannot use selection function ttl on PRIMARY KEY part:

* [TTLs on tables with *only* primary keys?](https://groups.google.com/forum/#!topic/nosql-databases/clH_MNX41h8)

### Table TTL
* default_time_to_live: If it is set, Cassandra applies a default Time To Live (TTL) marker to each column in the table, set to this value.
* gc_grace_seconds: The number of seconds after data is marked with a tombstone (deletion marker) before it is eligible for garbage-collection. The default value allows a great deal of time for Cassandra to maximize consistency prior to deletion.

```
CREATE TABLE test.user_with_ttl (
    id int PRIMARY KEY,
    age int,
    first_name text,
    last_name text
) WITH default_time_to_live = 120;

00:00:00
INSERT INTO user_with_ttl(id, age, first_name, last_name) VALUES (1, 1, '1f', '1l'); 
select * from user_with_ttl;
 id | age | first_name | last_name
----+-----+------------+-----------
  1 |   1 |         1f |        1l

00:01:00
INSERT INTO user_with_ttl(id, age, first_name, last_name) VALUES (2, 2, '2f', '2l');
select * from user_with_ttl;
 id | age | first_name | last_name
----+-----+------------+-----------
  1 |   1 |         1f |        1l
  2 |   2 |         2f |        2l

00:01:50
select * from user_with_ttl;
 id | age | first_name | last_name
----+-----+------------+-----------
  1 |   1 |         1f |        1l
  2 |   2 |         2f |        2l

00:02:10
select * from user_with_ttl;
 id | age | first_name | last_name
----+-----+------------+-----------
  2 |   2 |         2f |        2l

00:02:50
select * from user_with_ttl;
 id | age | first_name | last_name
----+-----+------------+-----------
  2 |   2 |         2f |        2l

00:03:10
select * from user_with_ttl;
 id | age | first_name | last_name
----+-----+------------+-----------
```


## delete column, column ttl, table ttl

### delete columns individually
过期后，能查到row，所有字段都是null。

```
delete first_name from user where id = 1;
delete last_name from user where id = 1;
delete age from user where id = 1;

select * from user;

 id | age  | first_name | last_name
----+------+------------+-----------
  1 | null |       null |      null
```


### update column using ttl individually
过期后，能查到row，所有字段都是null。

```
UPDATE user USING TTL 60 SET age = 22 where id = 2;
UPDATE user USING TTL 60 SET first_name = '2f' where id = 2;
UPDATE user USING TTL 60 SET last_name = '2l' where id = 2;


 id | age  | first_name | last_name
----+------+------------+-----------
  2 | null |       null |      null
```


### create table with ttl property
过期后，查不到row。

```
CREATE TABLE test.user_with_ttl (
    id int PRIMARY KEY,
    age int,
    first_name text,
    last_name text
) WITH default_time_to_live = 120;

INSERT INTO user_with_ttl(id, age, first_name, last_name) VALUES (1, 1, '1f', '1l'); 
UPDATE user_with_ttl USING TTL 240 SET age = 11 where id = 1;


select ttl(age),ttl(first_name),ttl(last_name) from user_with_ttl ;
 ttl(age) | ttl(first_name) | ttl(last_name)
----------+-----------------+----------------
      136 |            null |           null
select * from user_with_ttl ;
 id | age | first_name | last_name
----+-----+------------+-----------
  1 |  11 |       null |      null


select ttl(age),ttl(first_name),ttl(last_name) from user_with_ttl ;
 ttl(age) | ttl(first_name) | ttl(last_name)
----------+-----------------+----------------
select * from user_with_ttl ;
 id | age | first_name | last_name
----+-----+------------+-----------
```

### insert entire row using ttl
过期后，查不到row。

```
INSERT INTO user(id, age, first_name, last_name) VALUES (1, 1, '1f', '1l') USING TTL 60;
INSERT INTO user(id, age) VALUES (1, 1) using ttl 160;
select * from user where id = 1;
 id | age  | first_name | last_name
----+------+------------+-----------
```

### update entire row using ttl
过期后，能查到row，所有字段为null。

```
INSERT INTO user(id, age, first_name, last_name) VALUES (1, 1, '1f', '1l');

UPDATE user USING TTL 60 SET age = 11, first_name='1f', last_name='1l' where id = 1;

select ttl(age), ttl(first_name), ttl(last_name) from user where id = 1;
 ttl(age) | ttl(first_name) | ttl(last_name)
----------+-----------------+----------------
       56 |              56 |             56

select ttl(age), ttl(first_name), ttl(last_name) from user where id = 1;
 ttl(age) | ttl(first_name) | ttl(last_name)
----------+-----------------+----------------
     null |            null |           null

select * from user where id = 1;
 id | age  | first_name | last_name
----+------+------------+-----------
  1 | null |       null |      null
```

