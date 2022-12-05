# git-check

A simple python app that check if remote git repos' list, have new commit since last check.<br />
It use `git ls-remote https:/git...` command.<br />

```
$./git-check.py repos.json -h
usage: git-check.py [-h] [-v] [-c] [-l] [-a ADD_GIT] [-r ENTRY_POS] jsonfile

positional arguments:
  jsonfile              a json file with a git repos list to check

options:
  -h, --help            show this help message and exit
  -v, --verbose         show more commit info while checking git repos
  -c, --check-only      do not update commit info in the json file and do not create the backup file
  -l, --list            show list of git repos defined in the json file and days since latest commit
  -a ADD_GIT, --add ADD_GIT
                        append a new git url entry in the json file
  -r ENTRY_POS, --remove ENTRY_POS
```

**Note 1:**
_*jsonfile*_ must be a json formatted file, e.g.: 

**Note 2:**
Before start using **git-check**, create new empty file with this simple command:
```
$ echo '[]' > filename.json
```
 
then start to add git url with:
```
$ ./git-check filename.json -a https://github.repo.to.check.git
```
 
**A screenshot:**<br />
![Screenshot](https://raw.github.com/dasnoopy/git-check/main/screenshot.png)
