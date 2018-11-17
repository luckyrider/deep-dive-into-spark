# The Year in Machine Learning

四部分

* https://thomaswdinsmore.com/2016/12/19/the-year-in-machine-learning-part-one/
* https://thomaswdinsmore.com/2017/01/02/the-year-in-machine-learning-part-two/
* https://thomaswdinsmore.com/2017/01/09/the-year-in-machine-learning-part-three/
* https://thomaswdinsmore.com/2017/01/16/the-year-in-machine-learning-part-four/

语言和API

* R和Python依然是数据科学家最喜欢的语言和平台
* Python成为越来越多框架的API，包括Spark、TensorFlow，H2O，Theano等等。

Apache的机器学习项目(TPL或incubator)

* Spark：MLlib
* Flink：主要优势在流式处理，ML方面还比较弱
* SystemML：开发比较活跃，2017年很有可能成为TPL，VLDB 2016 best paper，目前最大的问题是IBM之外的人很少用。
* PredictionIO：Salesforce收购并捐赠给了Apache，上一个版本发布于2016年4月，开发不活跃，Salesforce投入不多。
* MADLib：Pivotal捐赠给Apache，Big Data Machine Learning in SQL，运行在PostgreSQL,Greenplum,HAWQ上，根据MADLib团队的survey，目前主要用于Greenplum上。
* SINGA：新加坡国立大学捐赠给Apache，distributed deep learning。
* Hivemall：非常新的项目，基于HIVE UDF的ML，支持Hive，Spark，Pig等。team member阵容强大。
* SAMOA：基本上die
* Mahout: 式微

其他的开源ML项目：
* H2O：在国外好像挺火的，但在Spark社区似乎影响力不大
* XGBoost：颇受顶尖数据科学家的欢迎，越来越流行
* Weka：式微

深度学习框架

* TensorFlow(Google), MXNet(Amazon), CNTK(Microsoft)新的领导者，渐渐超越老牌的Caffe、Torch、DL4J等
* 在Python社区，Keras和Theano非常受欢迎
* TF, CNTK, Theano 将NN表示成图模型
* 性能提升：GPU vs FPGA
