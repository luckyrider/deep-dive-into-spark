# App Status

## Overview



## Design and Implementation

### Status overview
![status](status-overview.png)

Spark tracks app status using `AppStatusListener` and tracks SQL app status using
`SQLAppStatusListener`. These listeners write status finally into `KVStore`. On the other hand,
`AppStatusStore` and `SQLAppStatusStore` query `KVStore` to get app status.

### Live Entity
![livy entity](live-entity.png)

## Evolution
In Spark 2.1, Spark stores app status using listeners instead of `AppStatusStore`. And Spark tracks
SQL app status using `SQLListener` instead of `SQLAppStatusStore`.

![status (Spark 2.1)](status-2.1.png)
