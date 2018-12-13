# Spark App Troubleshooting

## Overview
* Data Modeling
* ANSI SQL support: subquery, built-in functions
* Hive compatibility (bucket, UDF)
* Spark on YARN
* OOM (more partitions, raise memoryOverhead)
* I18N: character set
* Deal with NULLs
* shuffle issues, e.g. FetchFailedException
  * due to OOM
  * non-OOM
  spark.network.timeout=6000 // The default 120 seconds will cause a lot of your executors to time out when under heavy load.
  spark.reducer.maxReqsInFlight=1 // Only pull one file at a time to use full network bandwidth.
  spark.shuffle.io.retryWait=60s  // Increase the time to wait while retrieving shuffle partitions before retrying. Longer times are necessary for larger files.
  spark.shuffle.io.maxRetries=10
* Frequently Thrown Exceptions

## References

User:
* Dealing with null in Spark. https://medium.com/@mrpowers/dealing-with-null-in-spark-cfdbb12f231e
* FetchFailedException or MetadataFetchFailedException when processing big data set. https://stackoverflow.com/questions/34941410/fetchfailedexception-or-metadatafetchfailedexception-when-processing-big-data-se
* Spark Shuffle FetchFailedException解决方案. https://www.jianshu.com/p/edd3ccc46980

Deeper:
* Yin Huai. How Apache Spark can fail or be confusing and what you can do about it. https://cdn.oreillystatic.com/en/assets/1/event/193/How%20Spark%20can%20fail%20or%20be%20confusing%20and%20what%20you%20can%20do%20about%20it%20Presentation.pdf
* Reduce Apache Spark Troubleshooting Time from Days to Seconds. https://unraveldata.com/automated-root-cause-analysis-spark-application-failures-reducing-troubleshooting-time-days-seconds/



