# filodb study notes

## Quick start
create dataset via filo-cli:

```
./filo-cli --command create --dataset gdelt --columns GLOBALEVENTID:int,SQLDATE:string,MonthYear:int,Year:int,FractionDate:double,Actor1Code:string,Actor1Name:string,Actor1CountryCode:string,Actor1KnownGroupCode:string,Actor1EthnicCode:string,Actor1Religion1Code:string,Actor1Religion2Code:string,Actor1Type1Code:string,Actor1Type2Code:string,Actor1Type3Code:string,Actor2Code:string,Actor2Name:string,Actor2CountryCode:string,Actor2KnownGroupCode:string,Actor2EthnicCode:string,Actor2Religion1Code:string,Actor2Religion2Code:string,Actor2Type1Code:string,Actor2Type2Code:string,Actor2Type3Code:string,IsRootEvent:int,EventCode:string,EventBaseCode:string,EventRootCode:string,QuadClass:int,GoldsteinScale:double,NumMentions:int,NumSources:int,NumArticles:int,AvgTone:double,Actor1Geo_Type:int,Actor1Geo_FullName:string,Actor1Geo_CountryCode:string,Actor1Geo_ADM1Code:string,Actor1Geo_Lat:double,Actor1Geo_Long:double,Actor1Geo_FeatureID:int,Actor2Geo_Type:int,Actor2Geo_FullName:string,Actor2Geo_CountryCode:string,Actor2Geo_ADM1Code:string,Actor2Geo_Lat:double,Actor2Geo_Long:double,Actor2Geo_FeatureID:int,ActionGeo_Type:int,ActionGeo_FullName:string,ActionGeo_CountryCode:string,ActionGeo_ADM1Code:string,ActionGeo_Lat:double,ActionGeo_Long:double,ActionGeo_FeatureID:int,DATEADDED:string,Actor1Geo_FullLocation:string,Actor2Geo_FullLocation:string,ActionGeo_FullLocation:string --rowKeys GLOBALEVENTID --segmentKey ':string 0'
```

local mode:

```
bin/spark-shell --jars /Users/seanmao/dataplatform/FiloDB/spark/target/scala-2.10/filodb-spark-assembly-0.3.jar --packages com.databricks:spark-csv_2.10:1.2.0 --driver-memory 3G --executor-memory 3G
```

standalone:

```
bin/spark-shell --master spark://10.101.50.246:7077 --jars $DATAPLATFORM/filodb/lib/filodb-spark-assembly-0.4-SNAPSHOT.jar --packages com.databricks:spark-csv_2.10:1.2.0 
```

load dataset:

```
val csvDF = sqlContext.read.format("com.databricks.spark.csv").
           option("header", "true").option("inferSchema", "true").
           load("/Users/seanmao/dataplatform/filodb/resource/GDELT-1979-1984-100000.csv");
```

create dataset via spark DataFrame:

```
import org.apache.spark.sql.SaveMode;
csvDF.write.format("filodb.spark").
             option("dataset", "gdelt").
             option("row_keys", "GLOBALEVENTID").
             option("segment_key", ":round GLOBALEVENTID 10000").
             option("partition_keys", ":getOrElse MonthYear -1").
             mode(SaveMode.Overwrite).save();
```

You can also query filoDB tables using Spark thrift server:

```

```
