# macOS Cookbook

## Overview
* System Admin
* Tools Overview
* Tool Cookbooks

## System Admin

### ssh
```
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
sudo launchctl list | grep ssh
```

### netstat
```
netstat -an | grep 3306
```

### lsof
```
lsof -i:80
```

-i参数表示网络链接，:80指明端口号，该命令会同时列出PID，方便kill

### NTFS

```
sudo mkdir /Volumes/NTFS
sudo mount_ntfs -o rw,auto,nobrowse,noowners,noatime /dev/disk2s1 /Volumes/NTFS
```

```
brew cask install osxfuse
brew install ntfs-3g
sudo /usr/local/bin/ntfs-3g /dev/disk2s1 /Volumes/NTFS -olocal -oallow_other
```

other:

```
diskutil
```

see more at: 
* https://apple.stackexchange.com/questions/20889/how-do-i-write-to-ntfs-drives-in-os-x
* https://www.makeuseof.com/tag/solving-the-read-only-external-hard-drive-problem-on-your-mac/

### 设置文件关联
为了统一修改该类型的所有文件的打开方式，需要在某个文件上 右键 - 显示简介 - 打开方式 - 选择程序 - 然后切记点击下面的 全部修改 按钮，否则只是修改了这个文件的打开方式。

## Tools Overview
Popular tools:

* Terminal & Shell & SSH
  * iTerm2
  * oh-my-zsh
* Package management
  * Homebrew
  * Homebrew Cask装App Store里没有的软件
* UX
  * Alfred
  * Bartender
  * Moom: Move and zoom windows
* Microsoft Office
* Chrome
  * Dark Reader
  * SwitchySharp
* zip/unzip
  * iZip Unarchiver
* Networking
  * lrzsz
  * Thunder: for file download
  * ShadowsocksX
  * SecureCRT
* Multimedia
  * VLC
  * Elmedia Player
  * OmniGraffle
  * Jietu
* Text editor
  * Sublime
* JDK
* IDE
  * JetBrains Toolbox to install IntelliJ IDEA and more
  * IntelliJ IDEA
* MySQL
  * Install with Homebrew
  * Sequel Pro: MySQL Client
* Docker for Mac
* Dash: API Documentation Browser and Code Snippet Manager
* StarUML

Reference:
* [程序员如何优雅地使用 macOS？](https://www.zhihu.com/question/20873070)

## iTerm2 & oh-my-zsh
### Shortcut
* delete word: esc + delete
* delete/restore line: ctrl + U, ctrl + Y

see more:
* https://medium.com/@jonnyhaynes/jump-forwards-backwards-and-delete-a-word-in-iterm2-on-mac-os-43821511f0a
* https://stackoverflow.com/questions/15733312/iterm2-delete-line

### Theme
* iTerm2使用Solarized Dark主题
* iTerm2使用Powerline fonts, 不然使用oh-my-zsh的agnoster主题时会有乱码
* oh-my-zsh使用agnoster主题

see more:
* https://xiaozhou.net/learn-the-command-line-iterm-and-zsh-2017-06-23.html
* http://www.cnblogs.com/xishuai/p/mac-iterm2.html

### ZModem Integration

see more:
* https://github.com/mmastrac/iterm2-zmodem

## Homebrew

### invalid active developer path after macOS upgrade

```
sudo xcode-select --install
```

see more:
* https://apple.stackexchange.com/questions/209624/how-to-fix-homebrew-error-invalid-active-developer-path-after-upgrade-to-os-x

## Alfred

see more:
* http://wellsnake.com/jekyll/update/2014/06/15/001/

## Sublime
在新标签页打开文件可以在设置里面找到open_files_in_new_window并改为false：

```
"open_files_in_new_window": false，
```

## JDK
https://docs.oracle.com/javase/8/docs/technotes/guides/install/mac_jdk.html

## MySQL

Uninstall mysql
* http://community.jaspersoft.com/wiki/uninstall-mysql-mac-os-x

Install MySQL on macOS Sierra via homebrew
* https://gist.github.com/nrollr/3f57fc15ded7dddddcc4e82fe137b58e
* https://coolestguidesontheplanet.com/get-apache-mysql-php-and-phpmyadmin-working-on-macos-sierra/

```
==> Downloading https://homebrew.bintray.com/bottles/mysql-5.7.18_1.sierra.bottle.tar.gz
######################################################################## 100.0%
==> Pouring mysql-5.7.18_1.sierra.bottle.tar.gz
Error: The `brew link` step did not complete successfully
The formula built, but is not symlinked into /usr/local
Could not symlink lib/pkgconfig/mysqlclient.pc
/usr/local/lib/pkgconfig is not writable.

You can try again using:
  brew link mysql
==> Using the sandbox
==> /usr/local/Cellar/mysql/5.7.18_1/bin/mysqld --initialize-insecure --user=cmao --basedir=/usr/local/Cellar/mysql/5.7.
==> Caveats
We've installed your MySQL database without a root password. To secure it run:
    mysql_secure_installation

MySQL is configured to only allow connections from localhost by default

To connect run:
    mysql -uroot

To have launchd start mysql now and restart at login:
  brew services start mysql
Or, if you don't want/need a background service you can just run:
  mysql.server start
==> Summary
🍺  /usr/local/Cellar/mysql/5.7.18_1: 320 files, 232.9MB
```


```
sudo chown -R $(whoami) /usr/local
brew link mysql
```

sequel pro currently does not support mysql 8.0. it works to downgrade to mysql 5.7.

https://github.com/sequelpro/sequelpro/issues/2699

## Docker for Mac
Docker for Mac vs Docker tools
* Docker for Mac = Xhyve + Alpine + docker engine = for newer version mac
* Docker Tools includes Docker Machine = VirtualBox + boot2docker + engine = for older version mac

### StarUML

Contents/www/license/node/LicenseManagerDomain.js:

```
    function validate(PK, name, product, licenseKey) {
        var pk, decrypted;

        // edit by 0xcb
        return {
            name: "0xcb",
            product: "StarUML",
            licenseType: "vip",
            quantity: "bbs.chinapyg.com",
            licenseKey: "later equals never!"
        };

        ...
```

see more at: 
* http://www.chinapyg.com/thread-79022-1-1.html
