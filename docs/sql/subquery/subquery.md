# Subquery

## Overview
Subquery support has been introduced in Spark 2.0. The initial implementation covers the most common subquery use case: the ones used in TPC queries for instance.

Spark currently supports the following subqueries:

* Uncorrelated Scalar Subqueries. All cases are supported.
* Correlated Scalar Subqueries. We only allow subqueries that are aggregated and use equality predicates.
* Predicate Subqueries. IN or Exists type of queries. We allow most predicates, except when they are pulled from under an Aggregate or Window operator. In that case we only support equality predicates.

However this does not cover the full range of possible subqueries. This, in part, has to do with the fact that we currently rewrite all correlated subqueries into a (LEFT/LEFT SEMI/LEFT ANTI) join.

We currently lack supports for the following use cases:

* The use of predicate subqueries in a projection.
* The use of non-equality predicates below Aggregates and or Window operators.
* The use of non-Aggregate subqueries for correlated scalar subqueries.

subquery related tickets.

* https://issues.apache.org/jira/browse/SPARK-18455
* https://issues.apache.org/jira/browse/SPARK-18863
* https://issues.apache.org/jira/browse/SPARK-19047
* https://issues.apache.org/jira/browse/SPARK-16161
