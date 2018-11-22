# Catalyst

## Overview
At the core of Spark SQL is the Catalyst optimizer.

At its core, Catalyst contains a general library for representing trees and applying rules to manipulate them. On top of this framework, we have built libraries specific to relational query processing (e.g., expressions, logical query plans), and several sets of rules that handle different phases of query execution: analysis, logical optimization, physical planning, and code generation to compile parts of queries to Java bytecode.

## References

* https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html

## Parser





## Analyzer




## Optimizer





## References:
* https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html
* A Deep Dive into Spark SQL's Catalyst Optimizer with Yin Huai. https://www.youtube.com/watch?v=RmUn5vHlevc
* https://virtuslab.com/blog/spark-sql-hood-part-i/
* https://blog.imaginea.com/spark-2-0-sql-source-code-tour-part-1-introduction-and-catalyst-query-parser/
* https://blog.imaginea.com/spark-2-0-sql-source-code-tour-part-2-catalyst-query-plan-transformation/
* https://blog.imaginea.com/spark-2-0-sql-source-code-tour-part-3-implicit-cast-is-evil/
* https://developer.ibm.com/code/2017/11/30/learn-extension-points-apache-spark-extend-spark-catalyst-optimizer/
* https://issues.apache.org/jira/browse/SPARK-18127