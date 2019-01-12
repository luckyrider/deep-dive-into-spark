# Hive Query Language

## Overview
https://cwiki.apache.org/confluence/display/Hive/LanguageManual


## Windowing and Analytics

Spark SQL 2.0.2可以跑过:

```
select * from (
select u.*, row_number() over (partition by first_name order by last_name desc) as rn from user u
) where rn =1;

select * from (
select u.*, row_number() over (distribute by first_name sort by last_name desc) as rn from user u
) where rn =1;
```

* https://cwiki.apache.org/confluence/display/Hive/LanguageManual+WindowingAndAnalytics
* http://stackoverflow.com/questions/26009059/finding-the-first-row-in-a-group-using-hive
