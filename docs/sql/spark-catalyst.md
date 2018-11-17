# Spark Catalyst

## Overview
At the core of Spark SQL is the Catalyst optimizer.

At its core, Catalyst contains a general library for representing trees and applying rules to manipulate them. On top of this framework, we have built libraries specific to relational query processing (e.g., expressions, logical query plans), and several sets of rules that handle different phases of query execution: analysis, logical optimization, physical planning, and code generation to compile parts of queries to Java bytecode.

## References

* https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html