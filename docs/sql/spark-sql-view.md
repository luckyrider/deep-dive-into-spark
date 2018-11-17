# Spark SQL View

## Issues

### SPARK-25797
* https://github.com/apache/spark/pull/16613
* https://github.com/apache/spark/pull/16869

* decimalExpressions.scala
* views.scala

## In Action

### Hive compatibility
Create table and view via Hive:

```
CREATE TABLE t1 (c1 INT, c2 STRING);

CREATE VIEW v1 AS SELECT c1 + 1, upper(c2) FROM t1;

CREATE VIEW v2 AS SELECT * FROM (SELECT c1 + 1, upper(c2) FROM t1) t2;

CREATE VIEW v3 AS SELECT * FROM (SELECT c1 + 1 AS inc_c1, upper(c2) AS upper_c2 FROM t1) t2;
```

Why v1 works?

```
spark-sql> explain extended select * from v1;
_c0: int, _c1: string
Project [_c0#285, _c1#286]
+- SubqueryAlias v1
   +- View (`default`.`v1`, [_c0#285,_c1#286])
      +- Project [cast((c1 + 1)#289 as int) AS _c0#285, cast(upper(c2)#290 as string) AS _c1#286] // added by AliasViewChild
         +- Project [(c1#287 + 1) AS (c1 + 1)#289, upper(c2#288) AS upper(c2)#290]
            +- SubqueryAlias t1
               +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#287, c2#288]
```

Why v2 does not work?

```
spark-sql> select * from v2;
Error in query: cannot resolve '`t2._c0`' given input columns: [t2.(c1 + 1), t2.upper(c2)]; line 1 pos 7;
'Project [*]
+- 'SubqueryAlias v2
   +- View (`default`.`v2`, [_c0#317,_c1#318])
      +- 'Project ['t2._c0, 't2._c1]  // add by 
         +- SubqueryAlias t2
            +- Project [(c1#319 + 1) AS (c1 + 1)#321, upper(c2#320) AS upper(c2)#322]
               +- SubqueryAlias t1
                  +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#319, c2#320]
```

```
spark-sql> SELECT * FROM (SELECT c1 + 1, upper(c2) FROM t1) t2;
(c1 + 1): int, upper(c2): string
Project [(c1 + 1)#327, upper(c2)#328]
+- SubqueryAlias t2
   +- Project [(c1#325 + 1) AS (c1 + 1)#327, upper(c2#326) AS upper(c2)#328]
      +- SubqueryAlias t1
         +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#325, c2#326]
```

Analyzer debug log

```
03:31:23.622 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't1.c1 to c1#9
03:31:23.623 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't1.c2 to c2#10
03:31:23.655 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't2._c0 to 't2._c0
03:31:23.655 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't2._c1 to 't2._c1
03:31:23.659 DEBUG org.apache.spark.sql.hive.HiveSessionStateBuilder$$anon$1: 
=== Result of Batch Resolution ===
 'Project ['t2._c0, 't2._c1]                                                                   'Project ['t2._c0, 't2._c1]
!+- 'SubqueryAlias `t2`                                                                        +- SubqueryAlias `t2`
!   +- 'Project [unresolvedalias(('t1.c1 + 1), None), unresolvedalias('upper('t1.c2), None)]      +- Project [(c1#9 + 1) AS (c1 + 1)#11, upper(c2#10) AS upper(c2)#12]
!      +- 'UnresolvedRelation `default`.`t1`                                                         +- SubqueryAlias `default`.`t1`
!                                                                                                       +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#9, c2#10]
          
03:31:23.666 DEBUG org.apache.spark.sql.hive.HiveSessionStateBuilder$$anon$1: 
=== Result of Batch Post-Hoc Resolution ===
 'Project ['t2._c0, 't2._c1]                                                                                       'Project ['t2._c0, 't2._c1]
 +- SubqueryAlias `t2`                                                                                             +- SubqueryAlias `t2`
    +- Project [(c1#9 + 1) AS (c1 + 1)#11, upper(c2#10) AS upper(c2)#12]                                              +- Project [(c1#9 + 1) AS (c1 + 1)#11, upper(c2#10) AS upper(c2)#12]
       +- SubqueryAlias `default`.`t1`                                                                                   +- SubqueryAlias `default`.`t1`
          +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#9, c2#10]            +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#9, c2#10]
          
03:31:23.669 DEBUG org.apache.spark.sql.hive.HiveSessionStateBuilder$$anon$1: 
=== Result of Batch Cleanup ===
 'Project ['t2._c0, 't2._c1]                                                                                       'Project ['t2._c0, 't2._c1]
 +- SubqueryAlias `t2`                                                                                             +- SubqueryAlias `t2`
    +- Project [(c1#9 + 1) AS (c1 + 1)#11, upper(c2#10) AS upper(c2)#12]                                              +- Project [(c1#9 + 1) AS (c1 + 1)#11, upper(c2#10) AS upper(c2)#12]
       +- SubqueryAlias `default`.`t1`                                                                                   +- SubqueryAlias `default`.`t1`
          +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#9, c2#10]            +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#9, c2#10]
          
03:31:23.670 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't2._c0 to 't2._c0
03:31:23.670 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't2._c1 to 't2._c1
03:31:23.687 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't2._c0 to 't2._c0
03:31:23.688 DEBUG org.apache.spark.sql.catalyst.analysis.Analyzer$ResolveReferences: Resolving 't2._c1 to 't2._c1
03:31:23.697 DEBUG org.apache.spark.sql.hive.HiveSessionStateBuilder$$anon$1: 
=== Result of Batch Resolution ===
 'Project [*]                  'Project [*]
!+- 'UnresolvedRelation `v2`   +- 'SubqueryAlias `default`.`v2`
!                                 +- View (`default`.`v2`, [_c0#7,_c1#8])
!                                    +- 'Project ['t2._c0, 't2._c1]
!                                       +- SubqueryAlias `t2`
!                                          +- Project [(c1#9 + 1) AS (c1 + 1)#11, upper(c2#10) AS upper(c2)#12]
!                                             +- SubqueryAlias `default`.`t1`
!                                                +- HiveTableRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#9, c2#10]
```

