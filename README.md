# git-check

A simple python app that check if remote git repos' list, have new commit since last check.<br />
It use `git ls-remote https:/git...` command.<br />
I wrote this utility to avoid manually check of every git repo that I compile using AUR PKGBUILD.<br />

```
usage: git-check.py [-h] [-v] [-c] jsonfile

positional arguments:
  jsonfile          a json file with a git repos list to check (a backup copy file is made before update the file itself)

options:
  -h, --help        show this help message and exit
  -v, --verbose     show commits info while checking git repos
  -c, --check_only  do not update filename (and do not create the backup file) with updated information
```

**Note 1:**
_*jsonfile.json*_ must be a json formatted file, e.g.: 

```
[
    {
        "Repo_Url": "https://github.com/user/software.git",
        "Last_Check": "0",
        "Current_Commit": "0"
    },
    {
        "Repo_Url": "https://gitlab.gnome.org/World/gnome-sw.git",
        "Last_Check": "0",
        "Current_Commit": "0"
    }
 ]
```

**Note 2:**<br />
When add a new git repo to the file, Last_Check and Current_Commit keys can be any numeric value.<br />
These values will be overwritten,with correct data,after first run script unless you use the `--check_only` argument.

![Screenshot](https://raw.github.com/dasnoopy/git-check/main/screenshot.png)
