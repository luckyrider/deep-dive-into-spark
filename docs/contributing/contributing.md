# Contributing
## Overview
http://spark.apache.org/contributing.html

## Development Tools

### code style
* checkstyle

### build
* maven
* sbt

### CI
* Jenkins

## Coding Style
https://github.com/databricks/scala-style-guide

## Coding Skills

### SparkFirehoseListener

This is a concrete Java class in order to ensure that we don't forget to update it when adding new methods to SparkListener: forgetting to add a method will result in a compilation error (if this was a concrete Scala class, default implementations of new event handlers would be inherited from the SparkListener trait).

## Community

* https://projects.apache.org/committee.html?spark
* http://spark.apache.org/committers.html
