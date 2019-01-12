# Hive Configuration

## Overview



## file size
hive中默认的hive.input.format是org.apache.hadoop.hive.ql.io.CombineHiveInputFormat。对于CombineHiveInputFormat，map数由三个配置决定
* mapred.min.split.size.per.node: 一个node上split的最小值
* mapred.min.split.size.per.rack: 一个rack上split的最小值
* mapred.max.split.size: 一个split最大值

为了防止job结果小文件太多，可以启动额外的job来合并结果小文件。
* hive.merge.smallfiles.avgsize

