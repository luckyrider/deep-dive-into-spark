# Git Cookbook

## Outline
* git fundamentals
* install and config
* operations
* github

## Git Fundamentals
best learning material is http://git-scm.com/book, Chinese version is also available at http://git-scm.com/book/zh/.

(1) Snapshots, No differences
Git 和其他版本控制系统的主要差别在于，Git 只关心文件数据的整体是否发生变化，而大多数其他系统则只关心文件内容的具体差异。这类系统（CVS，Subversion，Perforce，Bazaar 等等）每次记录有哪些文件作了更新，以及都更新了哪些行的什么内容。Git 并不保存这些前后变化的差异数据。实际上，Git 更像是把变化的文件作快照后，记录在一个微型的文件系统中。

(2) Three States
Git has three main states that your files can reside in: committed, modified, and staged. Committed means that the data is safely stored in your local database. Modified means that you have changed the file but have not committed it to your database yet. Staged means that you have marked a modified file in its current version to go into your next commit snapshot.

the three main sections of a Git project: the Git directory, the working directory, and the staging area.

(3) Branch, HEAD: 
A branch in Git is simply a lightweight movable pointer to one of these commits. The default branch name in Git is master. As you initially make commits, you’re given a master branch that points to the last commit you made. Every time you commit, it moves forward automatically.

How does Git know what branch you’re currently on? It keeps a special pointer called HEAD. In Git, this is a pointer to the local branch you’re currently on.

## Install and config

### install

```
yum install git
git --version
```

### Configure Git
specify username and email globally. Git saves your email address into the commits you make. We use the email address to associate your commits with your GitHub account.

```
git config --global user.name "Your Name Here"
# Sets the default name for git to use when you commit
git config --global user.email "your_email@example.com"
# Sets the default email for git to use when you commit
```

Overriding settings in individual repos by:

```
cd my_other_repo
# Changes the working directory to the repository you need to switch info for
git config user.name "Different Name"
# Sets the user's name for this specific repository
git config user.email "differentemail@email.com"
# Sets the user's email for this specific repository
```

password caching. The credential helper only works when you clone an HTTPS repository URL. If you use the SSH repository URL instead, SSH keys are used for authentication.

```
git config --global credential.helper cache
# Set git to use the credential memory cache
```

example:
```
git config user.name "halida9cxm"
git config user.email "halida9cxm@gmail.com"
git config credential.helper cache
```

Set http/https proxy:

```
git config --global http.proxy http://proxyuser:proxypwd@proxy.server.com:8080
git config --global https.proxy http://proxyuser:proxypwd@proxy.server.com:8080
```

If you decide at any time to reset this proxy and work without (no proxy) :
```
git config --global http.proxy "" or
git config --global --unset http.proxy
```

git and HTTPS (fatal: HTTP request failed)
```
git config --global http.sslverify false 
```
see more: http://blog.hqcodeshop.fi/archives/148-git-and-HTTPS-fatal-HTTP-request-failed.html

## Operations

### Getting a Git Repository
* Initializing a Repository in an Existing Directory
* Cloning an Existing Repository

### States and change management

states transition:

* `git add`: modified -> staged
* `git commit`: staged -> committed

view status:

    git status

view commit history:

    git log


### Working with Remotes

remote command:

```
git remote add <name> <url>
git remote show <name>
git remote remove <name>
```

add remote repos:

Make a new repository on GitHub: on GitHub website, click "New repository"

Create a new repository on the command line:

```
touch README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/halida9cxm/awesomedata.git
git push -u origin master
```

Access github via HTTPS instead of SSH as shown above, you will get an error

```
git push -u origin mastererror: The requested URL returned error: 403 Forbidden while accessing https://github.com/halida9cxm/awesomedata.git/info/refs

fatal: HTTP request failed
```

The solution is to add your GitHub username to your “remote.origin.url”.

```
git config -l | grep remote.origin.url
remote.origin.url=https://github.com/halida9cxm/awesomedata.git
git config remote.origin.url "https://halida9cxm@github.com/halida9cxm/awesomedata.git"
```

see more details at: http://mark.koli.ch/pushing-to-an-http-git-remote-ref-on-ubuntu-1004-lts-with-git-1704-403-inforefs

or, you can push an existing repository from the command line

```
git remote add origin https://github.com/halida9cxm/awesomedata.git
git push -u origin master
```

### pull
git clone will give you the whole repository

checkout master:

    git checkout master

checkout a branch:

    git clone -b <branch> <remote_repo>

checkout origin/master as a new branch:

    git checkout -b <new-branch> origin/master

check out a tag

```
git clone
git tag -l
git checkout tags/<tag_name>
```

pull in upstream changes:

```
git remote add upstream https://github.com/apache/mahout.git
git fetch upstream
git merge upstream/master
```
To discard changes in working directory:
```
git checkout -- <file>
git checkout -- <dir>
```

### push
push a repository

    git push -u origin master

What does git push -u mean? "Upstream" would refer to the main repo that other people will be pulling from, e.g. your GitHub repo. The -u option automatically sets that upstream for you, linking your repo to a central one. That way, in the future, Git "knows" where you want to push to and where you want to pull from, so you can use git pull or git push without arguments.

> git push error: RPC failed; result=56, HTTP code = 0

The problem is most likely because your git buffer is too low. You will need to increase Git’s HTTP buffer by setting.

    git config --global http.postBuffer 128M


### branch management

create a new branch and switch to that branch:

```
git checkout -b iss53
```

rename a branch

```
git branch -m <oldname> <newname>
```

If you want to rename the current branch, you can simply do:

```
git branch -m <newname>
```

e.g.:

```    
git branch -m hadoop220
```

rename remote branch:

```
git branch -m newname
git push origin newname
git push origin :oldname <- this will delete a remote branch
```

### merging
merge a hotfix back into master:

```
git checkout master
git merge hotfix
```

### file operations
rename

```
git mv <from> <to>
```

delete:

```
git rm <file>
```

warning: LF will be replaced by CRLF:

```
$ rm -rf .git  
$ git config --gobal core.autocrlf false
```

## GitHub

### GitHub Client
安装GitHub客户端，会同时安装Git Shell，使用起来类似于Linux的shell，比较方便。在当前用户主目录的.ssh下有`github_rsa`和`github_rsa.pub`，其中`github_rsa.pub`的内容可以上传到Gitlab的个人SSH Key里面。

### Collaborating with Issues and Pull Requests
https://help.github.com/categories/collaborating-with-issues-and-pull-requests/

### Manage assets

Push images to wiki git repo, then reference an image by the pattern

    https://raw.githubusercontent.com/wiki/[username]/[repository]/[path-to-file]/[filename]

e.g.:

    https://raw.githubusercontent.com/wiki/halida9cxm/workbench/images/OryxArchitecture.png

reference:

* http://stackoverflow.com/questions/10045517/embedding-images-inside-a-github-wiki-gollum-repository
* http://nerdwin15.com/2013/08/adding-images-to-github-wiki-repo/

use issues (this is an old workaround)

* http://solutionoptimist.com/2013/12/28/awesome-github-tricks/
