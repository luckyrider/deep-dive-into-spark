# Vagrant Cookbook

## Quickstart
### Introduction
Vagrant stands on the shoulders of giants. Machines are provisioned on top of VirtualBox, VMware, AWS, or any other provider. Then, industry-standard provisioning tools such as shell scripts, Chef, or Puppet, can be used to automatically install and configure software on the machine.

### Up and Running
Install Vagrant/VirtualBox: the latest version of Vagrant is 1.7.2. If you want to create your own base box, use 1.6.5 or 1.7.2 instead of 1.7.0/1.7.1.

1.7.0/1.7.1 issue and workaround:

* https://github.com/mitchellh/vagrant/issues/4960

Project setup (generate vagrantfile):

```
mkdir vagrant-quickstart
cd vagrant-quickstart
vagrant init hashicorp/precise32
```

Create and start VM (with VirtualBox headless processes):

```
vagrant up
```

Destroy VM:

```
vagrant destroy
```

Connect with SSH client, e.g. Putty.

* hostname: localhost
* port 2222
* user: vagrant
* password: vagrant

Access vagrant project from VM:

```
ls /vagrant
```

### Reference
* https://docs.vagrantup.com/v2/
* https://docs.vagrantup.com/v2/getting-started/index.html
* https://atlas.hashicorp.com/search
* [Vagrant 快速入门](http://blog.csdn.net/jillliang/article/details/8251242)

## Workflow
1. `vagrant init`: initialize vagrant environment, create Vagrantfile (i.e. config for VM)
2. `vagrant box add`: use existing box, or `vagrant package --base`: create a base box by yourself first
3. `vagrant up`: create guest VM for VirtualBox and start the VM
4. `vagrant halt`: stop the VM
5. `vagrant package --output`
5. `vagrant destroy`: remove guest VM from VirtualBox

## Vagrantfile
Vagrant actually loads a series of Vagrantfiles, merging the settings as it goes.

1. Vagrantfile packaged with the box that is to be used for a given machine.
2. Vagrantfile in your Vagrant home directory (defaults to `~/.vagrant.d`). This lets you specify some defaults for your system user.
3. Vagrantfile from the project directory. This is the Vagrantfile that you'll be modifying most of the time.
4. Multi-machine overrides if any.
5. Provider-specific overrides, if any.

## Defining Multiple Machines
Within each Vagrantfile, you may specify multiple Vagrant.configure blocks.

```
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "centos7"
end

# Define multiple machines below
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo Hello"

  config.vm.define "web" do |web|
    web.vm.box = "apache"
  end

  config.vm.define "db" do |db|
    db.vm.box = "mysql"
  end
end
```

## Creating a Base Box
### Within VirtualBox Install CentOS and Its Guest Additions
Install guest additions, easiest way is using Devices -> Install Guest Additions in the VM's GUI window. 

### Networking
Enable the network interface to auto start on the Boot and get dynamic ip, provided by vagrant: 

```
vi /etc/sysconfig/network-scripts/ifcfg-enp0s3
ONBOOT=yes
```

### Default User Settings
Create user vagrant:

```
useradd vagrant
passwd vagrant
```

Change root password to "vagrant", login as root:

```
passwd
vagrant
```

Change sudoers:

```
visudo
vagrant ALL=(ALL) NOPASSWD: ALL
# Defaults    requiretty
```

Add vagrant's public key so vagrant user can ssh without password:

```
mkdir .ssh
curl -k https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub > .ssh/authorized_keys
chmod 0700 .ssh
chmod 0600 .ssh/authorized_keys
```

### Vagrant Package
```
vagrant package --base my-virtual-machine
```

Where "my-virtual-machine" is replaced by the name of the virtual machine in VirtualBox to package as a base box.

1.7.0/1.7.1 have a bug, so use an older version. See more at:

* [Vagrant crashes without providing a useful error message when asked to package a base box #4931](https://github.com/mitchellh/vagrant/issues/4931)
* [Packaging base with 1.7.0 returns error: wrong number of arguments (2 for 1) (ArgumentError) #4936](https://github.com/mitchellh/vagrant/issues/4936)

### References
* [Creating a Base Box](http://docs.vagrantup.com/v2/boxes/base.html)
* http://docs.vagrantup.com/v2/virtualbox/boxes.html
* https://github.com/ckan/ckan/wiki/How-to-Create-a-CentOS-Vagrant-Base-Box

## Package
### CLI
`vagrant package`

* `--base NAME` - Instead of packaging a VirtualBox machine that Vagrant manages, this will package a VirtualBox machine that VirtualBox manages. NAME should be the name or UUID of the machine from the VirtualBox GUI.
* `--output NAME` - The resulting package will be saved as NAME. By default, it will be saved as package.box.
* `--include x,y,z` - Additional files will be packaged with the box. These can be used by a packaged Vagrantfile (documented below) to perform additional tasks.
* `--vagrantfile FILE` - Packages a Vagrantfile with the box, that is loaded as part of the Vagrantfile load order when the resulting box is used.

### About Networking
注意：不要在使用`private_network`或者`public_network`的VM上进行package操作。

根本原因是`70-persistent-net.rules`和`ifcfg-eth1`这两个文件里会包含过时的网卡信息，会导致冲突。具体说明见下面。

相关文件如下：
```
cat /etc/udev/rules.d/70-persistent-net.rules
ls /etc/sysconfig/network-scripts/ifcfg*
cat /etc/sysconfig/network-scripts/ifcfg-lo
cat /etc/sysconfig/network-scripts/ifcfg-eth0
cat /etc/sysconfig/network-scripts/ifcfg-eth1
```

`ifcfg-lo`和`ifcfg-eth0`是默认的network interface，其中`ifcfg-eth0`用作NAT网络，无论使用哪种vagrant网络，都是需要的。如果删除这两个，会导致vagrant无法进行初始的访问。
```
Clearing any previously set forwarded ports...
Fixed port collision for 22 => 2222. Now on port 2200.
Clearing any previously set network interfaces...
Preparing network interfaces based on configuration...
Adapter 1: nat
Forwarding ports...
8443 => 8443 (adapter 1)
22 => 2200 (adapter 1)
Booting VM...
Waiting for machine to boot. This may take a few minutes...
SSH address: 127.0.0.1:2200
SSH username: vagrant
SSH auth method: private key
Warning: Connection timeout. Retrying...
Warning: Connection timeout. Retrying...
Warning: Connection timeout. Retrying...
Warning: Connection timeout. Retrying...
Warning: Connection timeout. Retrying...
Warning: Connection timeout. Retrying...
Warning: Connection timeout. Retrying...
```

`ifcfg-eth1`以上用作host-only等，由vagrant自动生成以反映最新的网卡信息。证据如下：

```
cat /etc/sysconfig/network-scripts/ifcfg-eth1
#VAGRANT-BEGIN
# The contents below are automatically generated by Vagrant. Do not modify.
NM_CONTROLLED=no
BOOTPROTO=none
ONBOOT=yes
IPADDR=172.28.128.110
NETMASK=255.255.255.0
DEVICE=eth1
PEERDNS=no
#VAGRANT-END
```

`70-persistent-net.rules`在系统启动时自动生成，以反映最新的网卡信息。证据如下：

```
cat /etc/udev/rules.d/70-persistent-net.rules
This file was automatically generated by the /lib/udev/write_net_rules program, run by the persistent-net-generator.rules rules file.
```

如果package时存在这两个文件。则当vagrantfile配置了host-only时，vagrant会为VM增加一块网卡（第一块网卡是eth0，用作NAT）并生成（已存在则修改）`ifcfg-eth1`，另一方面，系统发现`70-persistent-net.rules`文件里`eth1`已经存在，系统会将这个host-only的adapter命名为eth2。示例如下：

```
cat /etc/udev/rules.d/70-persistent-net.rules
# This file was automatically generated by the /lib/udev/write_net_rules
# program, run by the persistent-net-generator.rules rules file.
#
# You can modify it, as long as you keep each rule on a single
# line, and change only the value of the NAME= key.

# PCI device 0x8086:0x100e (e1000)
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="08:00:27:ce:08:3d", ATTR{type}=="1", KERNEL=="eth*", NAME="eth0"

# PCI device 0x8086:0x100e (e1000)
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="08:00:27:5d:ce:2c", ATTR{type}=="1", KERNEL=="eth*", NAME="eth1"

# PCI device 0x8086:0x100e (e1000)
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="08:00:27:51:21:91", ATTR{type}=="1", KERNEL=="eth*", NAME="eth2"
```

这样的话，vagrant生成的`ifcfg-eth1`里的网卡叫`eth1`，而`70-persistent-net.rules`里`eth1`是老的网卡（实际的网卡应当是`eth2`），其MAC地址和vagrant创建的网卡地址不匹配，所以导致启动时找不到网卡。

```
Device eth1 does not seem to be present, delaying initialization.
```

## Provisioning
### Basic Usage
Provisioners in Vagrant allow you to automatically install software, alter configurations, and more on the machine as part of the vagrant up process.

Provisioning happens at certain points during the lifetime of your Vagrant environment:

* On the first vagrant up that creates the environment, provisioning is run. If the environment was already created and the up is just resuming a machine or booting it up, they won't run unless the `--provision` flag is explicitly provided.
* When vagrant provision is used on a running environment.
* When vagrant reload `--provision` is called. The `--provision` flag must be present to force provisioning.

You can also bring up your environment and explicitly not run provisioners by specifying `--no-provision`.

### Provisioner name: "file"
The file provisioner allows you to upload a file from the host machine to the guest machine.

### Provisioner name: "shell"
The shell provisioner allows you to upload and execute a script within the guest machine.

Shell provisioning is ideal for users new to Vagrant who want to get up and running quickly and provides a strong alternative for users who aren't comfortable with a full configuration management system such as Chef or Puppet.

### Ansible

### Puppet

### Chef

## Networking
3 modes:

* forwarded ports
* private network
* public network

e.g.

```
Vagrant.configure("2") do |config|
  # other config here

  config.vm.network "forwarded_port", guest: 80, host: 8080
end
```

e.g.

```
Vagrant.configure("2") do |config|
  config.vm.network "public_network"
end
```

* https://docs.vagrantup.com/v2/networking/basic_usage.html
* https://docs.vagrantup.com/v2/networking/public_network.html

## Other Tips
### SSH
You may add %GIT_HOME%/bin to PATH to let `vagrant ssh`work. Or you will get the following error.

```
vagrant ssh
`ssh` executable not found in any directories in the %PATH% variable
```

### puphpet/centos

(1) Cannot retrieve repository metadata (repomd.xml) for repository: scl

https://github.com/puphpet/puphpet/issues/2321

Problem:

```
sudo yum -y update
设置更新进程
http://mirror.centos.org/centos/6/SCL/x86_64/repodata/repomd.xml: [Errno 14] PYCURL ERROR 22 - "The requested URL returned error: 404 Not Found"
尝试其他镜像。
错误：Cannot retrieve repository metadata (repomd.xml) for repository: scl. Please verify its path and try again
```

solution:

```
sudo yum -y remove centos-release-SCL
sudo yum -y install centos-release-scl
```


