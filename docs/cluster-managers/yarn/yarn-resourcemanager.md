# YARN ResourceManager

## Overview

* http://hadoop.apache.org/docs/r2.7.3/hadoop-yarn/hadoop-yarn-site/ResourceManagerRestart.html
* http://hadoop.apache.org/docs/r2.7.3/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html

## Restart

Phase 1: Non-work-preserving RM restart. As of Hadoop 2.4.0 release, only ResourceManager Restart Phase 1 is implemented

Phase 2: Work-preserving RM restart. As of Hadoop 2.6.0, we further enhanced RM restart feature to address the problem to not kill any applications running on YARN cluster if RM restarts.

## HA

