# Machine Learning Platform Overview

## 算法平台及应用情况
* 算法平台架构与应用 On MaxCompute. http://download.csdn.net/meeting/speech_preview/297
* 百度大规模推荐系统实践. http://download.csdn.net/meeting/speech_preview/343
* 360聚效广告大数据平台实践. http://download.csdn.net/meeting/speech_preview/341
* 搜狐基于Spark的新闻和广告推荐实战. http://www.csdn.net/article/2015-07-31/2825353
* 今日头条的人工智能技术实践. http://download.csdn.net/meeting/speech_preview/288
* 基于图算法的跨设备受众识别. Admaster. http://download.csdn.net/meeting/speech_preview/342
* 携程Spark算法平台及其应用. http://download.csdn.net/meeting/speech_preview/313
* 深度学习在搜狗无线搜索广告中的应用. http://www.infoq.com/cn/news/2016/08/sougou-deep-learing-wireless-sea

## 常用算法

## https://www.zhihu.com/question/37970802

```
阿里巴巴：LR，MLR，GBDT
百度：LR，GBDT，DNN
360：LR，FM探索中
腾讯据我所知线上主要是LR+GBDR，线下探索DNN+FTRL
```

```
CTR预估模型主要是两类：
1. 线性模型 或 层数较少的非线性模型(比如：LR, SVM, FM) + 大量特征提取、特征离散化、特征组合
2. 深层非线性模型(比如：NN) + 少量连续特征 + 大量调参
```

```
算法基本就是常用优化算法的分布式版本。
LR: 简单，可解释性好，便于debug
MLR: Mixed Logistic Regression
GBDT
FM(Factorization Machines): 解决categorical feature One Hot Encoding带来的特征稀疏问题
NN/DNN
FTRL: Proximal—Follow-the-regularized-leader，在线学习
```

```
现在主流的肯定还是lr+gbdt，但是也有开始研究gbdt＋fm的了。细节的各种算法也是有在用的。
现在各大互联网大厂建模都是依赖于spark平台，如搜狗，搜狐，58赶集集团，美团等
为什么呢，因为Spark Mllib 实现了lr,gbdt,spark JIRA实现了fm等(这个不知道现在发布没）
```
