# VirtualBox Cookbook

## Networking
* 如果需要作为服务器供外部访问的话，可以配置为bridged network。不过，bridged network在某些网络环境中可能会有问题，比如无法从DHCP拿到IP地址，原因可能是DHCP服务器限制了1块网卡只能获得1个IP地址，安装VirtualBox的机器一般有两块网卡“以太网适配器 本地连接”和“以太网适配器 VirtualBox Host-Only Network”。比如：
  * ["Bridged Adapter" issue while running CentOS 6.3 on VirtualBox.](https://www.centos.org/forums/viewtopic.php?t=8230)
  * [VirtualBox bridged adapter not working under certain circumstances](http://superuser.com/questions/243549/virtualbox-bridged-adapter-not-working-under-certain-circumstances)
* 如果需要一个能互相访问的集群，同时又能访问internet，可以同时配置为Host only和NAT。

Referneces:

* [Chapter 6. Virtual networking](http://www.virtualbox.org/manual/ch06.html)

## Hard Disk
### Change Hard Disk UUID
Problem
```
Cannot register the hard disk ...because a hard disk with UUID already exists
```

Solution. `VBoxManage`位于`C:\Program Files\Oracle\VirtualBox`:
```
VBoxManage internalcommands sethduuid xxx.vmdk
```

## Guest Addition

### Shared Folder
device -> shared folder，注意不要选择自动挂载。
```
mkdir /mnt/share
sudo mount -t vboxsf share /mnt/share
```

## Toubleshooting

### unable to load R3 module

现象：

> unable to load R3 module C:\Program Files\Oracle\VirtualBox\VBoxDD.dll(VBoxDD): GetLastError=1790 (VERR_UNRESOLVED_ERROR).

原因：因为大多人使用的ghost系统都会破解uxtheme.dll文件，而在运行时要载入Virtualbox进程的模块都要进行校验，因为是破解版，所以导致virtualbox启动失败。

解决方法：将`c:\windows\system32\uxtheme.dll`改名，然后放入原版的`uxtheme.dll`。原版下载地址：`http://pan.baidu.com/s/1gdgTE63`


References:

* http://www.dotcoo.com/virtualbox-uxtheme
* http://blog.csdn.net/u014225510/article/details/45110849


