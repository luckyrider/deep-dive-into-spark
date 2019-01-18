# CentOS Cookbook

## Overview
* Hardware
* Network
* NTP
* YUM
* 系统监控

## Hardware

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

## Network Basics
### 禁用防火墙iptables

```
sudo service iptables status
iptables: Firewall is not running.
```

### 禁用IPv6

```
cat /etc/sysctl.conf | grep disable_ipv6
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```



### Private Networks
```
24-bit block 	10.0.0.0 - 10.255.255.255
20-bit block 	172.16.0.0 - 172.31.255.255
16-bit block 	192.168.0.0 - 192.168.255.255
```

References:
* http://en.wikipedia.org/wiki/Private_network

### Change Hostname
Linux操作系统的 hostname是一个kernel变量:
* hostname
* cat /proc/sys/kernel/hostname
上面两种输出结果相同。

newname即要设置的新的hostname，运行后立即生效，但是在系统重启后会丢失所做的修改，如果要永久更改系统的hostname，就要修改相关的设置文件。

$ hostname newname

永久更改Linux的hostname. 由/etc/rc.d/rc.sysinit这个脚本负责设置系统的hostname，它读取/etc /sysconfig/network这个文本文件，RedHat的hostname就是在这个文件里设置。如果要永久修改RedHat的hostname，就修改/etc/sysconfig/network文件，将里面的HOSTNAME这一行修改成 HOSTNAME=NEWNAME，其中NEWNAME就是你要设置的hostname。

```
vi /etc/sysconfig/network
HOSTNAME=newname
```

/etc/hosts文件的作用相当如DNS，提供IP地址到hostname的对应。

* 如何修改centos等linux系统的hostname. http://www.ctohome.com/FuWuQi/1b/414.html

### Disable IPv6
adding the following to /etc/sysctl.conf:
```
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
net.ipv6.conf.eth0.disable_ipv6 = 1
```

To disable in the running system:
```
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.eth0.disable_ipv6=1
```
or (可能会fail):
```
echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/default/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/lo/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/eth0/disable_ipv6
```

References:
* http://wiki.centos.org/FAQ/CentOS6#head-d47139912868bcb9d754441ecb6a8a10d41781df

### Proxy Settings
modify /etc/profile:

```
export http_proxy=host:port
export https_proxy=$http_proxy
```

### How To Fix “Device eth0 does not seem to be present, delaying initialization” Error 
Problem:
```
# ifup eth0
Device eth0 does not seem to be present, delaying initialisation
```

Solution:
* `rm /etc/udev/rules.d/70-persistent-net.rules`
* 删除`/etc/sysconfig/network-scripts/ifcfg-eth0`的`HWADDR`和`UUID`。

References:
* http://www.unixmen.com/fix-device-eth0-seem-present-delaying-initialization-error/

### route add
```
ping 10.11.12.101
ls /etc/sysconfig/network-scripts/
cat /etc/sysconfig/network-scripts/ifcfg-em2:0
ifup em2:0
cat /etc/rc.local
#!/bin/sh
#
# This script will be executed *after* all the other init scripts.
# You can put your own initialization stuff in here if you don't
# want to do the full Sys V style init stuff.

touch /var/lock/subsys/local

route add -net 192.168.10.0/24 gw 192.168.18.1 metric 60 dev em2
route add -net 10.11.0.0/16 gw 10.11.11.1 metric 60 dev em2
route add -net 192.168.60.0/24 gw 10.11.11.1 metric 60 dev em2

sudo service network restart
vi /etc/sysconfig/network
```


## 时区一致

