# git-check

A simple python app that check if a remote git repos' list have new commit since last run of git-check itself.<br />
It use `git ls-remote https:/git...` command.<br />

```

$./git-check.py repos.json -h
usage: git-check.py [-h] [-v] [-c] [-l] [-s] [-a ADD_GIT] [-f FIND_TEXT] [-r ENTRY_POS] jsonfile

positional arguments:
  jsonfile              a json file with a git repos list to check

options:
  -h, --help            show this help message and exit
  -v, --verbose         show more commit info while checking git repos
  -c, --check-only      do not update commit info in the json file and do not create the backup
                        file
  -l, --list            show list of git repos defined in the json file and days since latest
                        commit
  -s, --sort            sort json objects by last change date key (ascending order) and update
                        the json file
  -a ADD_GIT, --add ADD_GIT
                        append a new git url entry in the json file
  -f FIND_TEXT, --find FIND_TEXT
                        find text in url entry
  -r ENTRY_POS, --remove ENTRY_POS
                        delete specific numbered entry from the json file

```

**Note:**
before start using **git-check**, create a new json file, e.g., from command shell with:
```
$ echo '[]' > filename.json
```
 
then start to add git url with:
```
$ ./git-check filename.json -a https://github.repo.to.check.git
```
 
**A screenshot:**<br />
![Screenshot](https://raw.github.com/dasnoopy/git-check/main/screenshot.png)
