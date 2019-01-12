# Cassandra Batch

summary:

* batch的主要好处是保证atomicity，而不是performance。
* 最快的方式是不用batch。

exerpts:

> Using a batch statement is not a good way to optimize performance — for details, see Using and misusing batches. For a discussion about the fastest way to load data, see Cassandra: Batch loading without the Batch keyword. Instead, using a batch is a good way to synchronize data to tables.

> Although a logged batch enforces atomicity (that is, it guarantees if all DML statements in the batch succeed or none do), Cassandra does no other transactional enforcement at the batch level.

> Fastest option no batch.

> Multi partition batches should only be used to achieve atomicity for a few writes on different tables. Apart from this they should be avoided because they’re too expensive. Single partition batches can be used to get atomicity + isolation, they’re not much more expensive than normal writes.

> When you’re writing to multiple partitions you should prefer multiple async writes.

> The proposal is to ignore size on single partition batch statements. (CASSANDRA-10876, Fix Version/s: 3.6)

> For single partition batches there’s no batch log and no ceremony involved and they’re atomic and isolated.

配置。最好不要改动默认值，可能引起节点不稳定。

```
batch_size_warn_threshold_in_kb 
(Default: 5KB per batch) Causes Cassandra to log a WARN message when any batch size exceeds this value in kilobytes.
CAUTION:
Increasing this threshold can lead to node instability.
batch_size_fail_threshold_in_kb 
(Default: 50KB per batch) Cassandra fails any batch whose size exceeds this setting. The default value is 10X the value of batch_size_warn_threshold_in_kb.
```


references:

* https://docs.datastax.com/en/cql/3.3/cql/cql_reference/batch_r.html
* https://docs.datastax.com/en/cql/3.3/cql/cql_using/useBatch.html
* https://lostechies.com/ryansvihla/2014/08/28/cassandra-batch-loading-without-the-batch-keyword/
* https://lostechies.com/ryansvihla/2016/04/29/cassandra-batch-loading-without-the-batch%E2%80%8A-%E2%80%8Athe-nuanced-edition/
* https://inoio.de/blog/2016/01/13/cassandra-to-batch-or-not-to-batch/
* http://christopher-batey.blogspot.de/2015/03/cassandra-anti-pattern-cassandra-logged.html
* https://issues.apache.org/jira/browse/CASSANDRA-10876
