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

_Note:_ **filename.csv** must be a csv file with header, e.g. : 

| Repo Name | Last Check | Latest Commit |
| :---      | :---       | :---          |
|https://github.com/user/one_project.git|0|0
|https://github.com/user/another_project.git|0|0


when add a new git repo to monitor, Last_Check and Latest_Commit can be any numeric value
correct value wil be overwritten after first script run unless you use the `--check_olny` argument.


