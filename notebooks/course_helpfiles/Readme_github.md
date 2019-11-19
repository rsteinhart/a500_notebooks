# the pull request workflow

## initial setup

0) log into your github account

1) visit https://github.com/phaustin/a500_notebooks and hit the fork button to fork my repository

2) clone your fork to your local machine

    git clone https://github.com/yourname/a500_notebooks.git

3) `git remote -vv` on your computer should show a remote calle "origin" pointing to your fork

4) add my remote as "upstream" with the following command

     git remote add upstream https://github.com/phaustin/a500_notebooks.git

5) fetch my remote to your machine:

     git fetch upstream

6)  create a new branch with your initials

     git checkout -b your_initials

7)  push your branch up to your fork

     git push origin your_initials

8)  issue a pull request by checking out your branch on github and hitting the pull request button


## Day to day workflow

When I make changes on upstream master, you can incorporate those changes to your fork like this:

     git fetch upstream
     git checkout master
     git rebase upstream/master
     git push origin master

I recommend you always keep your own master identical with mine, and make changes to
a working branch. Once you've rebased origin master on upstream amster, you can  move
those changes to your branch like this:

     git checkout your_initials
     git rebase master
     git push origin your_initials

You can associate make your branches "tracking branches"  so that you
push does what you want by default

     git branch --set-upstream-to origin your_initials

after this then the push sequence from your branch would be:

     git checkout your_initials
     git rebase master
     git push

When you have changes you want me to see

1) make sure you have rebased on current upstream/master

2) push your branch with changes up to origin

3) issue a pull request on your branch


