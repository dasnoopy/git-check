#!/usr/bin/python3
#
# git-check by Andrea Antolini
#
import os
import sys
import csv
import subprocess
import re
import datetime
import argparse
import pathlib
import shutil
import errno

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

# clean screen 
os.system('clear')

# passing arguments and/or define some variabiles
# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='show commits info')
parser.add_argument('-c', '--check_only', action='store_true', dest='check_only', help='do not update filename with last commit info')
parser.add_argument('filename', type=pathlib.Path, help='a csv formatted text file with a list of git repos to check')
args = parser.parse_args()

#print('verbose is', args.verbose)
#print('check_only is', args.check_only)
#print('filename  is', args.file)

fName=str(args.filename)
verbose=args.verbose
checkonly=args.check_only

# initial checking  time
def orario ():
	return datetime.datetime.now().strftime("%d-%b-%Y/%H:%M:%S")

def check_repos():
	# open the file in read mode
	try:
		filename = open(fName, 'r')
	except FileNotFoundError as error:
		print (colors.fg.red + 'Error: '+ colors.reset + 'file [ ' + fName + ' ] not found! Please check filename or path.')
		print (colors.reset)
		sys.exit()

	# create a backup of original file unless -c is passed
	if checkonly == False :
		tempTuple = os.path.splitext(fName)
		bName = tempTuple[0] + '.bak'
		shutil.copyfile(fName, bName)

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
		currentCommit.append(col['Current_Commit'])

	index = 0
	changed = 0
	not_changed = 0

	# set header for final list/multiline string to write in the text file
	all_rows  = ['Repo_Name,Last_Check,Current_Commit'] 

	# some initial statistics
	print (colors.bold + '❯ Checking ' + str(len(repoList)) + ' remote git repos from file: ' + colors.fg.purple + fName)
	print (colors.reset + '❯ Current check time: ' + colors.fg.purple + orario() )
	print (colors.reset)

	# check latest commit for each repo using git ls-remote command
	for repo_url in repoList:
		process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
		stdout, stderr = process.communicate()
		lastCommit = re.split(r'\t+', stdout.decode('ascii'))[0]
		print(colors.bold + colors.fg.lightblue + '→ ' + '[' + str(index + 1)+ '] ' + colors.reset + colors.fg.blue + repo_url)
		
		if currentCommit[index] != lastCommit:
			changed += 1
			print(colors.fg.red + '✔ ...some changes since last check: ' + colors.bold + checktime[index])
		else:
			not_changed += 1
			print(colors.fg.green + '✔ ...no changes since last check: ' + colors.bold + checktime[index])
		
		# show commits info
		if verbose == True :
			print(colors.reset + '→ Stored commit: ' + colors.bold + colors.fg.lightcyan + currentCommit[index])
			print(colors.reset + '→ Latest commit: ' + colors.bold + colors.fg.yellow + lastCommit)

		print (colors.reset)
		# append rows
		all_rows.append(repo_url+',' + orario() + ','+lastCommit)
		index += 1

	# close the file after all operations
	filename.close()
	# some final statistics
	print (colors.reset + '❯ Check is over. ' + colors.fg.red + str(changed) + colors.reset + ' repos changed. ' + colors.fg.green + str(not_changed) + colors.reset + ' repos not changed.')

	# update the file unless -c is passed
	# but, before, convert all_rows list in a multiline string
	if checkonly == False :
		# join all rows and add a newline at the end of dict
		result = '\n'.join(all_rows)
		result = (result + ('\n'))
		# update the current file
		with open(fName, 'w') as filename:
			filename.writelines(result)
			filename.close()

# main program
if __name__ == '__main__':
	check_repos()
	sys.exit()

# TODO list
# some error management