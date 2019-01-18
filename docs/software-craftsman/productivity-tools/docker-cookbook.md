# Docker Cookbook

## Overview
Docker for Mac
* https://docs.docker.com/docker-for-mac/

Get started
* https://docs.docker.com/get-started/

Architecture
* https://docs.docker.com/engine/docker-overview/

Guides and Reference
* https://docs.docker.com/

## Preferences
### /proc/meminfo MemTotal low
setting the preferences -> advance in the Docker Application

Reference:
* https://stackoverflow.com/questions/44806234/how-to-set-ram-memory-of-a-docker-container-by-terminal-or-dockerfile

## Manage Images

Pull an image

```
docker pull <image>
docker image pull <image>
```

List images

```
docker images
docker image ls -a
```

Create a docker image from a Dockerfile:

```
docker build -t <image tag> <Dockerfile dir>
```

Create a docker image from an existing container:

```
docker commit -c "EXPOSE 8088" <container> <image>
docker container commit  -c "EXPOSE 8088" <container> <image>
```

## Manage Containers

Create a new container:

```
docker container create <image>
```

List containers:

```
docker ps
docker ps -a
docker container ls
docker container ls -a
```

Start/Stop:

```
docker [start|stop] <container>
```

Attach to a running container:

```
docker container attach 
```

Run a command in a running container:

```
docker exec -it <container> bash
```

## Manage Network

```
docker network ls
docker network inspect <network>
docker network connect <network> <container>
docker network disconnect <network> <container>
```

## Manage Data


## Spark Ecosystem
```
docker run -itd --name master -v /opt/provision:/opt/provision dataplatformbase
docker run -itd --hostname slave01 --name slave01 -v /opt/provision:/opt/provision dataplatformbase
docker run -itd --hostname slave02 --name slave02 -v /opt/provision:/opt/provision dataplatformbase
```

```
docker run -itd --name <container_name> --hostname <container_hostname> -v <host_dir>:<guest_dir> <image>
```

```
# MySQL
guest: 3306,  host: 3307
# Zookeeper
guest: 2181,  host: 2181
# Hadoop
guest: 50070, host: 50070 # NameNode WebUI
guest: 8020,  host: 8020  # NameNode RPC
guest: 50075, host: 50075 # DataNode WebUI
guest: 50020, host: 50020 # DataNode RPC
guest: 50010, host: 50010 # DataNode Data Transfer
guest: 8088,  host: 8088  # ResourceManager WebUI
guest: 8032,  host: 8032  # ResourceManager RPC
# Hive
guest: 9083,  host: 9083  # Metastore
guest: 10000, host: 10000 # HiveServer2
# Spark
guest: 8080,  host: 8080  # Standalone Master WebUI
guest: 7077,  host: 7077  # Standalone Master RPC
guest: 4040,  host: 4040  # Spark Application WebUI
# Cassandra
guest: 9042,  host: 9042  # Native Transport Port
# Kafka
guest: 9092,  host: 9092  # Server Port
# ES
guest: 9200,  host: 9200  # HTTP Port
```

