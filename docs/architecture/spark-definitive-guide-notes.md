# Spark The Definitive Guide Notes

## Chapter 1. What is Apache Spark

Apache Spark’s Philosophy

* Unified
* Computing engine
* Libraries

## chapter 19. Performance Tuning
Just as with monitoring, there are a number of different levels that you can try to tune at. For
instance, if you had an extremely fast network, that would make many of your Spark jobs faster
because shuffles are so often one of the costlier steps in a Spark job. Most likely, you won’t have
much ability to control such things; therefore, we’re going to discuss the things you can control
through code choices or configuration.

One of the best things you can do to figure out how to improve performance is to implement good
monitoring and job history tracking. Without this information, it can be difficult to know whether
you’re really improving job performance.

In Part III, we briefly discussed the serialization libraries that can be used within RDD
transformations. When you’re working with custom data types, you’re going to want to serialize them
using Kryo because it’s both more compact and much more efficient than Java serialization. However,
this does come at the inconvenience of registering the classes that you will be using in your application.

More often that not, when you’re saving data it will be read many times as other folks in your
organization access the same datasets in order to run different analyses. Making sure that you’re
storing your data for effective reads later on is absolutely essential to successful big data
projects. This involves choosing your storage system, choosing your data format, and taking
advantage of features such as data partitioning in some storage formats.

Generally you should always favor structured, binary types to store your data, especially when
you’ll be accessing it frequently. Although files like “CSV” seem well-structured, they’re very slow
to parse, and often also full of edge cases and pain points. The most efficient file format you can
generally choose is Apache Parquet.

In general, we recommend sizing your files so that they each contain at least a few tens of
megatbytes of data.

One way of controlling data partitioning when you write your data is through a write option
introduced in Spark 2.2. To control how many records go into each file, you can specify the
maxRecordsPerFile option to the write operation.

for RDD-based jobs, the serialization format has a large impact on shuffle performance—always prefer
Kryo over Java serialization.

spark.executor.extraJavaOptions = -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps

The goal of garbage collection tuning in Spark is to ensure that only long-lived cached datasets are
stored in the Old generation and that the Young generation is sufficiently sized to store all
short-lived objects. If a full garbage collection is invoked multiple times before a task completes,
it means that there isn’t enough memory available for executing tasks, so you should decrease the
amount of memory Spark uses for caching (spark.memory.fraction).

There are many more tuning options described online, but at a high level, managing how frequently
full garbage collection takes place can help in reducing the overhead. 