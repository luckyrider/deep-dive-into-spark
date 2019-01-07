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

## Chapter 2. A Gentle Introduction to Spark
A group of machines alone is not powerful, you need a framework to coordinate work across them. The
cluster of machines that Spark will use to execute tasks is managed by a cluster manager.

The driver process runs your main() function, sits on a node in the cluster, and is responsible for 
three things: maintaining information about the Spark Application; responding to a user’s program or 
input; and analyzing, distributing, and scheduling work across the executors (discussed momentarily). 
The driver process is absolutely essential—it’s the heart of a Spark Application and maintains all 
relevant information during the lifetime of the application.

The executors are responsible for actually carrying out the work that the driver assigns them. This 
means that each executor is responsible for only two things: executing code assigned to it by the 
driver, and reporting the state of the computation on that executor back to the driver node.

Spark supports a subset of the ANSI SQL 2003 standard. 

When using Spark from Python or R, you don’t write explicit JVM instructions; instead, you write 
Python and R code that Spark translates into code that it then can run on the executor JVMs.

Although you can drive Spark from a variety of languages, what it makes available in those languages 
is worth mentioning. Spark has two fundamental sets of APIs: the low-level “unstructured” APIs, and 
the higher-level structured APIs.

There is a one-to-one correspondence between a SparkSession and a Spark Application.

The DataFrame concept is not unique to Spark. R and Python both have similar concepts. because Spark 
has language interfaces for both Python and R, it’s quite easy to convert Pandas (Python) DataFrames 
to Spark DataFrames, and R DataFrames to Spark DataFrames.

The easiest and most efficient are DataFrames, which are available in all languages.

There are two types of transformations: those that specify narrow dependencies, and those that 
specify wide dependencies.

A wide dependency (or wide transformation) style transformation will have input partitions 
contributing to many output partitions. You will often hear this referred to as a shuffle whereby 
Spark will exchange partitions across the cluster. With narrow transformations, Spark will 
automatically perform an operation called pipelining, meaning that if we specify multiple filters on 
DataFrames, they’ll all be performed in-memory. The same cannot be said for shuffles. When we 
perform a shuffle, Spark writes the results to disk.

To trigger the computation, we run an action. There are three kinds of actions:
* Actions to view data in the console
* Actions to collect data to native objects in the respective language
* Actions to write to output data sources

## Chapter 4. Structured API Overview
The Structured APIs are a tool for manipulating all sorts of data, from unstructured log files to 
semi-structured CSV files and highly structured Parquet files. These APIs refer to three core types 
of distributed collection APIs:
* Datasets
* DataFrames
* SQL tables and views

the majority of the Structured APIs apply to both batch and streaming computation.

Spark is a distributed programming model in which the user specifies transformations. Multiple 
transformations build up a directed acyclic graph of instructions. An action begins the process of 
executing that graph of instructions, as a single job, by breaking it down into stages and tasks to 
execute across the cluster. The logical structures that we manipulate with transformations and 
actions are DataFrames and Datasets. To create a new DataFrame or Dataset, you call a 
transformation. To start computation or convert to native language types, you call an action.

To Spark, DataFrames and Datasets represent immutable, lazily evaluated plans that specify what 
operations to apply to data residing at a location to generate some output. When we perform an 
action on a DataFrame, we instruct Spark to perform the actual transformations and return the 
result. These represent plans of how to manipulate rows and columns to compute the user’s desired 
result.

Tables and views are basically the same thing as DataFrames. We just execute SQL against them 
instead of DataFrame code.

A schema defines the column names and types of a DataFrame. 
* You can define schemas manually 
* or read a schema from a data source (often called schema on read). 

Spark is effectively a programming language of its own. Internally, Spark uses an engine called 
Catalyst that maintains its own type information through the planning and processing of work. In 
doing so, this opens up a wide variety of execution optimizations that make significant differences. 
Spark types map directly to the different language APIs that Spark maintains and there exists a 
lookup table for each of these in Scala, Java, Python, SQL, and R. Even if we use Spark’s Structured 
APIs from Python or R, the majority of our manipulations will operate strictly on Spark types, not 
Python types.

DataFrames Versus Datasets.

