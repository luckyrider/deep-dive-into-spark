# Spark Tungsten

## Overview
Project Tungsten will be the largest change to Spark’s execution engine since the project’s inception. It focuses on substantially improving the efficiency of memory and CPU for Spark applications, to push performance closer to the limits of modern hardware. This effort includes three initiatives:
* Memory Management and Binary Processing: leveraging application semantics to manage memory explicitly and eliminate the overhead of JVM object model and garbage collection
* Cache-aware computation: algorithms and data structures to exploit memory hierarchy
* Code generation: using code generation to exploit modern compilers and CPUs


key points:

* whole stage code generation
* vectorization

## Troubleshooting

### Java 7 broken code cache flushing
Databricks people discuss the JAVA 7 issue that has negative impact on  Spark code gen:

* http://apache-spark-developers-list.1001551.n3.nabble.com/discuss-ending-support-for-Java-7-in-Spark-2-0-td16808.html

java 7 CodeCache issues:

* https://blogs.oracle.com/poonam/entry/why_do_i_get_message
* https://bugs.openjdk.java.net/browse/JDK-8051955

The following are two known problems in jdk7u4+ with respect to the CodeCache flushing:

1. The compiler may not get restarted even after the CodeCache occupancy drops down to almost half after the emergency flushing.
2. The emergency flushing may cause high CPU usage by the compiler threads leading to overall performance degradation.


## References
* Tungsten Phase 1. https://databricks.com/blog/2015/04/28/project-tungsten-bringing-spark-closer-to-bare-metal.html
* Tungsten Phase 2: Speed up Apache Spark by 10X. https://databricks.com/blog/2016/05/23/apache-spark-as-a-compiler-joining-a-billion-rows-per-second-on-a-laptop.html
