# git-check

A simple python app that check if remote git repo have new commit since last check time.<br />
I wrote this utility to avoid manually check of every git app I compile from AUR.<br />

```

usage: git-check.py [-h] [-v] [-c] filename

positional arguments:
  filename          a csv formatted text file with a list of git repos to check

options:
  -h, --help        show this help message and exit
  -v, --verbose     show commits info
  -c, --check_only  do not update filename with last commit info

```

**Note 1:**
_*filename.csv*_ must be a csv file with header, e.g. : 

| Repo_Name | Last_Check | Current_Commit |
| :---      | :---       | :---          |
|https://github.com/user/one_project.git|0|0
|https://gitlab.com/user/another_project.git|0|0

**Note 2:**<br />
When add a new git repo to the file, Last_Check and Current_Commit can be any numeric value.<br />
These values will be overwritten,with correct info,after first script run unless you use the `--check_only` argument.

![Screenshot](https://raw.github.com/dasnoopy/git-check/main/screenshot.png)