In essence, within the Structured APIs, there are two more APIs, the “untyped” DataFrames and the 
“typed” Datasets. To say that DataFrames are untyped is as lightly inaccurate; they have types, but 
Spark maintains them completely and only checks whether those types line up to those specified in 
the schema at runtime. Datasets, on the other hand, check whether types conform to the specification 
at compile time. Datasets are only available to Java Virtual Machine (JVM)–based languages (Scala 
and Java) and we specify types with case classes or Java beans.

For the most part, you’re likely to work with DataFrames. To Spark (in Scala), DataFrames are simply 
Datasets of Type Row. The “Row” type is Spark’s internal representation of its optimized in-memory 
format for computation. This format makes for highly specialized and efficient computation because 
rather than using JVM types, which can cause high garbage-collection and object instantiation costs, 
Spark can operate on its own internal format without incurring any of those costs. To Spark (in 
Python or R), there is no such thing as a Dataset: everything is a DataFrame and therefore we always 
operate on that optimized format.

there are some excellent talks by Josh Rosen and Herman van Hovell:
* Deep Dive into Project Tungsten Bringing Spark Closer to Bare Metal -Josh Rosen (Databricks)
* A Deep Dive into the Catalyst Optimizer (Herman van Hovell)

## Chapter 10. Spark SQL


## Chapter 15. How Spark Runs on a Cluster
The Spark driver. The driver is the process “in the driver seat” of your Spark Application. It is 
the controller of the execution of a Spark Application and maintains all of the state of the Spark 
cluster.

An execution mode gives you the power to determine where the aforementioned resources are physically 
located when you go to run your application. You have three modes to choose from:
* Cluster mode
* Client mode
* Local mode

Client mode. we are running the Spark Application from a machine that is not colocated on the 
cluster. These machines are commonly referred to as gateway machines or edge nodes.

Local mode is a significant departure from the previous two modes: it runs the entire Spark 
Application on a single machine.

Each application is made up of one or more Spark jobs. Spark jobs within an application are executed 
serially (unless you use threading to launch multiple actions in parallel).

A SparkContext object within the SparkSession represents the connection to the Spark cluster. This 
class is how you communicate with some of Spark’s lower-level APIs, such as RDDs. Through a 
SparkContext, you can create RDDs, accumulators, and broadcast variables, and you can run code on 
the cluster. 

`SparkContext.getOrCreate()`

As a historical point, Spark 1.X had effectively two contexts. The SparkContext and the SQLContext. 
In Spark 2.X, the community combined the two APIs into the centralized SparkSession that we have 
today. It is important to note that you should never need to use the SQLContext and rarely need to 
use the SparkContext.

In general, there should be one Spark job for one action. Actions always return results. Each job 
breaks down into a series of stages, the number of which depends on how many shuffle operations need 
to take place.

A shuffle represents a physical repartitioning of the data.

By default when you create a DataFrame with range, it has eight partitions.

The spark.sql.shuffle.partitions default value is 200, which means that when there is a shuffle 
performed during execution, it outputs 200 shuffle partitions by default.

One of the key optimizations that Spark performs is pipelining, which occurs at and below the RDD 
level. With pipelining, any sequence of operations that feed data directly into each other, without 
needing to move it across nodes, is collapsed into a single stage of tasks that do all the 
operations together.

Shuffle persistence. Spark always executes shuffles by first having the “source” tasks (those 
sending data) write shuffle files to their local disks during their execution stage. Then, the stage 
that does the grouping and reduction launches and runs tasks that fetch their corresponding records 
from each shuffle file and performs that computation (e.g., fetches and processes the data for a 
specific range of keys).

One side effect you’ll see for shuffle persistence is that running a new job over data that’s 
already been shuffled does not rerun the “source” side of the shuffle. In the Spark UI and logs, you 
will see the pre-shuffle stages marked as “skipped”. You run some Spark actions on aggregated data 
and inspect them in the UI.

## Chapter 18. Monitoring and Debugging
The Monitoring Landscape. At some point, you’ll need to monitor your Spark jobs to understand where 
issues are occurring in them. It’s worth reviewing the different things that we can actually monitor 
and outlining some of the options for doing so.

* Spark Applications and Jobs
  * Spark UI
  * Spark logs
* JVM
  * JVM utilities such as jstack for providing stack traces, jmap for creating heap-dumps, jstat for 
    reporting time–series statistics, and jconsole for visually exploring various JVM properties are 
    useful for those comfortable with JVM internals. You can also use a tool like jvisualvm to help 
    profile Spark jobs.
  * Some of this information is provided in the Spark UI, but for very low-level debugging, the 
    aforementioned tools can come in handy.
