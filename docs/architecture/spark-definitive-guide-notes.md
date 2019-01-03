# Spark The Definitive Guide Notes

## Chapter 1. What is Apache Spark

Apache Spark’s Philosophy

* Unified
* Computing engine
* Libraries

Spark is designed to support a wide range of data analytics tasks, ranging from simple data loading
and SQL queries to machine learning and streaming computation, over the same computing engine and
with a consistent set of APIs.

Spark provides consistent, composable APIs that you can use to build an application out of smaller
pieces or out of existing libraries. It also makes it easy for you to write your own analytics
libraries on top. However, composable APIs are not enough: Spark’s APIs are also designed to enable
high performance by optimizing across the different libraries and functions composed together in a
user program.

Why do we need a new engine and programming model for data analytics in the first place? As with 
many trends in computing, this is due to changes in the economic factors that underlie computer
applications and hardware.

Unfortunately, this trend in hardware stopped around 2005: due to hard limits in heat dissipation, 
hardware developers stopped making individual processors faster, and switched toward adding more 
parallel CPU cores all running at the same speed. This change meant that suddenly applications 
needed to be modified to add parallelism in order to run faster, which set the stage for new 
programming models such as Apache Spark.

The AMPlab had worked with multiple early MapReduce users to understand the benefits and drawbacks
of this new programming model, and was therefore able to synthesize a list of problems across
several use cases and begin designing more general computing platforms. In addition, Zaharia had
also worked with Hadoop users at UC Berkeley to understand their needs for the platform—specifically,
teams that were doing large-scale machine learning using iterative algorithms that need to make 
multiple passes over the data.

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

When we cache an RDD, we cache the actual, physical data (i.e., the bits). The bits. When this data
is accessed again, Spark returns the proper data. This is done through the RDD reference. However,
in the Structured API, caching is done based on the physical plan. This means that we effectively
store the physical plan as our key (as opposed to the object reference) and perform a lookup prior
to the execution of a Structured job.

Joins are a common area for optimization. The biggest weapon you have when it comes to optimizing
joins is simply educating yourself about what each join does and how it’s performed. This will help
you the most. Additionally, equi-joins are the easiest for Spark to optimize at this point and
therefore should be preferred wherever possible. Beyond that, simple things like trying to use the
filtering ability of inner joins by changing join ordering can yield large speedups. Additionally,
using broadcast join hints can help Spark make intelligent planning decisions when it comes to
creating query plans, as described in Chapter 8. Avoiding Cartesian joins or even full outer joins
is often low-hanging fruit for stability and optimizations because these can often be optimized into
different filtering style joins when you look at the entire data flow instead of just that one
particular job area. Lastly, following some of the other sections in this chapter can have a
significant effect on joins. For example, collecting statistics on tables prior to a join will help
Spark make intelligent join decisions. Additionally, bucketing your data appropriately can also help
Spark avoid large shuffles when joins are performed.

In general, the main things you’ll want to prioritize are (1) reading as little data as possible
through partitioning and efficient binary formats, (2) making sure there is sufficient parallellism
and no data skew on the cluster using partitioning, and (3) using high-level APIs such as the
Structured APIs as much as possible to take already optimized code.