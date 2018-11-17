
how is `spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version` passed to Hadoop?

`org/apache/hadoop/mapreduce/lib/output/FileOutputCommitter.java`


what is `mapreduce.fileoutputcommitter.algorithm.version`?

https://hadoop.apache.org/docs/r2.7.0/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml

> The file output committer algorithm version, valid algorithm version number: 1 or 2, default to 1, which is the original algorithm 
>
> In algorithm version 
> 1. commitTask will rename directory $joboutput/_temporary/$appAttemptID/_temporary/$taskAttemptID/ to $joboutput/_temporary/$appAttemptID/$taskID/ 
> 2. recoverTask will also do a rename $joboutput/_temporary/$appAttemptID/$taskID/ to $joboutput/_temporary/($appAttemptID + 1)/$taskID/ 
> 3. commitJob will merge every task output file in $joboutput/_temporary/$appAttemptID/$taskID/ to $joboutput/, then it will delete $joboutput/_temporary/ and write $joboutput/_SUCCESS 
It has a performance regression, which is discussed in MAPREDUCE-4815. If a job generates many files to commit then the commitJob method call at the end of the job can take minutes. the commit is single-threaded and waits until all tasks have completed before commencing. 
>
> algorithm version 2 will change the behavior of commitTask, recoverTask, and commitJob. 
> 1. commitTask will rename all files in $joboutput/_temporary/$appAttemptID/_temporary/$taskAttemptID/ to $joboutput/ 
> 2. recoverTask actually doesn't require to do anything, but for upgrade from version 1 to version 2 case, it will check if there are any files in $joboutput/_temporary/($appAttemptID - 1)/$taskID/ and rename them to $joboutput/ 
> 3. commitJob can simply delete $joboutput/_temporary and write $joboutput/_SUCCESS 
This algorithm will reduce the output commit time for large jobs by having the tasks commit directly to the final output directory as they were completing and commitJob had very little to do.