* OS/Machine
  * The JVMs run on a host operating system (OS) and it’s important to monitor the state of those 
    machines to ensure that they are healthy. This includes monitoring things like CPU, network, and 
    I/O. These are often reported in cluster-level monitoring solutions; however, there are more 
    specific tools that you can use, including dstat, iostat, and iotop.
* Cluster
  * Some popular cluster-level monitoring tools include Ganglia and Prometheus.

What to Monitor. After that brief tour of the monitoring landscape, let’s discuss how we can go 
about monitoring and debugging our Spark Applications. There are two main things you will want to 
monitor: the processes running your application (at the level of CPU usage, memory usage, etc.), and 
the query execution inside it (e.g., jobs and tasks).

If you could monitor only one machine or a single JVM, it would definitely be the driver. With that 
being said, understanding the state of the executors is also extremely important for monitoring 
individual Spark jobs. To help with this challenge, Spark has a configurable metrics system based on 
the Dropwizard Metrics Library. These metrics can be output to a variety of different sinks, 
including cluster monitoring solutions like Ganglia.

Although the driver and executor processes are important to monitor, sometimes you need to debug 
what’s going on at the level of a specific query. Spark provides the ability to dive into queries, 
jobs, stages, and tasks. When looking for performance tuning or debugging, this is where you are 
most likely to start. 

the two most common ways of doing so: the Spark logs and the Spark UI.

The logs themselves will be printed to standard error when running a local mode application, or 
saved to files by your cluster manager when running Spark on a cluster. Refer to each cluster 
manager’s documentation about how to find them—typically, they are available through the cluster 
manager’s web UI.

The Spark UI provides a visual way to monitor applications while they are running as well as metrics 
about your Spark workload, at the Spark and JVM level. Every SparkContext running launches a web UI.
Cluster managers will also link to each application’s web UI from their own UI.

Spark REST API. In addition to the Spark UI, you can also access Spark’s status and metrics via a 
REST API. This is is available at http://localhost:4040/api/v1 and is a way of building 
visualizations and monitoring tools on top of Spark itself. For the most part this API exposes the 
same information presented in the web UI, except that it doesn’t include any of the SQL-related 
information. This can be a useful tool if you would like to build your own reporting solution based 
on the information available in the Spark UI.

Normally, the Spark UI is only available while a SparkContext is running, so how can you get to it 
after your application crashes or ends? To do this, Spark includes a tool called the Spark History 
Server that allows you to reconstruct the Spark UI and REST API, provided that the application was 
configured to save an event log. 

There are many issues that may affect Spark jobs, so it’s impossible to cover everything. But we 
will discuss some of the more common Spark issues you may encounter. In addition to the signs and 
symptoms, we’ll also look at some potential treatments for these issues. Most of the recommendations 
about fixing issues refer to the configuration tools discussed in Chapter 16.

**Spark Jobs Not Starting, Errors Before Execution**

* Ensure that machines can communicate with one another on the ports that you expect. Ideally, you 
  should open up all ports between the worker nodes unless you have more stringent security constraints.
* Ensure that your Spark resource configurations are correct and that your cluster manager is 
  properly set up for Spark.

**Errors During Execution**

* providing the wrong input file path or field name.
* Check to see if your data exists
* analysis error while planning the query
* Spark will show you the exception thrown by your code
* you can also view the logs on that machine to understand what it was doing when it failed.

**Slow Tasks or Stragglers**. This issue is quite common when optimizing applications, and can occur 
either due to work not being evenly distributed across your machines (“skew”), or due to one of your 
machines being slower than the others (e.g., due to a hardware problem).

* Try increasing the number of partitions to have less data per partition.
* Try repartitioning by another combination of columns. For example, stragglers can come up when you 
  partition by a skewed ID column, or a column where many values are null. In the latter case, it 
  might make sense to first filter out the null values.
* Try increasing the memory allocated to your executors if possible.
* Turning on speculation. This can be helpful if the issue is due to a faulty node because the task 
  will get to run on a faster one. Speculation does come at a cost, however, because it consumes 
  additional resources. In addition, for some storage systems that use eventual consistency, you 
  could end up with duplicate output data if your writes are not idempotent.
