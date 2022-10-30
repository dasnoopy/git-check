#!/usr/bin/python3

import os
import gi
import sys
import csv
import subprocess
import re
import datetime

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
fName='list_projects.csv'
verbose=True
checkonly=False

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print ()

# initial checking  time
adesso = datetime.datetime.now()
now = adesso.strftime("%d/%m/%Y_%H:%M:%S")

# open the file in read mode
filename = open(fName, 'r')

# creating dictreader object
dictName= csv.DictReader(filename)

# creating empty lists
repoList = []
checktime =[]
currentCommit = []

# iterating over each row and append
# values to empty list
for col in dictName:
	repoList.append(col['Repo_Name'])
	checktime.append(col['Last_Check'])
	currentCommit.append(col['Latest_Commit'])

index = 0
# set header for final list/multiline string to write in the text file
all_rows  = ['Repo_Name,Last_Check,Latest_Commit'] 

# some statistic header
print ('# Checking ' + str(len(repoList)) + ' remote git repos from file: ' + fName +'.')
print ('# Current check time: ' + colors.fg.red + now)
print (colors.reset)

# check latest commit for each repo using git ls-remote commaand
for repo_url in repoList:
	process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
	stdout, stderr = process.communicate()
	lastCommit = re.split(r'\t+', stdout.decode('ascii'))[0]
	print(colors.reset + '→ [' + str(index +1)+ '] git repo: ' + colors.fg.blue + colors.bold + repo_url)
	
	# update checking time
	adesso = datetime.datetime.now()
	now = adesso.strftime("%d/%m/%Y_%H:%M:%S")
	
	if currentCommit[index] != lastCommit:
		print(colors.fg.red + '✔ ...changes since last check (' + checktime[index] + ')' )
	else:
		print(colors.fg.green + '✔ ...no changes since last check (' + checktime[index] + ')' )
	# show commits info
	if verbose == True :
		print(colors.reset + '→ Previous commit : ' + colors.fg.orange + currentCommit[index])
		print(colors.reset + '→ Latest commit   : ' + colors.fg.lightcyan + lastCommit)

	print (colors.reset)
	all_rows.append(repo_url+',' + now + ','+lastCommit)
	index += 1

filename.close()

# write the file
# but befonre convert all_rows list in a multiline string
if checkonly == False :
	result = '\n'.join(all_rows)

	with open(fName, 'w') as filename:
		filename.writelines(result)
		filename.close()

# TODO list
# parametro -v --verbose per stampare  righe commit
# parametro -c --check-only per controllare ma non aggiornare il file con la lista dei repo, con ultimo commit
# parametro -l --list usa una lista da un percorso e nome che si vuole es -l /home/andrea/dati/gitrep.txt
# indentatura migliore usare main e def+
#lista repo non viene trovata se si lancia script con path assoluto

    # storing current date and time
   # current_date_time = datetime.now()
   #https://www.geeksforgeeks.org/how-to-add-timestamp-to-csv-file-in-python/