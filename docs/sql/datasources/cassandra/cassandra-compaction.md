# Cassandra Compaction

## Overview

When Leveled Compaction is a Good Option:

* High Sensitivity to Read Latency
* High Read/Write Ratio
* Rows Are Frequently Updated

When Leveled Compaction may not be a Good Option:

* Your Disks Can’t Handle the Compaction I/O
* Write-heavy Workloads
* Rows Are Write-Once

References:

* http://docs.datastax.com/en/cassandra/3.x/cassandra/dml/dmlHowDataMaintain.html
* http://www.datastax.com/dev/blog/leveled-compaction-in-apache-cassandra
* http://www.datastax.com/dev/blog/when-to-use-leveled-compaction
* http://stackoverflow.com/questions/27862808/what-delays-a-tombstone-purge-when-using-lcs-in-cassandra
* https://blog.alteroot.org/articles/2015-04-20/change-cassandra-compaction-strategy-on-production-cluster.html
* http://cassandra.apache.org/doc/latest/operating/compaction.html