* If this issue is associated with a join or an aggregation, see “Slow Joins” or “Slow Aggregations”.
* Check whether your user-defined functions (UDFs) are wasteful in their object allocation or 
  business logic. Try to convert them to DataFrame code if possible.
* Ensure that your UDFs or User-Defined Aggregate Functions (UDAFs) are running on a small enough 
  batch of data. Oftentimes an aggregation can pull a lot of data into memory for a common key, 
  leading to that executor having to do a lot more work than others.
* Another common issue can arise when you’re working with Datasets. Because Datasets perform a lot 
  of object instantiation to convert records to Java objects for UDFs, they can cause a lot of 
  garbage collection. If you’re using Datasets, look at the garbage collection metrics in the Spark 
  UI to see if they’re consistent with the slow tasks.


**Slow Aggregations**

* Sometimes, the data in your job just has some skewed keys, and the operation you want to run on 
  them needs to be slow.
* Ensure null values are represented correctly (using Spark’s concept of null) and not as some 
  default value like " " or "EMPTY". Spark often optimizes for skipping nulls early in the job when 
  possible, but it can’t do so for your own placeholder values.
* Some aggregation functions are also just inherently slower than others. For instance, collect_list 
  and collect_set are very slow aggregation functions because they must return all the matching 
  objects to the driver, and should be avoided in performance-critical code.

**Slow Joins**. Joins and aggregations are both shuffles, so they share some of the same general symptoms as well as 
treatments.
* Many joins can be optimized (manually or automatically) to other types of joins.
* Experimenting with different join orderings can really help speed up jobs, especially if some of 
  those joins filter out a large amount of data; do those first.
* Slow joins can also be caused by data skew.
* Ensuring that all filters and select statements that can be are above the join can help to ensure 
  that you’re working only on the data that you need for the join.
* Ensure that null values are handled correctly (that you’re using null) and not some default value 
  like " " or "EMPTY", as with aggregations.

**Slow Reads and Writes**
* Turning on speculation
* Ensuring sufficient network connectivity
* For distributed file systems such as HDFS running on the same nodes as Spark, make sure Spark sees 
  the same hostnames for nodes as the file system. This will enable Spark to do locality-aware 
  scheduling, which you will be able to see in the “locality” column in the Spark UI.

**Driver OutOfMemoryError or Driver Unresponsive**
* Your code might have tried to collect an overly large dataset to the driver node using operations 
  such as collect.
* You might be using a broadcast join where the data to be broadcast is too big. Use Spark’s maximum 
  broadcast join configuration to better control the size it will broadcast.
* A long-running application generated a large number of objects on the driver and is unable to 
  release them.
* Increase the driver’s memory allocation if possible to let it work with more data.

**Executor OutOfMemoryError or Executor Unresponsive**
* Try increasing the memory available to executors and the number of executors.
* UDF
* Ensure that null values are handled correctly
* Datasets because of object instantiations

**Unexpected Nulls in Results**
* Most often, users will place the accumulator in a UDF when they are parsing their raw data into a 
  more controlled format and perform the counts there. This allows you to count valid and invalid 
  records and then operate accordingly after the fact.
* Ensure that your transformations actually result in valid query plans. Spark SQL sometimes does 
  implicit type coercions that can cause confusing results.

**No Space Left on Disk Errors**
* You see “no space left on disk” errors and your jobs fail.

**Serialization Errors**
* This often happens when you’re working with either some code or data that cannot be serialized 
  into a UDF or function, or if you’re working with strange data types that cannot be serialized. If 
  you are using (or intend to be using Kryo serialization), verify that you’re actually registering 
  your classes so that they are indeed serialized.
* Try not to refer to any fields of the enclosing object in your UDFs when creating UDFs inside a 
  Java or Scala class. This can cause Spark to try to serialize the whole enclosing object, which 
  may not be possible. Instead, copy the relevant fields to local variables in the same scope as 
  closure and use those.

As with debugging any complex software, we recommend taking a principled, step-by-step approach to 
debug issues. Add logging statements to figure out where your job is crashing and what type of data 
arrives at each stage, try to isolate the problem to the smallest piece of code possible, and work 
up from there. For data skew issues, which are unique to parallel computing.

## Chapter 19. Performance Tuning
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