# Scheduler

## Overview


## Design and Implementation

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

