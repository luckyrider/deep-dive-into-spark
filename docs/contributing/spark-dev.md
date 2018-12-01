# Spark Development

## Build
### Overview
http://spark.apache.org/docs/latest/building-spark.html

### maven or sbt
Maven is the official build tool recommended for packaging Spark, and is the build of reference. 

But SBT is supported for day-to-day development since it can provide much faster iterative compilation. More advanced developers may wish to use SBT.

### maven
requirements: Maven 3.3.9 or newer and Java 7+

export MAVEN_OPTS="-Xmx2g -XX:ReservedCodeCacheSize=512m"

自带maven（build/mvn），会自动下载maven, scala, zinc。如果本地有maven，会优先使用本地的maven，但是仍然会下载和使用Scala和Zinc。

```
./build/mvn -Pyarn -Phadoop-2.7 -Dhadoop.version=2.7.0 -Phive -Phive-thriftserver -DskipTests clean package
./build/mvn -Pyarn -Phadoop-2.7 -Dhadoop.version=2.7.3 -Phive -Phive-thriftserver -DskipTests clean package
```

### 构建Distribution
跟直接使用maven一样，可以指定profile等选项

```
dev/make-distribution.sh --name custom-spark --tgz -Psparkr -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn
```

for more options: 

```
dev/make-distribution.sh --help
make-distribution.sh - tool for making binary distributions of Spark
usage:
make-distribution.sh [--name] [--tgz] [--mvn <mvn-command>] <maven build options>
```

sourecode:

```
BUILD_COMMAND=("$MVN" -T 1C clean package -DskipTests $@)
```

利用了并行构建功能：

```
mvn -T 1C clean install # 1 thread per cpu core
```

see more:

* https://cwiki.apache.org/confluence/display/MAVEN/Parallel+builds+in+Maven+3

### HDFS
Read/write HDFS.

build:

```
-Phadoop-2.7 -Dhadoop.version=2.7.3
```

pom:

```
    <profile>
      <id>hadoop-2.7</id>
      <properties>
        <hadoop.version>2.7.3</hadoop.version>
        <jets3t.version>0.9.3</jets3t.version>
        <zookeeper.version>3.4.6</zookeeper.version>
        <curator.version>2.6.0</curator.version>
      </properties>
    </profile>
```

### YARN
Spark on YARN.

build:

```
-Pyarn
```

pom:

```
    <profile>
      <id>yarn</id>
      <modules>
        <module>yarn</module>
        <module>common/network-yarn</module>
      </modules>
    </profile>
```

### Hive and JDBC support
build:

```
-Phive -Phive-thriftserver
```

pom:

```
    <hive.group>org.spark-project.hive</hive.group>
    <!-- Version used in Maven Hive dependency -->
    <hive.version>1.2.1.spark2</hive.version>
    <!-- Version used for internal directory structure -->
    <hive.version.short>1.2.1</hive.version.short>
    <derby.version>10.12.1.1</derby.version>
```

### R

安装R：下载mac包（R-3.3.2.pkg），点击安装在默认位置。

```
export R_HOME=/Library/Frameworks/R.framework/Resources/
```

```
-Psparkr
```

see more:

* https://www.anchormen.nl/executing-r-scripts-from-within-a-spark-job/

### Packaging without Hadoop Dependencies for YARN
build:

```
-Phadoop-provided
```

pom:

```
    <profile>
      <id>hadoop-provided</id>
    </profile>
```

### release build
spark.git/dev/create-release/release-build.sh:

```
  # We increment the Zinc port each time to avoid OOM's and other craziness if multiple builds
  # share the same Zinc server.
  make_binary_release "hadoop2.3" "-Psparkr -Phadoop-2.3 -Phive -Phive-thriftserver -Pyarn" "3033" &
  make_binary_release "hadoop2.4" "-Psparkr -Phadoop-2.4 -Phive -Phive-thriftserver -Pyarn" "3034" &
  make_binary_release "hadoop2.6" "-Psparkr -Phadoop-2.6 -Phive -Phive-thriftserver -Pyarn" "3035" &
  make_binary_release "hadoop2.7" "-Psparkr -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn" "3036" &
  make_binary_release "hadoop2.4-without-hive" "-Psparkr -Phadoop-2.4 -Pyarn" "3037" &
  make_binary_release "without-hadoop" "-Psparkr -Phadoop-provided -Pyarn" "3038" &
```

### troubleshooting: java8-tests_2.11 build failed
`.m2/settings.xml`设置了profile jdk17，导致`java8-tests_2.11`编译失败。如果注释掉profile jdk17，build成功。

```
<profiles>
        <profile>
            <id>jdk17</id>
            <activation>
                <activeByDefault>true</activeByDefault>
                <jdk>1.7</jdk>
            </activation>
            <properties>
                <maven.compiler.source>1.7</maven.compiler.source>
                <maven.compiler.target>1.7</maven.compiler.target>
                <maven.compiler.compilerVersion>1.7</maven.compiler.compilerVersion>
            </properties>
        ...
        </profile>
...
</profiles>
```

使用`mvn help:effective-pom`分析`.m2/settings.xml`带来的影响，最终的pom唯一区别是：

```
    <maven.compiler.compilerVersion>1.7</maven.compiler.compilerVersion>
    <maven.compiler.source>1.7</maven.compiler.source>
    <maven.compiler.target>1.7</maven.compiler.target>
```

see also: 

* https://maven.apache.org/plugins/maven-compiler-plugin/examples/set-compiler-source-and-target.html

### build with sbt
The SBT build is derived from the Maven POM files, and so the same Maven profiles and variables can be set to control the SBT build.

```
build/sbt clean package -Phadoop-2.7 -Phive -Phive-thriftserver -Pyarn -Psparkr
```

## Test


## Debug



