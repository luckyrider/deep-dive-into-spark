# Kafka官方文档中文版（0.8.2）
注：Kafka的应用越来越广，这得益于Kafka优美的设计和务实的实现。看过很多关于kafka的文档后，发现Kafka的官方文档是解释kafka设计和实现最好的资料之一。目前还没有见到完整的Kafka官方文档中文版，于是决定把官方文档翻译成中文，方便大家学习kafka。此为原创，转载烦请注明出处。

## 1 入门

### 1.1 引言
Kafka是一个分布式的、带分片（partitioned）和副本（replicated）机制的提交日志（commit log）服务。它提供的是消息系统（messaging system）的功能，但设计是独特的。

这都意味着什么呢？

首先让我们回顾一些消息机制（messaging）的基本术语：

* Kafka将消息流（feeds of messages）按类别（category）进行组织，这些类别被称作**topic**
* 往Kafka的topic发布消息的进程，我们称之为**producer**
* 订阅了topic并处理被发布的消息流的进程，我们称之为**consumer**
* Kafka以集群方式运行，由一个或多个服务器组成，每个服务器被称为**broker**

所以，从高层来看，producer通过网络发送消息给Kafka集群，而Kafka集群则将消息提供给consumer，如下图所示：

![producer and consumer](http://kafka.apache.org/images/producer_consumer.png)

客户端和服务器之间的通信，使用一种简单的、高性能的、语言中立的TCP协议。我们（译者注：指官方）提供了Kafka的Java客户端，不过存在许多语言的客户端（译者注：详见[这里](https://cwiki.apache.org/confluence/display/KAFKA/Clients)）。

#### Topic和日志
让我们首先深入到Kafka提供的高层抽象 - topic。

一个topic是所发布消息的类别或者消息流名称。对于每个topic，Kafka集群维护一个经过分片的日志，就像这样：

![log anatomy](http://kafka.apache.org/images/log_anatomy.png)

每个分片是一个有序的、不可变的消息序列，并且不断追加（append）消息，所以本质上也就是一个提交日志（commit log）。分片中的每条消息会分配一个连续的id号，称为偏移量（offset），用它来唯一的识别分片中每条消息。

Kafka集群保留所有发布的消息，不管它们是否已经被消费，保留多长时间是可以配置的。例如，如果日志保留期限被设置为2天，那么一条消息发布后的2天当中，该消息都是可以被消费的，而过了2天后该消息则会被丢弃以释放空间。因为对于不同的数据大小，Kafka的性能可以保持稳定，所以保留大量的数据不是问题。

实际上，每个consumer唯一需要维护的元数据是该consumer在该日志中位置，叫做偏移量（offset）。这个偏移量是由消费者控制的，通常来说消费者会一边读消息一边线性的向前移动其偏移量，但是实际上这个位置是消费者控制的，所以消费者可以任何他喜欢的方式消费消息。例如，消费者可以将偏移量重新设置为一个较老的值然后重新处理消息。

这些特性组合起来，意味着Kafka的消费者是非常廉价的，它们可以来来去去而对集群或其他消费者不产生很大的影响。例如，你可以使用命令行工具去tail任意topic的内容，而不改变已有消费者所消费的东西。

日志的分片有几个用途。首先，它们让日志可以超过一台服务器能容纳的大小。每个单独的分片必须能够安放在所处的服务器上，但是一个topic可以有很多分片，从而可以处理任意数量的数据。其次，它们用作并发的单元（unit of parallelism），稍后详述。

#### 分布
日志的分片分布在Kafka集群中的服务器上，每个服务器处理一部分分片的数据和请求。为了容错，每个分片被复制到指定数量的服务器上。

每个分片有一个服务器作为leader，0个或多个服务器作为follower。leader处理该分片的所有的读和写请求，而follower则只是被动的对leader进行复制。如果leader失效了，某个follower会自动变为新的leader。每个服务器会作为某些分片的leader，而作为其他分片的follower，所以负载在集群中很好的进行了均衡。

#### Producer
Producer发布数据到它所选的topic上。Producer负责选择哪个消息分配到哪个该topic的分片。这可以通过round-robin的方式简单的进行负载均衡，或者通过某个语义分片函数（semantic partition function）（比如说基于消息中的某个key）。稍后详述。

#### Consumer
消息机制（messaging）传统上有两种模型：队列（queuing）和发布-订阅（publish-subscribe）。队列模型中，一组消费者从服务器读，每个消息只会到达其中一个；发布-订阅模型中，消息被广播到所有的消费者。Kafka提供了一个简单的消费者的抽象，可以泛化这两种模型，该抽象被称为消费者组（consumer group）。

消费者用消费者组名来标记自己，每个发布到topic的消息会被传递给每个消费者组的一个消费者实例。消费者实例可以在单独的进程中，或者单独的机器上。

如果所有的消费者实例有相同的消费者组，那么这相当于传统的队列，用来在消费者之间均衡负载。

如果所有的消费者实例都有不同的消费者组，那么这相当于发布-订阅，所有消费会广播给所有的消费者。

不过，更常见的是，topic有为数不多的消费者组，每个对应一个逻辑订阅者（logical subscribe）。为了可伸缩性和容错，每个组则包含许多消费者实例。这不过就是发布-订阅语义，只是订阅者是一组消费者而不是一个单独的进程。

![consumer groups](http://kafka.apache.org/images/consumer-groups.png)

Kafka也比传统的消息系统有更强的顺序保证。

传统的队列在服务器上维持消息的顺序，如果多个消费者消费队列的话，那么服务器会按照消息储存的顺序传递消息。但是，尽管服务器传递消息是有序的，消息是以异步的方式传递给这多个消费者的，所以消息到达不同的消费者时是无序的。这意味着，在并行消费时，消息的顺序丢失了。消息系统通常使用排他消费者（exclusive consumer）这一概念来处理这一问题，即只允许一个进程消费一个队列，当然这意味着没有了处理的并行性。

Kafka处理得更好。使用分片来实现topic内的并行的概念，Kafka能够同时提供顺序保证和一组消费者进程间的负载均衡。topic中的每个partition分配给消费者组中的消费者，并且使得每个partition只被组中的一个消费者消费。通过这种方式，我们保证了消费者是这个partition的唯一reader，从而按顺序消费数据。既然有很多partition，这种方式仍然能够将负载均衡分布在众多消费者实例上。但是注意，消费者实例不能比partition多。（译者注：比partition多的消费者实例没有机会消费数据）

Kafka仅仅提供一个partition内消息的全序关系（total order），一个topic内不同partition的消息则没有这种保证。partition单位的顺序，以及根据key将数据进行分片（partition）的能力，对大多数应用来说足够了。不过，如果你需要的是所有消息上的全序关系，则可以通过一个只有一个partition的topic来实现，当然这也意味着只能有一个消费者进程。

#### 保证
从高层来看，Kafka提供了如下保证：

* 一个生产者发送到某个topic的某个partition的消息，会按照消息发送的顺序追加。也就是说，如果消息M1和M2都是同一个生产者发送的，并且M1先发送，那么M1相比M2来说会有一个较低的偏移量，在日志中出现也较早。
* 一个消费者实例按照消息储存在日志中的顺序来看消息。
* 如果一个topic的副本因子是N，我们顶多可以忍受N-1个服务器的失效而不会丢失已经提交到日志的任何消息。

关于这些保证的更多细节见后文说明Kafka设计的部分。

### 1.2 用例


### 1.3 快速上手
本教程假设你从干净的环境开始,并且没有遗留的Kafka或Zookeeper的数据。

#### 第1步: 下载源码
[下载](https://www.apache.org/dyn/closer.cgi?path=/kafka/0.8.2.0/kafka_2.10-0.8.2.0.tgz)0.8.2.0发行版并解压。

```
> tar -xzf kafka_2.10-0.8.2.0.tgz
> cd kafka_2.10-0.8.2.0
```

#### 第2步: 启动服务器
Kafka使用了ZooKeeper，因此如果你还没有准备它的话，需要首先启动一个ZooKeeper服务器。你可以使用跟Kafka封装在一起的方便的脚本来获得一个单节点的ZooKeeper实例。

```
> bin/zookeeper-server-start.sh config/zookeeper.properties
[2013-04-22 15:01:37,495] INFO Reading configuration from: config/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
...
```

现在启动Kafka服务器：

```
> bin/kafka-server-start.sh config/server.properties
[2013-04-22 15:01:47,028] INFO Verifying properties (kafka.utils.VerifiableProperties)
[2013-04-22 15:01:47,051] INFO Property socket.send.buffer.bytes is overridden to 1048576 (kafka.utils.VerifiableProperties)
...
```

#### 第3步: 创建topic
让我们创建一个名为"test"的单分片和仅有一个副本的topic:

```
> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

如果我们运行罗列topic的命令，我们马上就能看到这个topic:

```
> bin/kafka-topics.sh --list --zookeeper localhost:2181
test
```

除了手动创建topic之外，你也可以配置你的brokers，使得往一个不存在的topic发布消息时，自动创建该topic。

#### 第4步：发送一些消息
Kafka用命令行客户端作为输入，从一个文件或标准输入，并发送消息到Kafka集群。默认情况下,每一行将作为一个单独的消息被发送。
运行producer脚本,然后输入几条消息到控制台并发送到服务器。

```
> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test 
This is a message
This is another message
```

#### 第5步:启动一个Consumer
Kafka也有一个命令行Consumer脚本，它将消息转储到标准输出。

```
> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
This is a message
This is another message
```

如果你在一个不同的终端运行上面的命令,那么你现在应该可以输入消息Producer终端和看到他们出现在Consumer终端。
所有的命令行工具都有附加选项,不使用任何参数运行命令将显示使用信息，其中记录了更多细节。

#### 第6步：配置一个多broker集群
到目前为止我们反对运行一个单一的broker，那没有什么乐趣。对于Kafka，一个单一的broker只是仅有1个节点的集群，与其他有多个broker的集群相比没有什么变化。但为了感受它，让我们扩大我们的集群到三个节点（仍然运行在我们本地机器上）。

首先，我们为每个broker创建一个配置文件：

```
> cp config/server.properties config/server-1.properties 
> cp config/server.properties config/server-2.properties
```

现在按下面的配置信息编辑这些文件：

```
config/server-1.properties:
    broker.id=1
    port=9093
    log.dir=/tmp/kafka-logs-1
 
config/server-2.properties:
    broker.id=2
    port=9094
    log.dir=/tmp/kafka-logs-2
```

broker.id属性是各节点在集群中唯一的和永久的标识。
我们必须重写端口和日志目录，这是因为我们在相同的机器上运行它们，我们想要保持所有试图通过相同的端口注册或者覆盖彼此数据的这些brokers。

我们之前已经启动了Zookeeper和我们的单节点，因此我们只需要启动下面这两个新节点：

```
> bin/kafka-server-start.sh config/server-1.properties &
...
> bin/kafka-server-start.sh config/server-2.properties &
...
```

现在创建一个有三个副本的新的topic：

```
> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic
```

好，现在我们有一个集群，我们怎么能知道哪个broker在做什么？可以运行`describe topics`命令看一下：

```
> bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
Topic:my-replicated-topic	PartitionCount:1	ReplicationFactor:3	Configs:
	Topic: my-replicated-topic	Partition: 0	Leader: 1	Replicas: 1,2,0	Isr: 1,2,0
```

下面是一个topic说明的输出。第一行给出所有分区的一个概要，每一行提供了有关一个分区的信息。因为这个Topic只有一个分区那么就只有一行。

```
"leader" is the node responsible for all reads and writes for the given partition. Each node will be the leader for a randomly selected portion of the partitions.
"replicas" is the list of nodes that replicate the log for this partition regardless of whether they are the leader or even if they are currently alive.
"isr" is the set of "in-sync" replicas. This is the subset of the replicas list that is currently alive and caught-up to the leader.
```

请注意，在我的例子中，节点1为Topic的唯一分区的leader。

我们可以在原来创建的Topic上运行相同的命令：

```
> bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test
Topic:test	PartitionCount:1	ReplicationFactor:1	Configs:
	Topic: test	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
```

看起来没有什么惊喜，原来的topic没有副本，在服务器0上，当我们创建它时，它仅仅是我们集群中的服务器。

让我们发布一些消息到我们的新的topic：

```
> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic
...
my test message 1
my test message 2
^C
```

现在让我们消费这些消息：

```
> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic
...
my test message 1
my test message 2
^C
```

现在让我们测试容错。Broker 1担当leader的角色，让我们干掉它：

```
> ps | grep server-1.properties
7564 ttys002    0:15.91 /System/Library/Frameworks/JavaVM.framework/Versions/1.6/Home/bin/java...
> kill -9 7564
```

Leader被换成了从节点中的一个，并且节点1不再同步副本集：

```
> bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
Topic:my-replicated-topic	PartitionCount:1	ReplicationFactor:3	Configs:
	Topic: my-replicated-topic	Partition: 0	Leader: 2	Replicas: 1,2,0	Isr: 2,0
```

尽管原来写入的leader已经宕掉，但消息仍然可以被消费的：

```
> bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic
...
my test message 1
my test message 2
^C
```

### 1.4 生态系统
有太多的工具，它们整合了Kafka以外的主要分布。生态系统的页面列出了很多，包括数据流处理系统，Hadoop的集成，监控和部署工具。

### 1.5 升级

#### 从0.8.1升级到 0.8.2.0
0.8.2.0完全兼容0.8.1，升级能够通过简单的替换操作（bringing it down）依次完成每个broker，更新代码，并重新启动它。

#### 从0.8.0升级到 0.8.1
0.8.1版本完全兼容0.8。升级能够通过简单的替换操作（bringing it down）依次完成每个broker，更新代码，并重新启动它。

#### 从0.7升级
在0.8版本中添加了副本，也是我们第一个向后兼容的版本：API做了重大的改变，ZooKeeper的数据结构，协议和配置。从0.7升级到0.8.x 需要迁移的[专用工具](https://cwiki.apache.org/confluence/display/KAFKA/Migrating+from+0.7+to+0.8)。这种迁移可以做到不停机。

## 2. API

### 2.1 Producer API

### 2.2 高层Consumer API

### 2.3 简单Consumer API

### 2.4 Kafka Hadoop Comsumer API

## 3.配置

### 3.1 Broker配置

### 3.2 Consumer配置

### 3.3 Producer配置

### 3.4 新Producer配置

## 4. 设计

### 4.1 动机
我们将Kafka设计成一个统一平台，用来处理一个大公司可能有的所有实时数据流（data feeds）。为了实现这一目标，我们不得不考虑相当广泛的一组用例。

它必须具有高吞吐量，用以支持大量的事件流，比如实时的日志聚集。

它必须优雅地处理大量积压的数据（backlogs），比如从离线系统周期性地加载数据。

这也意味着这个系统能够处理低延迟的数据传递，用以处理相对较传统的messaging这种用例。

我们希望支持对这些数据feeds进行分片的、分布式的实时处理，以创建新的、派生的数据feeds。这个促成了我们的分片和消费者模型。

最后，如果数据流要递送给其他数据系统，这个系统必须保证机器故障时的容错性。

为了支持这些使用场景，我们的设计有一些很特别的元素，使它看起来更像数据库日志（database log），而不是一个传统的消息系统。我们将在接下来的部分概要描述我们的设计。

### 4.2 持久化

#### 不要害怕文件系统
Kafka严重依赖文件系统进行消息的存储和缓存。有一种普遍的想法是“磁盘是慢的”，这使得大家都怀疑，一个持久化的结构能够提供具有竞争力的性能。实际上，磁盘比人们想象的既要慢得多也快得多，就看怎么使用了。设计合理的话，磁盘结构通常可以和网络一样快。

磁盘性能的关键因素在于，在过去十年，磁盘寻道的高延迟导致了硬盘吞吐量的两极分化。结果是，对于由六块7200rpm、SATA硬盘组成的配置为JBOD的RAID-5磁盘阵列，线性写的性能可以达到每秒600MB，随机写的性能则只有每秒100KB，相差6000倍。线性读和写是所有使用模式中性能最可预测的，并且操作系统也进行了大量的优化。现代操作系统提供了预读（read-ahead）和后写（write-behind）技术，会预先取大量数据块，也会将较小的逻辑写合并为较大的物理写。关于该问题的进一步讨论可以参考[这篇ACM Queue的文章](http://queue.acm.org/detail.cfm?id=1563874)，实际上他们发现某些情况下线性的磁盘访问比随机的内存访问还要快。

为了弥合这种性能的两极分化，现代操作系统变得越来越aggressive地利用主存来进行磁盘的缓存。现代的操作系统很乐于把所有空闲的内存转变为磁盘缓存，当内存被回收时性能的影响也很小。所有对磁盘的读写都会经过这个统一的缓存。这个特性很难被关掉除非使用直接IO（direct IO），所以即使一个进程为数据维护了进程内的缓存，这些数据很可能也会复制都操作系统的pagecache里面，实际上任何数据都保存了两份。

更进一步，如果我们的系统构建在JVM上，对Java内存的使用略有了解的人都知道这两个事：

* 内存存储对象的开销是很高的，通常是所存储数据的两倍（甚至更糟）。
* 随着堆内（in-heap）数据的增长，Java垃圾收集会变得越来越费时费力。

根据上述因素，使用文件系统和pagecache，比维护进程内缓存要好，可用内存至少翻了一番，自动获得了所有空闲内存的访问能力，如果存储为紧凑的字节结构而不是存储为一个个独立的对象，可用内存又可以翻一番。这样做的话，在一台32GB内存的机器上，最多可以获得28到32GB的缓存，还没有垃圾收集的坏处。更进一步，这样的缓存即使是在服务重启之后还是保持热的（warm）；而进程内缓存是需要被重建的（10GB的缓存可能要10分钟），不然的话服务起来后缓存将是完全冷的（cold）（这很可能意味着很槽糕的初始性能）。这样的设计也能大大简化代码，因为维护缓存和文件系统一致性的逻辑都是操作系统负责的，并且操作系统层面的实现也比一次性的进程层面的实现更加高效和正确。如果磁盘使用场景倾向于线性的读，那么预读（read-ahead）会在每次读磁盘时预先将有用的数据填充到缓存中。

这也意味着设计是非常简单的：不是在内存中保持尽可能多的数据然后当空间不够时匆忙将它们全部刷写（flush）到文件系统，而是倒过来。所有的数据都马上写到文件系统的持久化日志上，而无需向磁盘进行刷写。实际上，这只不过意味着数据被传送到了内核的pagecache中。

这种基于pagecache的设计，在[关于Vanish设计的一篇文章](http://varnish.projects.linpro.no/wiki/ArchitectNotes)中有描述（带着适度的自负）。

#### 常量时间已足够
消息系统所使用的持久化数据结构通常是每个consumer一个队列，并伴随着使用B树或其他通用的随机访问数据结构以维护消息的元数据。B树是最通用的数据结构，可以支持消息系统多种多样事务的、非事务的语义。但是它们也带来了相当高的代价：B树操作是O(log N)。通常O(log N)被认为基本上等价于常量时间，但是对于磁盘操作来说这不成立。磁盘的寻道，一次需要花费10ms，并且每个磁盘每次只能进行一次寻道操作，所以并行是有限的。因此，即使少量的磁盘寻道也会导致很高的开销。既然存储系统混合着非常快速的缓存操作和非常慢的物理磁盘操作，在缓存固定而数据增加时，被观测到的树结构的性能通常是超线性的（superlinear），也就是说，数据加倍导致性能不止慢两倍，而是糟糕得多。

凭直觉，持久化队列可以基于简单读和追加到文件来构建，就跟通常的日志解决方法一样。这种结构的优势在于，所有的操作都是O(1)的，读不会阻塞写，也不会阻塞其他的读。性能优势是明显的，因为性能和数据大小完全是解耦的，服务器可以充分利用一些廉价、低转速、1TB以上的SATA磁盘。尽管它们的寻道性能很差，它们具有可接受的大量数据的读写性能，价钱只要1/3而容量是3倍。

可以访问无限的磁盘空间却没有性能的损害，这意味着我们可以提供通常的消息系统没有的功能。例如，在Kafka中，不是消息一旦被消费就尽快删除它，而是将消息保留相对较长的一段时间（比如说一周）。这给消费者带来了极大的灵活性，后文会详述。

### 4.3 效率
我们在效率上花了大量精力。我们主要的用例之一是处理web活动数据，其量是非常大的：一次页面浏览（page view），会产生大量的写。更进一步，我们假设每条消息会被不止一个（通常有很多）consumer读，因此我们努力使得消费的代价尽可能的低。

根据我们构建多个类似系统的经验，我们还发现效率对高效的多租户（multi-tenant）操作来说是关键。如果应用在使用方式上对底层的基础服务（downstream infrastructure service）有些小的碰撞（bump），就很容易地使基础服务成了瓶颈，这种的小变化也常常会导致问题。通过让基础服务非常快速，我们可以帮助确保在负载下，应用在基础服务支撑不住之前先倒下。如果希望运行一个集中式的服务（centralized service），它需要在一个集中的集群上支撑几十、上百个应用，这一点尤其重要，因为使用方式（usage patterns）的变化几乎是每天都会发生的事。

前一小节我们讨论了磁盘的效率。一旦槽糕的磁盘访问方式被消除，这类系统低效的原因常见的有两个：太多小的IO操作，过度的字节拷贝。

小的IO操作这个问题，发生在客户端和服务器之间，也发生在服务器自身的持久化操作上。

为了避免这个问题，我们的协议基于“消息组”（message set）这一抽象，它很自然地将多个消息组合在一起。这使得网络请求可以将多个消息组合在一起，分摊网络来回（round trip）的开销，而不是每次发送一条消息。服务器一次往日志追加大块的消息，consumer一次取大块的线性的消息。

这种简单的优化带来了数量级的速度提升。批处理（batching）导致更大的网络数据包，更大的线性磁盘操作，更大的连续内存块，等等，利用所有这些，Kafka能够将随机的消息写操作所形成的断断续续的数据流，转换为线性的写操作再流向consumer。

另一个低效在于字节拷贝。消息速率低时这不成问题，但是在高负载时影响是重大的。为了避免这一问题，我们采用标准的二进制消息格式，并被producer、broker和consumer所共享（所以数据块在他们之间无需修改就能传来传去）。

broker所维护的消息日志只是一个目录下的多个文件，每个文件包含一系列的消息组，写到磁盘上的消息组的格式跟producer和consumer所使用的格式是一样的。维护这个公共的格式，使得能够对最重要的操作 - 持久化日志块的网络传输 - 进行优化。现代的unix操作系统提供了经过高度优化的数据路径（译者注：原文有误，原文是code path，应该为data path）进行pagecache到socket的数据传输，在linux中这是通过[sendfile系统调用](http://man7.org/linux/man-pages/man2/sendfile.2.html)达到的。

为了理解sendfile带来的影响，理解通常的从文件到socket的数据路径很重要。

* 操作系统从磁盘读取数据放到内核空间（kernel space）的pagecache
* 应用程序将数据从内核空间读到用户空间（user space）的缓冲区（buffer）
* 应用程序将数据写回到内核空间的socket缓冲区（buffer）
* 操作系统将数据从socket缓冲区拷贝到NIC（译者注：即网卡）缓冲区，在这儿数据就可以发送到网络上了。

很明显这是低效的，包括4次拷贝和2次系统调用。使用sendfile，可以避免重复拷贝，使操作系统能够直接将数据从pagecache发送到网络上。在这个优化路径中，只需要最后的到NIC缓冲区的拷贝。

我们设想一个topic有多个consumer的用例是常见的情形。使用上面的零拷贝（zero-copy）优化，数据往pagecache中拷贝一次，然后被每次消费重用，而不是每次读数据时，先存储到内存中然后再拷贝到内核空间。这使得消息的消费速度可以接近网络连接的上限。

这种pagecache和sendfile的组合，意味着在consumer基本上能赶上的Kafka集群上，你将看不到对磁盘的读操作，因为数据服务完全从缓存提供。（译者注：没有文件IO，都是内存操作，因此效率是非常高的）

关于Java对sendfile和zero-copy支持的更多背景知识，可以参考[这篇文章](http://www.ibm.com/developerworks/linux/library/j-zerocopy)。

#### 端到端的批量压缩（Batch Compression）
有些时候，瓶颈实际上并不是CPU，也不是磁盘，而是网络带宽。特别是对需要在广域网（wide-area network）上的数据中心之间传送消息的数据管道（data pipeline）而言，则更是如此。当然，没有Kafka的支持，用户总归可以一次一条地压缩消息的，但是这会导致非常糟糕的压缩率，因为相同类型的消息有很多重复的地方（比如，JSON的字段名，web日志的user agent，或者公共的字符串值）。高效的压缩需要将多条消息一起压缩，而不是每条消息单独压缩。

Kafka通过重复出现的消息组来支持这种压缩。一批消息可以成块的进行压缩然后发送到服务器。这批消息会以压缩的形式写出去，在日志中也保持压缩的形式，只有consumer才会去解压缩。

Kafka支持GZIP和Snappy压缩协议。更多关于压缩的信息参见[这里](https://cwiki.apache.org/confluence/display/KAFKA/Compression)。

### 4.4 Producer
#### 负载均衡
Producer直接把数据发送给某个broker，没有任何中间的路由层，而这个broker就是分片的leader。为了帮助producer完成这个事情，任何时候，任何Kafka节点都可以回答元数据请求，比如哪些服务器是alive的，topic分片的leader在哪里，使得producer能够将请求发送到合适的服务器。

客户端控制消息发布到哪个分片。可以是随机的，实现随机的负载均衡，或者可以采用语义分片函数（semantic partitioning function）。我们暴露的用于语义分片的接口，允许用户指定一个用于分片的key，然后对key进行hash得到一个分片（如果需要的话，也可以重写这个分片函数）。比如说，如果所选的key是用户id，那么指定用户的所有数据将会发送到同一个分片。这也使得consumer可以作局部假设（locality assumptions）。我们明确采用了这种设计，这样的分片方式使得consumer可以进行局部敏感（locality-sensitive）处理。

#### 异步发送
批量处理（Batching）是效率的主要驱动力之一。为了实现批量处理，Kafka的producer会试着将数据累积在内存中，并在一个请求中发送较大的一批数据。批量处理的设置，可以是累积不超过一定数量的消息，或者等待不超过某个延迟上限（比如说64KB或者10ms）。这使得可以累积更多的字节再发送，对服务器也意味着较少次数、而每次较大数据量的IO操作。这种缓冲处理（buffering）是可配置的，这提供了一种机制，用少许的额外的延迟来换取更好的吞吐量。

关于producer的配置和API的详细信息可以参见本文档的相关部分。

### 4.5 Consumer
Kafka的consumer给broker发送fetch请求，该broker是它想要消费的分片的leader。consumer在每个请求中都会指定日志的偏移量，随后接收到从该位置开始一块日志。这样，consumer对这个位置有很大的控制权，如果需要的话，它可以回转这个偏移量以重新消费数据。

#### 推还是拉（Push vs. pull）
一开始我们就考虑的一个问题是，是应该让consumer从broker拉取数据呢，还是让broker把数据推送给consumer。就这个问题而言，Kafka沿用一种比较传统的设计，是大多数消息系统所采用，producer将数据推送到broker，consumer从broker拉取数据。有些以日志为中心（logging-centric）的系统，比如说Scribe和Apache Flume采用一种非常不同的基于推送的路线，数据被不断往下游推送。两种方法都有利有弊。然后，基于推送的系统要处理多种consumer是比较困难的，因为broker控制数据传输时的速度。通常目标是让consumer能够以尽可能快的速度消费数据；但是不幸的是，基于推送的系统中，这意味着当消费速度落后于生产速度时（本质上就是一个拒绝服务攻击，a denial of service attack），consumer会被淹没（overwhelmed）。基于拉取的系统有更好的特性，consumer就落后着，等可能的时候再赶上来。这个问题也可以通过某种后退协议（backoff protocol）进行减轻，consumer会指示说他被淹没了，但是怎么调整传输速度使得能充分利用消费者（但不过分利用），比看起来要微妙得多。根据之前我们试着用这种方式构建系统的经验，我们决定采用比较传统的拉取模型。

基于拉取的系统的另一个优势是，这导致往consumer发送数据时采用激进的批量处理的方式。一个基于推的系统，要么立即发送一个请求，要么累积更多的数据，然后不管下游的consumer是否有能力立即消费直接发送给consumer。如果为低延迟做了调优，这会导致每次只发送一条消息而只是被缓冲起来，这是一种浪费。基于拉取的设计则可以修复这个问题，consumer总是从日志中拉取当前位置后所有可用的消息（或者配置的最大值）。获得了理想的批量处理，却不会引入不必要的延迟。

#### 消费者的位置（Consumer Position）
有点意外的是，跟踪消费了哪些消息，是消息系统性能的关键点之一。

大多数的消息系统在broker上维持关于消费了哪些消息的元数据。也就是说，当一条消息被递交给消费者，broker要么马上在本地记录这个事实，或者等待来自消费者的确认。这是一种相当符合直觉的选择，对于单台机器的服务器，确实不清楚这个状态应该放在哪儿。既然很多消息系统用于存储的数据结构伸缩性很差，这也是一个实用的选择，因为broker知道什么被消费过了所以可以马上删掉它，从而保持数据比较小。

不太显然的是，让broker和consumer就什么已经被消费达成一致，不是一个微不足道的事。如果broker在每次将消息递送到网络上时就把该消息记录为已消费，那么，如果consumer没有成功处理这条消息（比如说因为它宕机了，或者请求超时了，或者其他什么的），这条消息就丢失了。为了解决这个问题，许多消息系统增加了确认机制（acknowledgement feature），这意味着一条消息被发送后仅仅被标记为“已发送”而不是“已消费”，broker等待来自consumer的特定的确认，然后才将该消息标记为“已消费”。这一策略解决了丢消息的问题，但是却制造了新的问题。首先，如果consumer处理了消息但是在他发送确认之前发生了故障，那么这条消息会被消费两次。第二个问题是关于性能的，现在broker需要为每条消息维护多个状态（先锁住它不让它递送两次，然后标记成已经被永久消费，这样就可以删除它了）。必须处理一些微妙的问题，例如，如果消息被发送了但是却一直没有收到确认，该怎么办。

Kakfa用不同的方式处理这个问题。topic被分割为一组保持全序关系的分片，每个分片在任何时候会被一个消费者进行消费。这意味着对每个分片的消费者来说，消费到哪个位置了，只是一个简单的整数，即要消费的下一条消息的偏移量。这使得什么消息已经被消费这个状态非常小，仅仅是每个分片一个整数。这个状态可以周期性地进行检查点处理（checkpoint）。这使得消息确认（message acknowledgements）的代价很低。

这个决策有一个副作用。一个consumer可以有意的回转到一个旧的偏移量并重新消费数据。这违反了通常的队列的约定，但是事实证明对很多消费者来说是一个必要的功能。例如，如果在消费了一些消息之后才发现consumer的代码有bug，consumer可以在这个bug被修复后重新消费那些消息。

#### 离线数据的加载（Offline Data Load）
可伸缩的持久机制，能够接纳仅仅周期性地消费批量数据负载的消费者。这样的消费者周期性地批量地将数据加载到离线系统，比如Hadoop或者关系型数据仓库。

就Hadoop这一场景而言，我们可以将负载分割成1个node/topic/partition的组合对应为1个map任务，从而将数据加载并行化。由Hadoop提供任务管理，失败的任务可以重新开始，因为会从原来的位置开始，所以不存在重复数据的危险。

### 4.6 消息传递语义（Message Delivery Semantics）
既然我们了解了producer和consumer是如何工作的，让我们讨论一下Kafka所提供的在producer和consumer之间的语义保证。很明显，能够提供多种可能的消息传递语义：

* 至多一次（At most once）：消息可能会丢失，但是不会被重复传递。
* 至少一次（At least once）：消息从不丢失，但是可能会被重复传递。
* 刚好一次（Exactly once）：这是人们真正需要的，每条消息被传递一次并且只传递一次。

值得一提的是，这可以分解为两个问题：发布消息的持久性保证，和消费消息时的保证。

许多系统声称提供刚好一次传递语义，但是要看仔细了，这些声明大多是误导人的（也就是说，它们无法应对consumer或者producer发生故障的情况，或者有多个消费者进程的情况，或者写到磁盘上的数据可能会丢失的情况）。

Kafka的语义比较简单直接。当发布一条消息时，我们有该消息被提交（committed）到日志这个概念。一旦发布的消息已经被提交，该消息会被写入某个分片，并且分片会被复制到多个broker，只要其中一个broker还存活着（alive），这条消息就不会丢失。存活的定义，以及哪些故障类型是我们试着去处理的，后面的小节会有更详细的描述。目前我们可以假设完美的、无损失的broker，在此基础上我们试着来理解提供给producer和consumer的保证。如果producer试着发布消息并且遇到了网络故障，它并不能确定这个故障是在消息被提交之前还是之后发生的。这类似于往数据库表里插入自增量键值（autogenerated key）的语义。

这些并不是对publisher最强的语义。尽管我们不能确定网络出错时到底发生了什么，但是，让producer产生某种主键（primary key）使得重新尝试produce request幂等，这是可能的。这个功能对一个带副本的系统不是无关紧要的，因为即使发生服务器故障的情况下它也要能正常工作。有了这个功能，producer只要不断重试，直到它接收到一个被成功提交的消息的确认，这时我们就能保证该消息被发布了刚好一次。我们希望在Kafka未来的版本中能增加这个功能。

并不是所有的用例都需要这么强的保证。对于延迟敏感（latency sensitive）的用户，我们允许producer指定它所需要的持久程度（durability level）。如果producer指定说它希望一直等到消息被提交，花费的时间是10ms这个量级的。不过，producer也可以指定说它希望完全异步地执行发送操作，或者它只愿意等到leader收到了消息（follower不一定收到）。

现在让我们从consumer的角度来描述语义。所有的副本有相同的日志也有相同的偏移量。consumer控制它在日志中的位置。如果consumer从不宕机，它可以只把这个位置放在内存中，但是如果consumer发生了故障，我们希望这个topic分片被另外一个进程接管，这个新的进程需要选择一个合适的位置开始进行处理。让我们假设consumer读取了一些消息，它有几种选项来处理消息和更新它的位置。

1. 它可以读消息，然后保存日志的位置，最后再处理消息。这种情况下，有可能发生的是，在consumer保存了位置之后但在保存消息处理的输出之前consumer进程发生故障。这种情况下，接管进程会从保存的位置开始，尽管该位置之前的一些消息还没有被处理。这相当于至多一次语义，因为在consumer发生故障时消息有可能不会被处理。
2. 它可以读消息，处理消息，最后再保存位置。这种情况下，有可能发生的是，在consumer处理了消息之后但在保存位置之前consumer进程发生故障。这种情况下，接管进程所接收到的头几条消息是已经被处理过的。这相当于至少一次语义，在consumer发生故障时。在很多时候，消息有主键，所以更新是幂等的（接受相同消息两次，只是用记录自身的拷贝来覆盖自己。）
3. 那刚好一次语义呢？（你真正想要的？）这里的限制其实不是消息系统的功能，而是必须协调consumer的位置和消息处理输出。经典的达到这个目的的方法是引入二阶段提交（two-phase commit），用以协调consumer位置的存储和consumer输出的存储。但是这可以用一种更简单和通用的方式来进行处理，即把偏移量和结果存在同一个地方。这更好，因为consumer想要写入的输出系统并不支持二阶段提交。举个例子，我们往HDFS上填充数据的Hadoop ETL在HDFS同时保存偏移量和所读的数据，使得能够保证数据和偏移量要么都被更新，要么都不被更新。我们在许多其他的需要这种较强语义但又不存在主键来进行去重（deduplication）的数据系统中遵循这种模式。

所以Kafka实际上默认提供了至少一次语义，同时，通过producer端禁用重发，结合consumer端在处理一批消息前提交偏移量，使用户能实现至多一次语义。刚好一次传递语义需要目的存储系统的配合，Kafka提供的偏移量使得这实现起来简单直接。

### 4.7 副本（Replication）
Kafka会将每个topic的每个partition的日志复制到指定数量的服务器上（你可以一个topic一个topic地设置这个副本因子）。这样，当集群中的一台机器发生故障时，可以自动切换到其他副本，使得消息仍然是可用的。

其他的消息系统提供某种副本相关的功能，但是在我们看来（完全是带偏见的），这看上去像是附加上去的，没有重度使用，有大的负面影响：slave不活跃，吞吐率受到严重影响，需要费事的手工配置，等等。Kafka被有意设计成默认情况下是使用副本的，实际上我们将无复制的topic实现为副本因子为1的有复制topic。

复制以topic的partition为单位。在无故障的情况下，Kafka中的每个partition有一个leader和零或多个follower。副本的总数（包括leader在内），构成了副本因子。所有的读和写操作在partition的leader上完成。通常，partition的数量比broker的数量多得多，leader会被均匀分布在broker上。follower上的日志跟leader上的日志是一模一样的，有相同的偏移量，消息有相同的顺序（当然，在任何时候，leader有可能有几个位于日志尾部的尚未复制的消息）。

Follower消费leader上的消息的方式就跟正常的Kafka consumer一样，然后将消费的消息写到自己的日志上。让follower从leader拉取消息，使得follower能很自然的将要写的日志条目集中成一批一批进行批量处理（batched together），这是一个很好的特性。

跟大多数的分布式系统一样，自动处理故障，需要精确地定义什么样的节点是活跃的（alive）。Kafka的节点是活跃的，有两个条件：

* 一个节点必须能够维护它和ZooKeeper之间的会话（基于ZooKeeper的心跳机制）
* 如果它是slave，它必须能够复制leader上的写操作，并且不能落后太多。

我们把满足这两个条件的节点称为“in sync”等，以避免“alive”或”failed“的含糊不清。leader会一直关注”in sync“节点的集合。如果一个follower宕了、很卡、或者落后太多，leader会把它从”in sync“副本列表中删除。落后多少算太多，由配置项`replica.lag.max.messages`来控制。卡多久算很卡，由配置项`replica.lag.time.max.ms`来控制。

用分布式系统的术语来说，我们只试着处理故障的一种”fail/recover“模型，这种模型中，节点突然停止工作，后来又恢复了（也许都不知道它们已经宕了）。Kafka不处理所谓的”拜占庭（Byzantine）“故障，这种故障中，节点会产生随意的或者有害的应答（也许是因为bug或犯规）。

一条消息所对应的partition的所有“in sync”副本已经将该消息写到它们的日志上，该消息才被认为是“committed”。只有“committed”消息会被递交给consumer。这意味着，consumer不用担心可能会看到leader失效就会丢失的消息。另一方面，producer则可以基于对延迟和持久性权衡的偏好，选择到底要不要等待消息直到消息被“committed”。这种偏好是有producer用的配置项`request.required.acks`来控制的。

Kafka所提供的保证是，任何时候，一条已提交（committed）的消息是不会丢失的，只要至少有一个in sync副本活着。

Kafka在节点故障发生时经过短时间的故障切换（failover）可以保持可用，但在网络分离（network partitions）的时候不一定能保持可用。

#### Replicated Logs: Quorums, ISRs, and State Machines

#### Unclean leader election: What if they all die?

#### 可用性和持久性保证

#### 副本管理


### 4.8 日志压紧（Compaction）

## 5. 实现

### 5.1 API设计

### 5.2 网络层

### 5.3 消息

### 5.4 消息格式

### 5.5 日志

### 5.6 分布

## 6. 运营

### 6.1 Kafka的基本运营

### 6.2 数据中心

### 6.3 Kafka的配置
#### 重要的服务器配置

#### 重要的客户端配置
producer最重要的配置控制着：

* compression
* sync vs async production
* batch size (for async producers)

consumer最重要的配置是fetch size。

所有的配置都记录在配置这一部分。

#### 一份生产环境的服务器配置
下面是我们的生产环境服务器的配置

```
# Replication configurations
num.replica.fetchers=4
replica.fetch.max.bytes=1048576
replica.fetch.wait.max.ms=500
replica.high.watermark.checkpoint.interval.ms=5000
replica.socket.timeout.ms=30000
replica.socket.receive.buffer.bytes=65536
replica.lag.time.max.ms=10000
replica.lag.max.messages=4000

controller.socket.timeout.ms=30000
controller.message.queue.size=10

# Log configuration
num.partitions=8
message.max.bytes=1000000
auto.create.topics.enable=true
log.index.interval.bytes=4096
log.index.size.max.bytes=10485760
log.retention.hours=168
log.flush.interval.ms=10000
log.flush.interval.messages=20000
log.flush.scheduler.interval.ms=2000
log.roll.hours=168
log.retention.check.interval.ms=300000
log.segment.bytes=1073741824

# ZK configuration
zookeeper.connection.timeout.ms=6000
zookeeper.sync.time.ms=2000

# Socket server configuration
num.io.threads=8
num.network.threads=8
socket.request.max.bytes=104857600
socket.receive.buffer.bytes=1048576
socket.send.buffer.bytes=1048576
queued.max.requests=16
fetch.purgatory.purge.interval.requests=100
producer.purgatory.purge.interval.requests=100
```

我们客户端的配置随着应用场景的不同有较大的变化。

### 6.4 Java版本
我们目前运行JDK 1.7 u51，我们切换到了G1 collector。如果你这么做的话（我们强烈推荐），请确保使用u51。我们测试了u21，我们发现了这个版本的GC实现有一些问题。我们进行了如下的调优：

```
-Xms4g -Xmx4g -XX:PermSize=48m -XX:MaxPermSize=48m -XX:+UseG1GC
-XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35
```

作为参考，LinkedIn峰值时最忙的一个集群的统计数据如下：15 brokers、15.5k partitions (replication factor 2)、400k messages/sec in、70 MB/sec inbound、400 MB/sec+ outbound。这个调优似乎很激进，但是这个集群所有的brokers，90%情况下GC暂停时间（pause time）大约是21ms，每秒进行的young GC小于1。

### 6.5 硬件和操作系统

#### 操作系统

#### 磁盘和文件系统

#### 应用和操作系统刷写（flush）管理

#### 理解Linux操作系统的刷写行为

#### Ext4注意点

### 6.6 监控

### 6.7 ZooKeeper
