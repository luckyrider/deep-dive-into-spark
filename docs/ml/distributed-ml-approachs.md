# Distributed Machine Learning Approaches

## Allreduce (or MPI) vs. Parameter server approaches
http://hunch.net/?p=151364

作者是John Langford, microsoft research.

总结来最近几年distributed machine learning approaches.包括：

* MPI gradient aggregation。主要问题：batch，所以比较慢；不适合Large datasets
* Map-Reduce statistical query algorithms。适合large datasets，但是慢
* Parameter averaging。只适用于convex learning。
* Graph-based approaches。通过图的切割，容易并行，问题是不少问题没法抽象成图。
* Parameter server approaches。解决参数单机存放不下的问题，还存在争议。
* Allreduce. 主要问题：poor performance under misbalanced loads
* GPU+MPI approaches

目前来看，哪种方法最好没有定论，需要看具体场景。

* 不要为了并行而并行。并发会带来复杂性，除非并发能带来实际的好处。
* 如果绑定到特定硬件或集群，没有选择，那就好好利用它，比如Hadoop。
* 如果数据单机能放得下，那单机上跑GPU效果应该不错。
* 如果数据必须放在多台机器上，那么优先考虑
  * Graph-based approaches
  * Allreduce-based approaches

从作者的观点来看，偏向allreduce。认为parameter server存在争议。

## Parameter Server Approach

### Overview
参数服务器对于spark而言，不是replace的关系，而是augment的关系。

* SPARK-4590, Early investigation of parameter server. https://issues.apache.org/jira/browse/SPARK-4590
* SPARK-6932, A Prototype of Parameter Server, 原来阿里的明风提出来的. https://issues.apache.org/jira/browse/SPARK-6932
* SPARK-6932讨论中提到另一个原型：Glint. https://github.com/rjagerman/glint
* SPARK-6567, Large linear model parallelism via a join and reduceByKey. https://issues.apache.org/jira/browse/SPARK-6567
* yahoo's Spark+PS architecture，解决10亿以上大模型问题. https://spark-summit.org/2016/events/scaling-machine-learning-to-billions-of-parameters/
* 最近比较火的parameter server是什么？https://www.zhihu.com/question/26998075
* Parameter Server详解. http://blog.csdn.net/cyh_24/article/details/50545780
* 参数服务器——分布式机器学习的新杀器. http://www.toutiao.com/i6268606164368359938/

### dmlc/ps-lite

A lightweight parameter server interface

* https://github.com/dmlc/ps-lite

## Allreduce

### Overview
hadoop/spark做的是MapReduce abstraction，graphlab做graph parallel，MPI提供的是Allreduce/Broadcast，PS提供的是异步的更新。

同步的Allreduce和异步的PS抽象会是高效机器学习算法最常用的两个抽象，越来越多地出现在以机器学习为中心的分布式平台中

* Reduce, Broadcast and AllReduce. http://www.udpwork.com/item/15791.html
* rabit作者陈天奇谈allreduce和rabit。http://weibo.com/p/1001603801281637563132
* http://stackoverflow.com/questions/34078430/treereduce-vs-reducebykey-in-spark
* http://stackoverflow.com/questions/32281417/understadning-treereduce-in-spark

### dmlc/rabit

Reliable Allreduce and Broadcast Interface for distributed machine learning

* https://github.com/dmlc/rabit