```
sudo cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

```
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```



## NTP
### 安装和配置
```
yum install ntp
```

对于master节点，修改配置文件，修改server值为对时中心，注释掉默认的server：
```
/etc/ntp.conf
server 2.cn.pool.ntp.org
server 3.asia.pool.ntp.org
server 0.asia.pool.ntp.org
# server 0.centos.pool.ntp.org iburst
# server 1.centos.pool.ntp.org iburst
# server 2.centos.pool.ntp.org iburst
# server 3.centos.pool.ntp.org iburst
```

对于slave节点，修改配置文件，修改server值为master节点，注释掉默认的server：
```
vi /etc/ntp.conf
server master
# server 0.centos.pool.ntp.org iburst
# server 1.centos.pool.ntp.org iburst
# server 2.centos.pool.ntp.org iburst
# server 3.centos.pool.ntp.org iburst
```

### 启动NTP同步时间
启动ntpd之前，需要先手动同步时间(用`ntpdate`命令)，使得我们机器的时间尽量接近标准时间，有利于ntpd与上一层服务器的对时。可以用ntpdate命令手动更新时间，保险起见可以运行2次。原因如下：
* 根据NTP的设置，如果你的系统时间比正确时间要快的话那么NTP是不会帮你调整的，所以要么你把时间设置回去，要么先做一个手动同步。
* 当你的时间和NTP服务器的时间相差很大的时候，NTP会花上较长一段时间才调整到位，手动同步可以使初始时间差很小从而减少这段时间。

在master节点，手动同步时间（至少2次）：
```
ntpdate -u 2.cn.pool.ntp.org
```

在master节点，启动NTP服务器：
```
service ntpd start
```

在slave节点，手动同步时间（至少2次）：
```
ntpdate -u master
```

手动同步slave时间时注意：
* master的ntpd启动后，大约要3－5分钟客户端才能与服务器建立正常的通讯连接，因此客户端有可能无法立即更新时间，提示错误`no server suitable for synchronization found`，等待一会儿再更新即可。
* 有可能防火墙会阻碍更新时间（封了123端口），这时可以加上`-u`参数。

在slave节点，启动ntpd：
```
service ntpd start
```

用ntpstat命令查看各个节点的同步状态，若为如下信息则已经完成时间同步。这个需要花费几分钟时间，需耐心等待。
```
ntpstat
synchronised to NTP server (202.112.31.197) at stratum 3
   time correct to within 1179 ms
   polling server every 64 s
```

另一个查看ntp状态的命令ntpq：
```
watch ntpq -p
```

最后，设置开机启动
```
chkconfig ntpd on
```

### 关于NTP的详细配置可以参考
* [Linux NTP配置详解 (Network Time Protocol) ](http://blog.csdn.net/iloli/article/details/6431757)
* [服务器托管中cnetos或linux NTP服务器搭建及内部服务器时间同步](http://www.9qu.com/news/detail.php?itemid=606)
* [China — cn.pool.ntp.org](http://www.pool.ntp.org/zone/cn)


配置NTP。详见http://www.cloudera.com/content/cloudera/en/documentation/core/latest/topics/install_cdh_enable_ntp.html

```
sudo yum install ntp
sudo vi /etc/ntp.conf
server 192.168.22.1        # 注释掉原有的server，添加新的server
sudo ntpdate 192.168.22.1  # 手动同步时间，至少执行2次
sudo service ntpd start
ntpstat                                     # 检查时间是否已经同步，如果出现以下信息则说明已同步
synchronised to NTP server (192.168.22.1) at stratum 4 
   time correct to within 1108 ms
   polling server every 64 s
