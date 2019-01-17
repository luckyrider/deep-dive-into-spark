# Spark Applications

## RDD

```
val lines = sc.textFile("file:///Users/cmao/Workspace/projects/github-seancxmao/spark/README.md")
val words = lines.flatMap(line => line.split(" "))
val wordTo1 = words.map(w => (w, 1))
val counts = wordTo1.reduceByKey(_ + _)
val someCounts = counts.take(10)
// scalastyle:off println
someCounts.foreach(println(_))
```

```
// active/completed job and stage
sc.parallelize(1 to 3, 3).map { n => Thread.sleep(10* 1000); n }.count
// failed job and stage
sc.parallelize(1 to 3, 3).map { n => Thread.sleep(10* 1000); throw new Exception() }.count
```

## spark-sql Apps
table population:

```
val person = Seq(
    (0, "Bill Chambers", 0, Seq(100)),
    (1, "Matei Zaharia", 1, Seq(500, 250, 100)),
    (2, "Michael Armbrust", 1, Seq(250, 100))).toDF("id", "name", "graduate_program", "spark_status")
val graduateProgram = Seq(
    (0, "Masters", "School of Information", "UC Berkeley"),
    (2, "Masters", "EECS", "UC Berkeley"),
    (1, "Ph.D.", "EECS", "UC Berkeley")).toDF("id", "degree", "department", "school")
val sparkStatus = Seq(
    (500, "Vice President"),
    (250, "PMC Member"),
    (100, "Contributor")).toDF("id", "status")
person.repartition(2, 'id).write.mode("overwrite").format("parquet").saveAsTable("person")
graduateProgram.repartition(2, 'id).write.mode("overwrite").format("parquet").saveAsTable("graduate_program")
sparkStatus.repartition(2, 'id).write.mode("overwrite").format("parquet").saveAsTable("spark_status")
```

```
spark-sql --conf spark.sql.autoBroadcastJoinThreshold=-1 --conf spark.sql.shuffle.partitions=2 --conf spark.sql.codegen.wholeStage=false
```

join:

```
select p.id, p.name, gp.school from person p join graduate_program gp on p.graduate_program = gp.id;
```

scalar subquery:

```
select p.id, p.name, gp.school, (select count(1) from person) total from person p join graduate_program gp on p.graduate_program = gp.id;
```

correlated subquery:

```
select p.id, p.name, gp.school, (select count(1) from graduate_program gp2 where gp2.school=gp.school) alumni from person p join graduate_program gp on p.graduate_program = gp.id;
```

## Standalone Apps
Spark project that uses Maven for building.  The app simply counts the number of lines in
a text file.

To build a JAR:

    mvn clean package

To run locally with Spark installed:

    spark-submit --master local target/ddis-sparkapps-0.1.0-jar-with-dependencies.jar <input file>

To run a REPL that can reference the objects and classes defined in this project:

    spark-shell --jars target/ddis-sparkapps-0.1.0-jar-with-dependencies.jar --master local

The `--master local` argument means that the application will run in a single local process. If the
cluster is running YARN, you can replace it with `--master yarn`.

To pass configuration options on the command line, use the `--conf` option, e.g.
`--conf spark.serializer=org.apache.spark.serializer.KryoSerializer`.
