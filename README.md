# git-check

```
usage: git-check.py [-h] [-v] [-c] filename.csv

positional arguments:
  file

options:
  -h, --help        show this help message and exit
  -v, --verbose
  -c, --check_only
```

**Note 1:**
_*filename.csv*_ must be a csv file with header, e.g. : 

| Repo Name | Last Check | Latest Commit |
| :---      | :---       | :---          |
|https://github.com/user/one_project.git|0|0
|https://github.com/user/another_project.git|0|0

**Note 2:**<br />
When add a new git repo to the file, Last_Check and Latest_Commit can be any numeric value.<br />
These values will be overwritten,with correct info,after first script run unless you use the `--check_only` argument.

![Screenshot](https://raw.github.com/dasnoopy/git-check/main/screenshot.png)
