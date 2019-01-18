# Macbook Cookbook

## Overview

as of 2017/05/27
* iTerm2
* oh-my-zsh
* JetBrains Toolbox
* IntelliJ IDEA
* Sublime
* SecureCRT 8.0.2
* MySQL (install with homebrew)
* Sequel Pro
* Docker for Mac
* OmniGraffle 7.2.1
* Microsoft Office
* Chrome (with dark reader, SwitchSharp)
* iZip Unarchiver (for 7z)
* ShadowsocksX
* Thunder (for file download)


## Network

### ssh

```
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
sudo launchctl list | grep ssh
```

### netstat
```
netstat -an | grep 3306
```

### osof
lsof -i:80

-i参数表示网络链接，:80指明端口号，该命令会同时列出PID，方便kill

## shadowsocks

### Using shadowsocks with Firefox
手动配置代理：

```
socks5 127.0.0.1 1080
```


or, 自动代理配置：

```
http://127.0.0.1:8090/proxy.pac
```

### Using shadowsocks with CLI tools
```
brew install proxychains-ng
vi /usr/local/etc/proxychains.conf
[ProxyList]
socks5  127.0.0.1 1080
```

```
proxychains4 curl google.com
proxychains4 git push origin master
```

proxify bash:

```
proxychains4 bash
curl google.com
git push origin master
```

see more at: https://github.com/shadowsocks/shadowsocks/wiki/Using-Shadowsocks-with-Command-Line-Tools

## SecureCRT
经试验，7.3.3可用。

先要执行以下脚本：

```
sudo perl /Volumes/SecureCRT\ 7.3.3\ by\ WaitsUn.com/securecrt_mac_crack.pl /Applications/SecureCRT.app/Contents/MacOS/SecureCRT
```

License data:

```
Name:          bleedfl
Company:       bleedfly.com
Serial Number: 03-29-002542
License Key:   ADGB7V 9SHE34 Y2BST3 K78ZKF ADUPW4 K819ZW 4HVJCE P1NYRC
Issue Date:    09-17-2013
```

see more at: http://www.waitsun.com/securecrt-7-3-3.html

Other Tips:

* 密码无法保存: 打开SecureCRT的全局选项，在主菜单Preferences（或者COMMAND键加逗号），取消掉Use Keychain即可。

## Tools

* 用Homebrew装开发工具链用
* Sublime Text
* 用iTerm 2 代替系统自带的Terminal
* sequel pro for mysql (free open source)
* Mou (markdown)
* OmniGraffle
* Homebrew Cask装所有Mac App Store里没有的软件
* 开发依赖复杂的项目时，不要直接在Mac系统中编译安装和搭建服务，而是使用Vagrant或者Docker（配合 docker-machine 和 docker-compose）
* 用Time Machine 做好备份
* RoboMongo for mongo

see more at: 

* http://www.zhihu.com/question/20873070
* http://chijianqiang.baijia.baidu.com/article/3733

## Misc

### prevent files in /tmp from being removed

`/etc/periodic.conf`:

```
daily_clean_tmps_enable="NO"
```

For more details:

* https://superuser.com/questions/187071/in-macos-how-often-is-tmp-deleted
* `/etc/defaults/periodic.conf`

### 设置文件关联
为了统一修改该类型的所有文件的打开方式，需要在某个文件上 右键 - 显示简介 - 打开方式 - 选择程序 - 然后切记点击下面的 全部修改 按钮，否则只是修改了这个文件的打开方式。

### Firefox

* 首选项 - 常规 - 启动firefox时 - 显示上次打开的窗口和标签页

### Sublime

* 在新标签页打开文件可以在设置里面找到open_files_in_new_window并改为false：
```
"open_files_in_new_window": false，
```

## Dev Tools
http://docs.oracle.com/javase/8/docs/technotes/guides/install/mac_jdk.html

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

see more at: http://www.chinapyg.com/thread-79022-1-1.html