sudo chkconfig ntpd on             # 设置开机启动
chkconfig --list ntpd
```


## yum
References:
* http://xmodulo.com/2013/07/how-to-fix-yum-errors-on-centos-rhel-or-fedora.html

### Fix 404 errors
Symptom: When you try to install a package with yum, yum complains that the URLs for repositories are not found, and throws 404 errors, as shown below.

You can get these 404 errors when the metadata downloaded by yum has become obsolete. To repair yum 404 errors, clean yum metadata as follows.
```
$ sudo yum clean metadata
```

Or you can clear the whole yum cache:
```
$ sudo yum clean all 
```

### Another app is currently holding the yum lock
```
rm -f /var/run/yum.pid
```

### Creating a Local Yum Repository
```
yum install yum-utils createrepo
cd /root/software
reposync -r cloudera-cdh5
cd <parent of RPMS>
createrepo .
```

References:
* http://www.cloudera.com/content/cloudera/en/documentation/core/latest/topics/cdh_ig_yumrepo_local_create.html

### Install newer software
see more at http://wiki.centos.org/AdditionalResources/Repositories/SCL

### 安装国内镜像
阿里云Linux安装镜像源地址：http://mirrors.aliyun.com/

CentOS系统更换软件安装源
第一步：备份你的原镜像文件，以免出错后可以恢复。

```
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
```

第二步：下载新的CentOS-Base.repo 到/etc/yum.repos.d/

```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
```

第三步：运行yum makecache生成缓存

```
yum makecache
```

网易开源镜像站:http://mirrors.163.com/

CentOS系统更换软件安装源 

第一步：备份你的原镜像文件，以免出错后可以恢复。 

```
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
```

第二步：下载新的CentOS-Base.repo 到/etc/yum.repos.d/

```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS6-Base-163.repo
```

第三步：运行以下命令生成缓存
  
```
yum clean all
yum makecache
```

其他镜像：

* 中科大的Linux安装镜像源：http://centos.ustc.edu.cn/
* 搜狐的Linux安装镜像源：http://mirrors.sohu.com/

references:

* [Centos修改镜像为国内的阿里云源或者163源等国内源](http://www.ruooo.com/VPS/594.html)

## File System

### mount
文件系统用ext4，数据相关节点分区mount到`/data`，并使用noatime。

```
mount
/dev/sdb on /data/1 type ext4 (rw,noatime)
/dev/sdc on /data/2 type ext4 (rw,noatime)
/dev/sdd on /data/3 type ext4 (rw,noatime)
/dev/sde on /data/4 type ext4 (rw,noatime)
```



### ulimit
Linux是有文件句柄限制的，而且Linux默认不是很高，一般都是1024，生产服务器用其实很容易就达到这个数量。
* Check: `ulimit -a`
* 可用ulimit命令来修改,但ulimit命令修改的数值只对当前登录用户的目前使用环境有效,系统重启或者用户退出后就会失效.
* 永久修改: `/etc/security/limits.conf`，或者修改`/etc/profile`增加`ulimit -HSn 65535`
* 硬限制是实际的限制，而软限制，是warnning限制，只会做出warning.其实ulimit命令本身就有分软硬设置，加`-H`就是硬，加`-S`就是软默认显示的是软限制，如果运行ulimit命令修改的时候没有加上的话，就是两个参数一起改变.

将ulimit的nofile改为65535

```
ulimit -n
65535
```

### swappiness
查看，默认值为60：
```
cat /proc/sys/vm/swappiness
```

临时改变，重启后回复默认值60。
```
sysctl vm.swappiness=0
```

永久改变：
```
vi /etc/sysctl.conf
vm.swappiness=0
```

解决方法：
```
sysctl vm.swappiness=0
echo 0 > /proc/sys/vm/swappiness
```
sysctl用来调整linux内核参数。

## 系统监控
```
yum install iptraf
```

## Misc
### /etc/environment 和 /etc/profile

http://blog.csdn.net/zhaogezhuoyuezhao/article/details/7326477


禁用SELinux

```
cat /etc/selinux/config | grep SELINUX=disabled
SELINUX=disabled
```

所有服务器新建非root账户：
```
sudo useradd admin
sudo passwd admin
123456
sudo vi /etc/sudoers.d/admin
%admin ALL=(ALL) NOPASSWD: ALL
```

### 配置无密码ssh
建立管理服务器到节点机器的无密码ssh登录：
```
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

如果出现ssh命令不存在则需要安装`openssh-clients`：
```
yum install openssh-clients
```


在master生成密钥对，一路回车即可
```
ssh-keygen -t rsa
```

将master公钥拷贝到需要无密码ssh的slave，注意文件权限：
```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

## Dev

### make

http://stackoverflow.com/questions/16018463/difference-in-details-between-make-install-and-make-altinstall

> install: altinstall bininstall maninstall
> altinstall skips creating the python link and the manual pages links, while install will hide the system binaries and manual pages.