# Spark on YARN
## Overview


## Design and Implementation

![spark on yarn](clustermanager.yarn.png)

key classes:
* org.apache.spark.deploy.yarn.ApplicationMaster
* org.apache.spark.deploy.yarn.ExecutorLauncher is merely a wrapper of ApplicationMaster. This object does not provide any special functionality. It exists so that it's easy to tell apart the client-mode AM from the cluster-mode AM when using tools such as ps or jps.

## FQA
### vcores

* https://stackoverflow.com/questions/38368985/spark-on-yarn-too-less-vcores-used
* https://stackoverflow.com/questions/25563736/yarn-is-not-honouring-yarn-nodemanager-resource-cpu-vcores/25570709#25570709
