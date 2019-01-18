# sbt notes


## popular plugins
### view dependency tree
project/plugins.sbt

```
addSbtPlugin("net.virtual-void" % "sbt-dependency-graph" % "0.8.2")
```

then `sbt dependencyTree`

## Troubleshooting

### corrupted Ivy 2 cache issue

```
[error] unresolved dependency: org.apache.zookeeper#zookeeper;3.4.6: several problems occurred while resolving dependency: org.apache.zookeeper#zookeeper;3.4.6 {compile=[compile(*), master(compile)], runtime=[runtime(*)]}:
[error] 	org.apache.zookeeper#zookeeper;3.4.6!zookeeper.pom(pom.original) origin location must be absolute: file:/Users/seanmao/.m2/repository/org/apache/zookeeper/zookeeper/3.4.6/zookeeper-3.4.6.pom
```

see similar issue: https://github.com/databricks/sbt-spark-package/issues/6

Apparently this would some sort of corrupted Ivy 2 cache issue, deleting the ~/.ivy2/ directory entirely and relaunching SBT resolved the problem

