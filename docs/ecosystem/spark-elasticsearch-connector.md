# Spark Elasticsearch Connector

## Overview
* 版本：org.elasticsearch:elasticsearch-spark-20_2.11:5.1.1
* Spark跟ES的通信是基于REST的。elasticsearch-hadoop uses Elasticsearch REST interface for communication, allowing for flexible deployments by minimizing the number of ports needed to be open within a network.
* HTTP端口配置无法动态修改，需要重启。The settings in the table below can be configured for HTTP. Note that none of them are dynamically updatable so for them to take effect they should be set in elasticsearch.yml.
* ES节点分为master, data, client等几种。spark executor写client node或是data node，有利有弊，后续看实际情况调整。
* Spark读写的并发度，跟ES的shard数量一致。
* 支持filter/projection的pushdown。目前不支持aggregation的pushdown。
* 如果指定了es.mapping.id，Spark SQL的insert = ES的upsert
* 通过rename alias，可以无缝切换最新的index上线使用

## Configuration
All configuration properties start with the es prefix. 包括：

* es.nodes
* es.port
* es.nodes.discovery (default true)
* es.nodes.client.only (default false)
* es.nodes.data.only (default true)
* es.write.operation (default index)
* es.mapping.id

## References
Flume + ES

* https://flume.apache.org/FlumeUserGuide.html#elasticsearchsink

Spark + ES

* https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html
* https://www.elastic.co/guide/en/elasticsearch/hadoop/current/arch.html
* https://www.elastic.co/guide/en/elasticsearch/hadoop/current/configuration.html
* 目前不支持aggregation pushdown. https://github.com/elastic/elasticsearch-hadoop/issues/867

ES

* https://www.elastic.co/guide/en/elasticsearch/reference/5.1/modules-http.html
* https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html
* https://www.elastic.co/guide/en/elasticsearch/guide/current/_talking_to_elasticsearch.html
* https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html
* https://www.elastic.co/blog/changing-mapping-with-zero-downtime
