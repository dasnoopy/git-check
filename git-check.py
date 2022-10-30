import os
import gi
import sys
import csv
import subprocess
import re

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

# color
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END ='\033[0m'

# pulizia screen e set dbname
os.system('clear')
# some variables
fName='list_projects.txt'
verbose=False

# open the file in read mode
filename = open(fName, 'r')

# creating dictreader object
dictName= csv.DictReader(filename)

# creating empty lists
repoList = []
currentCommit = []

# iterating over each row and append
# values to empty list
for col in dictName:
	repoList.append(col['Repo_Name'])
	currentCommit.append(col['Latest_Commit'])

index = 0
# set header for final list/multiline string to write in the text file
all_rows  = ['Repo_Name,Latest_Commit'] 

# check latest commit for each repo using git ls-remote commaand
for repo_url in repoList:
	process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
	stdout, stderr = process.communicate()
	lastCommit = re.split(r'\t+', stdout.decode('ascii'))[0]
	print(color.END + "→ Checking : " + color.BLUE + color.BOLD + repo_url)
	
	if currentCommit[index] != lastCommit:
		print(color.RED + '✔ ...git repo has been update since last check!')
		print(color.END)
	else:
		print(color.GREEN + '✔ ...no changes from last check!')
		print(color.END)
# show commits info
	if verbose == True :
		print(color.END + 'Previous commit : ' + color.CYAN + currentCommit[index])
		print(color.END + 'Latest commit   : ' + color.DARKCYAN + lastCommit)
		print(color.END)

	all_rows.append(repo_url+','+lastCommit)
	index += 1

filename.close()

#convert all_rows list in a multiline string
result = '\n'.join(all_rows)
# write the file
with open(fName, 'w') as f:
   f.writelines(result)
   f.close()

# TODO list
# parametro -v --verbose per stampare le tre righe
# piu colori
# salvare e scrivere orario ultimo check  
