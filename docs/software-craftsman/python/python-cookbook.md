# Python Cookbook

## Overview
* install python
* package management

References:

* https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4
* http://bicofino.io/2014/01/16/installing-python-2-dot-7-6-on-centos-6-dot-5/

## Install python


## Package management
* https://packaging.python.org/en/latest/installing

### how to get python package
https://pypi.python.org/pypi

To use a package from this index:

* either "pip install package" (get pip) 
* or download, unpack and "python setup.py install" it

pip is the recommended installer. There are a few cases where you might want to use easy_install instead of pip.

### install pip

```
wget get-pip.py
python get-pip.py
```

Install pip on mac

```
sudo easy_install pip

Adding pip 7.1.2 to easy-install.pth file
Installing pip script to /usr/local/bin
Installing pip2.7 script to /usr/local/bin
Installing pip2 script to /usr/local/bin

Installed /Library/Python/2.7/site-packages/pip-7.1.2-py2.7.egg
```

### isolation via virtual environments
https://virtualenv.pypa.io/en/latest/

Python “Virtual Environments” allow Python packages to be installed in an isolated location for a particular application, rather than being installed globally.

Currently, there are two viable tools for creating Python virtual environments: virtualenv and pyvenv. pyvenv is only available in Python 3.3 & 3.4, and only in Python 3.4, is pip & setuptools installed into environments by default, whereas virtualenv supports Python 2.6 thru Python 3.4 and pip & setuptools are installed by default in every version.

```
sudo pip install virtualenv
```

```
$ mkdir ~/.virtualenvs
$ virtualenv ~/.virtualenvs/dev
New python executable in ~/.virtualenvs/dev/bin/python
Installing setuptools, pip, wheel...done.
$ source ~/.virtualenvs/dev/bin/activate
$ python -V
Python 2.7.10
$ which python
~/.virtualenvs/dev/bin/python
```

