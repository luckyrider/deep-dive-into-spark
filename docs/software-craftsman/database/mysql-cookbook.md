# MySQL Cookbook
## Overview
* Mac安装和基本配置
* CentOS安装和基本配置
* Tips

## Mac安装和基本配置
download: 

* http://dev.mysql.com/downloads/mysql/

Install MySQL on macOS Sierra via homebrew

* https://gist.github.com/nrollr/3f57fc15ded7dddddcc4e82fe137b58e
* https://coolestguidesontheplanet.com/get-apache-mysql-php-and-phpmyadmin-working-on-macos-sierra/

Uninstall mysql

* http://community.jaspersoft.com/wiki/uninstall-mysql-mac-os-x

```
➜  ~ brew link mysql
Linking /usr/local/Cellar/mysql/5.7.18_1...
Error: Could not symlink lib/pkgconfig/mysqlclient.pc
/usr/local/lib/pkgconfig is not writable.
➜  ~
➜  ~ sudo brew link mysql
Password:
Error: Running Homebrew as root is extremely dangerous and no longer supported.
As Homebrew does not drop privileges on installation you would be giving all
build scripts full access to your system.

sudo chown -R $(whoami) /usr/local
```

https://sbaronda.com/2016/11/28/homebrew-disabling-auto-updating/

```
HOMEBREW_NO_AUTO_UPDATE=1 brew install xxx
```

```
/usr/local/mysql/bin/mysql -uroot -p
123456
```

references:

* [MySQL for Mac 安装和基本操作](http://blog.sina.com.cn/s/blog_9ea3a4b70101ihl3.html)

## CentOS安装
详见：http://dev.mysql.com/doc/refman/5.6/en/linux-installation-rpm.html

使用rpm安装

```
wget 
tar -xvf MySQL-5.6.26-1.el6.x86_64.rpm-bundle.tar
sudo yum install MySQL-shared-compat-5.6.26-1.el6.x86_64.rpm
sudo yum install MySQL-shared-5.6.26-1.el6.x86_64.rpm
sudo yum install MySQL-client-5.6.26-1.el6.x86_64.rpm
sudo yum install MySQL-server-5.6.26-1.el6.x86_64.rpm
```

如果仅仅需要mysqldump等客户端工具的话，不需要安装`MySQL-server-5.6.26-1.el6.x86_64.rpm`

修改随机生成的root密码：
```
sudo cat /root/.mysql_secret   # 获取MySQL安装时生成的随机密码
sudo service mysql start           # 启动MySQL服务
mysql -uroot -p                        # 进入MySQL，使用之前获取的随机密码
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('123456');  # 在MySQL命令行中设置root账户的密码
quit
sudo service mysql restart
```

安装好的MySQL已经设置为开机启动。
```
chkconfig --list mysql
mysql          	0:off	1:off	2:on	3:on	4:on	5:on	6:off
```

### Installing the MySQL JDBC Driver

* Install the JDBC driver on the Cloudera Manager Server host, as well as hosts to which you assign the Activity Monitor, Reports Manager, Hive Metastore Server, Sentry Server, Cloudera Navigator Audit Server, and Cloudera Navigator Metadata Server roles.
* Cloudera recommends that you assign all roles that require databases on the same host and install the driver on that host. Locating all such roles on the same host is recommended but not required.
* Do not use the yum install command to install the MySQL driver package, because it installs openJDK, and then uses the Linux alternatives command to set the system JDK to be openJDK.

```
tar zxvf mysql-connector-java-5.1.36.tar.gz
sudo mkdir -p /usr/share/java/
sudo cp mysql-connector-java-5.1.36/mysql-connector-java-5.1.36-bin.jar /usr/share/java/mysql-connector-java.jar
```


## Tips

### 命令行乱码
```
SHOW VARIABLES LIKE 'character_set%';
set SESSION character_set_results=utf8;
```

