# Git Cookbook

## Tips
### Config user and email
```
git config user.name "seancxmao"
git config user.email "seancxmao@gmail.com"
```

### Keep a fork up-to-date

```
git remote add upstream https://github.com/apache/spark
git fetch upstream
git checkout master
git rebase upstream/master
git push
```

### Push the current branch and set the remote as upstream

```
git push --set-upstream origin <local_branch>
```

### Squash multiple commits into one
To squash five commits into one, do the following. In the text editor that comes up, replace the words "pick" with "squash" next to the commits you want to squash into the commit before it. If you've already pushed commits to GitHub, and then squash them locally, you will have to force the push to your branch.

```
git rebase -i HEAD~5
pick xxx
squash xxx
squash xxx
squash xxx
squash xxx
...
git push --force
```

### Backport to an older version:

```
git checkout my-topic-branch
git rebase --onto branch-2.3 my-topic-branch~4 my-topic-branch
# fix conflicts
git add/rm <conflicted_files>
git rebase --continue
```

### Undo a commit

```
git reset HEAD~
```

### Unstaged local changes (before you commit)
Discard all local changes, but save them for possible re-use later. 

```
git stash
```

Discarding local changes (permanently) to a file. 

```
git checkout -- <file>
```

Discard all local changes to all files permanently. 

```
git reset --hard
```

### Rename a local and remote branch
Rename your local branch. If you are on the branch you want to rename:

```
git branch -m new-name
```

If you are on a different branch:
```
git branch -m old-name new-name
```

Delete the old-name remote branch and push the new-name local branch.

```
git push origin :old-name new-name
```

Reset the upstream branch for the new-name local branch. Switch to the branch and then:

```
git push origin -u new-name
```

Compare file

```
git diff <branch_a> <branch_b> -- <file>
```

Modify commit message

```
git commit --amend
```

Checkout pull request and create a new branch

```
git fetch upstream pull/22378/head:pull-22378
```
