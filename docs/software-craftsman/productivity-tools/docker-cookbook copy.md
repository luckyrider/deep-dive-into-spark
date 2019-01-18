# Docker Cookbook

## Overview
* basic concepts
* architecture
* underpinning techniques
* CLI

## Basic Concepts
* image: template of containers. build.
* registry: library of images. distribution.
* container: run.
* service: scalability.
* Docker for Mac/Docker Tools: portability.

Docker for Mac vs Docker tools
* Docker for Mac = Xhyve + Alpine + docker engine = for newer version mac
* Docker Tools includes Docker Machine = VirtualBox + boot2docker + engine = for older version mac

## Architecture
client-server

client <-> daemon <-> container

## Underpinning Techniques
* namespaces
* control groups
* union file systems
* container format: libcontainer

## CLI

### manage images

```
docker pull <image>
docker images
```

You may create a docker image:

* from an existing container

```
docker commit <container> <image>
```

* from a Dockerfile

```
docker build -t <image> <Dockerfile dir>
```


### manage containers

```
docker ps
docker ps -a
docker exec -it <container> bash
docker [start|stop] <container>
```

### network

```
docker network ls
docker network inspect <network>
docker network connect <network> <container>
docker network disconnect <network> <container>
```

### manage data

* data volume
* data volume container