### QueryPlan
```
create table t1 (
  c1 decimal(18,0)
)

create view v1 as select * from t1;
```

```
spark-sql> explain extended select * from t1;
== Parsed Logical Plan ==
'Project [*]
+- 'UnresolvedRelation `t1`

== Analyzed Logical Plan ==
c1: decimal(18,0)
Project [c1#149]
+- SubqueryAlias t1
   +- CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#149]

== Optimized Logical Plan ==
CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#149]

== Physical Plan ==
HiveTableScan [c1#149], CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#149]
```

```
spark-sql> create table t1 (
         > c1 decimal(18,0)
         > );
spark-sql> create view v1 as select * from t1;
Time taken: 0.137 seconds
spark-sql> explain extended select * from v1;
== Parsed Logical Plan ==
'Project [*]
+- 'UnresolvedRelation `v1`

== Analyzed Logical Plan ==
c1: decimal(18,0)
Project [c1#144]
+- SubqueryAlias v1
   +- View (`default`.`v1`, [c1#144])
      +- Project [cast(c1#145 as decimal(18,0)) AS c1#144]
         +- Project [c1#145]
            +- SubqueryAlias t1
               +- CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#145]

== Optimized Logical Plan ==
CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#145]

== Physical Plan ==
HiveTableScan [c1#145], CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#145]
```

```
spark-sql> explain extended select c1 c2 from t1 t2;
== Parsed Logical Plan ==
'Project ['c1 AS c2#151]
+- 'SubqueryAlias t2
   +- 'UnresolvedRelation `t1`

== Analyzed Logical Plan ==
c2: decimal(18,0)
Project [c1#154 AS c2#151]
+- SubqueryAlias t2
   +- SubqueryAlias t1
      +- CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#154]

== Optimized Logical Plan ==
Project [c1#154 AS c2#151]
+- CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#154]

== Physical Plan ==
*Project [c1#154 AS c2#151]
+- HiveTableScan [c1#154], CatalogRelation `default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, [c1#154]
```

### CatalogTable

```
spark-sql> create database db1;
spark-sql> create database db2;
spark-sql> use db1;
spark-sql> create table t1(c1 decimal(18,0));
spark-sql> create view db2.v1 as select (cast(c1 as decimal(18,0)) + cast(c1 as decimal(18,0))) c1 from t1;
spark-sql> desc extended db2.v1;
c1	decimal(19,0)	NULL

# Detailed Table Information	CatalogTable(
	Table: `db2`.`v1`
	Owner: cmao
	Created: Wed Oct 24 14:06:19 CST 2018
	Last Access: Thu Jan 01 08:00:00 CST 1970
	Type: VIEW
	Schema: [StructField(c1,DecimalType(19,0),true)]
	Original View: select (cast(c1 as decimal(18,0)) + cast(c1 as decimal(18,0))) c1 from t1
	View: SELECT `gen_attr_0` AS `c1` FROM (SELECT (CAST(CAST(`gen_attr_1` AS DECIMAL(18,0)) AS DECIMAL(19,0)) + CAST(CAST(`gen_attr_1` AS DECIMAL(18,0)) AS DECIMAL(19,0))) AS `gen_attr_0` FROM (SELECT `c1` AS `gen_attr_1` FROM `db1`.`t1`) AS gen_subquery_0) AS gen_subquery_1
	Properties: [transient_lastDdlTime=1540361179]
	Storage(InputFormat: org.apache.hadoop.mapred.SequenceFileInputFormat, OutputFormat: org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat, Serde: org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, Properties: [serialization.format=1]))
```

