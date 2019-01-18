## CentOS

```
cat /etc/redhat-release
CentOS release 6.7 (Final)

# Set time zone
sudo cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# Setup passphraseless ssh
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys

# Fix puphpet/centos issues (https://github.com/puphpet/puphpet/issues/2321)
sudo yum -y remove centos-release-SCL
sudo yum -y install centos-release-scl

# Install dev libs, required to build python/hadoop/...
sudo yum groupinstall -y development
sudo yum install -y cmake zlib-devel openssl-devel bats sqlite-devel bzip2-devel tcl-devel tk-devel ncurses-libs gdbm-devel readline-devel
```

## Java

```
echo 'Install JDK'
# sudo rpm -ih /vagrant/provision/java/jdk-7u75-linux-x64.rpm
sudo rpm -ih /vagrant/provision/java/jdk-8u60-linux-x64.rpm
```

## Protocol Buffers

```
tar -xf /vagrant/provision/protobuf/protobuf-2.5.0.tar.gz -C ~/
cd protobuf-2.5.0/
./configure
make
sudo make install
```

## Python

```
# Install Python 2.7
tar -xf /vagrant/provision/python/Python-2.7.10.tgz -C ~/
cd ~/Python-2.7.10
./configure --prefix=/usr/local/python-2.7.10
make
sudo make altinstall

# Install pip
sudo /usr/local/python-2.7.10/bin/python2.7 /vagrant/provision/python/get-pip.py

# Install virtualenv
sudo /usr/local/python-2.7.10/bin/pip install virtualenv

# Create 2.7.10 virtualenv
mkdir ~/.virtualenv
/usr/local/python-2.7.10/bin/virtualenv ~/.virtualenv/python-2.7.10

# activate python 2.7.10
source ~/.virtualenv/python-2.7.10/bin/activate
```

## MySQL

```
echo 'Install MySQL'
sudo rpm -ivh /vagrant/provision/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-shared-compat-5.6.26-1.el6.x86_64.rpm
sudo rpm -e mysql-libs-5.1.73-5.el6_6.x86_64
sudo rpm -ivh /vagrant/provision/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-shared-5.6.26-1.el6.x86_64.rpm
sudo rpm -ivh /vagrant/provision/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-client-5.6.26-1.el6.x86_64.rpm
sudo rpm -ivh /vagrant/provision/mysql/MySQL-5.6.26-1.el6.x86_64.rpm-bundle/MySQL-server-5.6.26-1.el6.x86_64.rpm

echo 'change randomly generated root password'
sudo cat /root/.mysql_secret
sudo service mysql start
mysql -uroot -p
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('123456');
quit
sudo service mysql restart

sudo chkconfig mysql off
chkconfig --list mysql
```
