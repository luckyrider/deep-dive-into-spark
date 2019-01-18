# Docker dataplatformbase

dataplatformbase

```
docker run -itd --name dataplatformbase -v /opt/provision:/opt/provision centos:centos6
```

```
docker attach dataplatformbase
```

```
yum install -y sudo
yum install -y openssh-server openssh-clients
chkconfig --list sshd
chkconfig sshd on
service sshd start
```

create a user:

```
useradd admin
passwd admin
123456
vi /etc/sudoers.d/admin
%admin ALL=(ALL) NOPASSWD: ALL
su - admin
```

setup passphraseless ssh

```
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

set time zone

```
sudo cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

install dev tools:

```
sudo yum groupinstall -y development
sudo yum install -y cmake zlib-devel openssl-devel bats sqlite-devel bzip2-devel tcl-devel tk-devel ncurses-libs gdbm-devel readline-devel
```

install jdk:

```
sudo rpm -ih /opt/provision/centos-base/java/jdk-8u60-linux-x64.rpm
```


install protobuf:

```
tar -xf /opt/provision/centos-base/protobuf/protobuf-2.5.0.tar.gz -C ~/
cd protobuf-2.5.0/
./configure
make
sudo make install
```

install python 2.7.10 and virutalenv:

```
# Install Python 2.7
tar -xf /opt/provision/centos-base/python/Python-2.7.10.tgz -C ~/
cd ~/Python-2.7.10
./configure --prefix=/usr/local/python-2.7.10
make
sudo make altinstall

# Install pip
sudo /usr/local/python-2.7.10/bin/python2.7 /opt/provision/centos-base/python/get-pip.py

# Install virtualenv
sudo /usr/local/python-2.7.10/bin/pip install virtualenv

# Create 2.7.10 virtualenv
mkdir ~/.virtualenv
/usr/local/python-2.7.10/bin/virtualenv ~/.virtualenv/python-2.7.10

# activate python 2.7.10
source ~/.virtualenv/python-2.7.10/bin/activate
```

install mysql

```
sudo rpm -ivh /opt/provision/centos-base/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-shared-5.6.26-1.el6.x86_64.rpm
sudo rpm -ivh /opt/provision/centos-base/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-client-5.6.26-1.el6.x86_64.rpm
sudo yum install -y libaio
sudo rpm -ivh /opt/provision/centos-base/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-server-5.6.26-1.el6.x86_64.rpm

sudo cat /root/.mysql_secret
sudo service mysql start
mysql -uroot -p
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('123456');
quit
sudo service mysql restart

sudo chkconfig mysql off
chkconfig --list mysql
```

