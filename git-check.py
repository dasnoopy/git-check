#!/usr/bin/python3

import os
import gi
import sys
import csv
import subprocess
import re

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class colors:
	reset = '\033[0m'
	bold = '\033[01m'
	disable = '\033[02m'
	underline = '\033[04m'
	reverse = '\033[07m'
	strikethrough = '\033[09m'
	invisible = '\033[08m'

	class fg:
		black = '\033[30m'
		red = '\033[31m'
		green = '\033[32m'
		orange = '\033[33m'
		blue = '\033[34m'
		purple = '\033[35m'
		cyan = '\033[36m'
		lightgrey = '\033[37m'
		darkgrey = '\033[90m'
		lightred = '\033[91m'
		lightgreen = '\033[92m'
		yellow = '\033[93m'
		lightblue = '\033[94m'
		pink = '\033[95m'
		lightcyan = '\033[96m'

	class bg:
		black = '\033[40m'
		red = '\033[41m'
		green = '\033[42m'
		orange = '\033[43m'
		blue = '\033[44m'
		purple = '\033[45m'
		cyan = '\033[46m'
		lightgrey = '\033[47m'

# pulizia screen e set dbname
os.system('clear')
# some variables
fName='list_projects.txt'
verbose=True


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print ()

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
	print(colors.reset + "→ Checking : " + colors.fg.blue + colors.bold + repo_url)
	
	if currentCommit[index] != lastCommit:
		print(colors.fg.red + '✔ ...git repo has been update since last check!')
		print(colors.reset)
	else:
		print(colors.fg.green + '✔ ...no changes from last check!')
		print(colors.reset)
# show commits info
	if verbose == True :
		print(colors.reset + 'Previous commit : ' + colors.fg.cyan + currentCommit[index])
		print(colors.reset + 'Latest commit   : ' + colors.fg.lightcyan + lastCommit)
		print(colors.reset)

	all_rows.append(repo_url+','+lastCommit)
	index += 1

filename.close()

#convert all_rows list in a multiline string
result = '\n'.join(all_rows)
# write the file
with open(fName, 'w') as filename:
   filename.writelines(result)
   filename.close()

# TODO list
# parametro -v --verbose per stampare le tre righe
# salvare e scrivere orario ultimo check  
