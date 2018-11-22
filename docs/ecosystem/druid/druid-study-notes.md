# Druid Study Notes

## Quickstart


References:

* http://druid.io/docs/0.9.1.1/tutorials/quickstart.html

## Design


Reference:

* http://druid.io/docs/0.9.1.1/design/index.html
* http://druid.io/docs/0.9.1.1/design/design.html
* Druid whitepaper: http://static.druid.io/docs/druid.pdf

## Case Study & Best Practice

* 基于Druid和Drill的OLAP引擎. 阿里巴巴. http://strata.oreilly.com.cn/hadoop-big-data-cn/hadoop-big-data-cn/public/schedule/detail/52345
* Druid在OneAPM的大数据分析实践. http://chinahadoop.com/archives/1965

## Sourcecode

### Build from Source
http://druid.io/docs/latest/development/build.html

```
git clone https://github.com/druid-io/druid.git
cd druid
git checkout druid-0.9.1.1
mvn clean package -DskipTests
```

## Misc

### Exact count distinct
How to do a exact count distinct aggregation? https://groups.google.com/forum/#!msg/druid-development/AMSOVGx5PhQ/oqdMtHOHeKUJ

* I just do a groupBy based on the dim on a single metric. The size of array returned is the exact count.
* One other option is to look at the segment metadata query: http://druid.io/docs/latest/SegmentMetadataQuery.html. It'll return the exact cardinality of columns for segments within an interval. It'll probably be faster than groupBy but requires summing cardinality values client side. This method will work for a single segment, but not for a query that spans multiple segments. We should at some point built a native exact cardinality aggregator. The approximate cardinality estimator is an aggregator and is there to avoid ingesting columns that can potentially ruin your rollup and vastly increase your data size.
* One other option that may potentially be faster and less resource intensive for a single dimension is to do a lexicographic topN (http://druid.io/docs/0.6.158/TopNMetricSpec.html), which supports pagination, and sum the size of the total result set.
* Thank you, a native exact cardinality aggregator may be the best solution. Durid can use a aggregator to store cardinality in a compressed bitmap with (dimension name, dimension value), and then use bit operator to do bool filter.  it will be fast enough. like this: http://radar.oreilly.com/2009/11/real-time-unique-user-count-with-streaming-databases.html

References:

* http://radar.oreilly.com/2009/11/real-time-unique-user-count-with-streaming-databases.html
* http://highscalability.com/blog/2012/4/5/big-data-counting-how-to-count-a-billion-distinct-objects-us.html
