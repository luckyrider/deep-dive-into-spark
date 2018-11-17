# Spark Parameter Server

## Overview

* spark+ps的方案，解决大规模参数（千万以上）是可行的
* 基于spark来开发ps，是可行的
* ps的开发，可以基于社区已有的原型来做，比从零开始容易得多
* ps很关键，了解其原理非常有必要
 
参数服务器对于spark而言，不是replace的关系，而是augment的关系。
* SPARK-4590, Early investigation of parameter server. https://issues.apache.org/jira/browse/SPARK-4590
* SPARK-6932, A Prototype of Parameter Server, 原来阿里的明风提出来的. https://issues.apache.org/jira/browse/SPARK-6932
* SPARK-6932讨论中提到另一个原型：Glint. https://github.com/rjagerman/glint
* SPARK-6567, Large linear model parallelism via a join and reduceByKey. https://issues.apache.org/jira/browse/SPARK-6567
* yahoo's Spark+PS architecture，解决10亿以上大模型问题. https://spark-summit.org/2016/events/scaling-machine-learning-to-billions-of-parameters/
* 最近比较火的parameter server是什么？https://www.zhihu.com/question/26998075
* Parameter Server详解. http://blog.csdn.net/cyh_24/article/details/50545780
* 参数服务器——分布式机器学习的新杀器. http://www.toutiao.com/i6268606164368359938/
 
参考文档：
* yahoo-ps.pdf from slideshare
* parameter server review.pdf from SPARK-4590
* ps-muli.pdf
* factorbird.pdf
