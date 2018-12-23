# Scheduler

## Overview


## Design and Implementation

### RDD
`RDD`:

![RDD](rdd.png)

`Partition`:

![Partition](Partition.png)

`Dependency`:

![Dependency](Dependency.png)

`Partitioner`:

![Partitioner](Partitioner.png)

### Scheduler overview

`DAGScheduler`, `TaskScheduler` and `SchedulerBackend`:

![Scheduler](scheduler-overview.png)

The interaction when an RDD action is invoked:

![RDD action scheduler sequence](rdd-action-scheduler-sequence.png)


### DAGScheduler

![DAGScheduler](DAGScheduler.png)


### TaskScheduler and SchedulerBackend

![TaskScheduler and SchedulerBackend](TaskScheduler&SchedulerBackend.png)

## Evolution


## References

* https://en.wikipedia.org/wiki/Event_loop
