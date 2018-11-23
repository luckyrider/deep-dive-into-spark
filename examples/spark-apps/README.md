Spark Applications
==============

Spark project that uses Maven for building.  The app simply counts the number of lines in
a text file.

To build a JAR:

    mvn clean package

To run locally with Spark installed:

    spark-submit --master local target/spark-apps-0.1.0-jar-with-dependencies.jar <input file>

To run a REPL that can reference the objects and classes defined in this project:

    spark-shell --jars target/spark-apps-0.1.0-jar-with-dependencies.jar --master local

The `--master local` argument means that the application will run in a single local process. If the
cluster is running YARN, you can replace it with `--master yarn`.

To pass configuration options on the command line, use the `--conf` option, e.g.
`--conf spark.serializer=org.apache.spark.serializer.KryoSerializer`.
