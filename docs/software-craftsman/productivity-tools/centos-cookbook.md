# CentOS Cookbook

## Overview

* System Admin


## System Admin

### Hardware
查看内存：

```
cat /etc/meminfo
```

查看逻辑CPU的个数。逻辑CPU数量=物理cpu数量 x cpu cores 这个规格值 x 2(如果支持并开启ht，即超线程技术) :

```
cat /proc/cpuinfo |grep "processor"|wc -l
```

查看CPU是几核:

```
cat /proc/cpuinfo |grep "cores"|uniq
```

### 时区一致

```
sudo cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

### 新建用户

```
sudo useradd admin
sudo passwd admin
123456
sudo vi /etc/sudoers.d/admin
%admin ALL=(ALL) NOPASSWD: ALL
```

### systemd
Running systemd within docker container. 

Issue:

```
Failed to get D-Bus connection: Operation not permitted
```

Solution:

```
--privileged
```

Reference:
* https://developers.redhat.com/blog/2014/05/05/running-systemd-within-docker-container/
* https://hub.docker.com/_/centos/
