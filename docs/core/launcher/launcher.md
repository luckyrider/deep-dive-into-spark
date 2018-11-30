# Launcher

## Overview
* Launch an interactive shell
* Launch a batch application
* Launch an app programmatically


## Launch an interactive shell
`spark-shell` calls `spark-submit`, which in turn calls `spark-class`.

`bin/spark-shell`

```
function main() {
  if $cygwin; then
    ...
  else
    export SPARK_SUBMIT_OPTS
    "${SPARK_HOME}"/bin/spark-submit --class org.apache.spark.repl.Main --name "Spark shell" "$@"
  fi
}
```

`bin/spark-submit`

```
exec "${SPARK_HOME}"/bin/spark-class org.apache.spark.deploy.SparkSubmit "$@"
```

For a simple spark-shell command:

```
spark-shell --name my-spark-shell --master yarn --conf spark.driver.memory=512m
```

The above command results in calling the following commands subsequently.

> /Users/cmao/Workspace/deploy/spark/bin/spark-submit --class org.apache.spark.repl.Main 
> --name Spark shell --name my-spark-shell --master yarn --conf spark.driver.memory=512m

> /Users/cmao/Workspace/deploy/spark/bin/spark-class org.apache.spark.deploy.SparkSubmit 
--class org.apache.spark.repl.Main --name Spark shell --name my-spark-shell --master yarn 
--conf spark.driver.memory=512m

> /Library/Java/JavaVirtualMachines/jdk1.8.0_131.jdk/Contents/Home/bin/java -cp 
/Users/cmao/Workspace/deploy/spark-conf/:/Users/cmao/Workspace/deploy/spark/jars/*:/Users/cmao/Workspace/dataplatform/deploy/hadoop-conf:/Users/cmao/Workspace/deploy/hadoop-conf/:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/common/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/common/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/hdfs/:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/hdfs/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/hdfs/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/yarn/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/yarn/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/mapreduce/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/mapreduce/*:/Users/cmao/Workspace/deploy/hadoop/contrib/capacity-scheduler/*.jar:/Users/cmao/Workspace/deploy/hive-conf/ 
-Dscala.usejavacp=true -Xmx512m org.apache.spark.deploy.SparkSubmit --master yarn 
--conf spark.driver.memory=512m --class org.apache.spark.repl.Main --name Spark shell 
--name my-spark-shell spark-shell

The final java command is generated using `org.apache.spark.launcher.Main`.

`bin/spark-class`

```
build_command() {
  "$RUNNER" -Xmx128m -cp "$LAUNCH_CLASSPATH" org.apache.spark.launcher.Main "$@"
  printf "%d\0" $?
}
```

`org.apache.spark.launcher.Main` is Command line interface for the Spark launcher. Used internally by Spark scripts. Its usage:

> Usage: Main [class] [class args]
>
> This CLI works in two different modes:
>
> * "spark-submit": if class is "org.apache.spark.deploy.SparkSubmit", the SparkLauncher (SparkSubmit?) class is used to launch a Spark application.
> * "spark-class": if another class is provided, an internal Spark class is run.
>
> This class works in tandem with the "bin/spark-class" script on Unix-like systems, and "bin/spark-class2.cmd" batch script on Windows to execute the final command.
On Unix-like systems, the output is a list of command arguments, separated by the NULL character. On Windows, the output is a command line suitable for direct execution from the script.

`org.apache.spark.deploy.SparkSubmit` is the main gateway of launching a Spark application, 
which uses `org.apache.spark.deploy.SparkSubmitArguments` to parse and encapsulate arguments from the spark-submit script.
The first unrecognized option is treated as the "primary resource". Everything else is treated as application arguments.
`spark-shell` is one of special primary resources. Other special primary resources are `pyspark-shell`, `sparkr-shell`, and etc, which represent shells rather than application jars.

## Launch a batch application

> spark-submit --name "ddis.simpleapp.SimpleApp (with handle)" --master yarn --conf spark.driver.memory=512m 
> target/simpleapp-0.1.0-jar-with-dependencies.jar README.md

> /Users/cmao/Workspace/deploy/spark/bin/spark-class org.apache.spark.deploy.SparkSubmit --name ddis.simpleapp.SimpleApp (with handle) 
> --master yarn --conf spark.driver.memory=512m target/simpleapp-0.1.0-jar-with-dependencies.jar README.md

> /Library/Java/JavaVirtualMachines/jdk1.8.0_131.jdk/Contents/Home/bin/java 
> -cp /Users/cmao/Workspace/deploy/spark-conf/:/Users/cmao/Workspace/deploy/spark/jars/*:/Users/cmao/Workspace/dataplatform/deploy/hadoop-conf:/Users/cmao/Workspace/deploy/hadoop-conf/:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/common/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/common/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/hdfs/:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/hdfs/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/hdfs/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/yarn/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/yarn/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/mapreduce/lib/*:/Users/cmao/Workspace/deploy/hadoop-2.7.3/share/hadoop/mapreduce/*:/Users/cmao/Workspace/deploy/hadoop/contrib/capacity-scheduler/*.jar:/Users/cmao/Workspace/deploy/hive-conf/ 
> -Xmx512m org.apache.spark.deploy.SparkSubmit --master yarn --conf spark.driver.memory=512m 
> --name ddis.simpleapp.SimpleApp (with handle) target/simpleapp-0.1.0-jar-with-dependencies.jar README.md

## Launch an application programmatically


