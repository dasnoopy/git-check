# git-check

A simple python app that check if remote git repos' list, have new commit since last check.<br />
It use `git ls-remote https:/git...` command.<br />
I wrote this utility to avoid manual check of every git repo that I install using AUR PKGBUILD.<br />

```
$./git-check.py -h
usage: git-check.py [-h] [-v] [-c] [-l] [-a ADD_GIT_URL] [-r ENTRY_POS] jsonfile

Check latest commits change passing a list of git repos

positional arguments:
  jsonfile              a json file with a git repos list to check

options:
  -h, --help            show this help message and exit
  -v, --verbose         show more info while checking git repos
  -c, --check-only      do not update json file or create the backup file with updated info
  -l, --list            numbered list of git repos defined in the json file
  -a ADD_GIT_URL, --add ADD_GIT_URL
                        append a new git url entry in the json file
  -r ENTRY_POS, --remove ENTRY_POS
                        delete specific numbered entry from the json file
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
