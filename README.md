# git-check

A simple python app that check if remote git repos' list, have new commit since last check.<br />
It use `git ls-remote https:/git...` command.<br />
I wrote this utility to avoid manually check of every git repo that I compile using AUR PKGBUILD.<br />

```
usage: git-check.py [-h] [--verbose] [--check-only] [--list] [--add ADD_GIT_URL] [--remove ENTRY_NUM] jsonfile

positional arguments:
  jsonfile            a json file with a git repos list to check

options:
  -h, --help          show this help message and exit
  --verbose           show commits info while checking git repos
  --check-only        do not update filename with last commit info
  --list              show git repos defined in the json file
  --add ADD_GIT_URL   append a new git url to check in the json file
  --remove ENTRY_NUM  delete entry nr. xx from the json file
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
When add a new git repo url to the json file, __Current_Commit__ keys have a "fake" id.<br />
This id will be overwritten with latest commit after first script execution, unless you use the `--check_only` argument.

![Screenshot](https://raw.github.com/dasnoopy/git-check/main/screenshot.png)
