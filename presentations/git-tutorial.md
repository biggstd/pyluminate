Learning Git
============

A brief overview of the installation of git, and regularly used commands.

By Tyler Biggs

[The official documentation and tutorial for git.](https://git-scm.com/docs/gittutorial)


Installing Git
--------------

There are several ways to install git. I will focus on Mac systems.

**Download the installer**

[Installer](http://sourceforge.net/projects/git-osx-installer/)

**Use Brew**

```
brew install git
```


Set up Github Account (Optional)
--------------------------------

**Identity** Most users will probably only ever need to set up the global configuraiton.

```
$ git config --global user.name "Tyler Biggs"
$ git config --global user.email biggstd@gmail.com
```


**View Config** You can view your settings.

```
$ git config --list
```

We are now ready to use git!


Creating a Repository
---------------------

Navigate to the desired parent folder that you wish to track and call:

```
$ git init
```

Importantly, this does not set up git to track anything within that directory.


Tracking Files in a Repository
------------------------------

**Add all files**
```
$ git add .
```

**Add all previously tracked files**
```
git add -u
```


Managing Branches
-----------------

A branch is a branch is a branch. Most git repositories have a `master` branch. This is
because `git init` creates this as a default branch.

**Show Branches**
```
git branch
```

**Create a new branch**
```
git branch <new_branch>
```

**Switch Branches**
```
git checkout <branch name>
```


**Merging Branches**
```
	  A---B---C topic
	 /
    D---E---F---G master
```

With current branch of `master`.


