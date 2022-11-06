#!/usr/bin/python3
#
# git-check by Andrea Antolini


# TODO list / improvement
# some error management
# -a : add a git repo entry in filename.json
# -r : remove git repo entry passing index e.g  -r 2
# -s : show repolist with index

import os
import sys
import json
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
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='show commits info while checking git repos')
parser.add_argument('-c', '--check_only', action='store_true', dest='check_only', help='do not update filename with last commit info')
parser.add_argument('jsonfile', type=pathlib.Path, help='a json file with a git repos list to check')
args = parser.parse_args()

fName=str(args.jsonfile)
verbose=args.verbose
checkonly=args.check_only

# initial checking  time
def orario ():
	return datetime.datetime.now()#.strftime("%d-%b-%Y %H:%M:%S")

def check_repos():
	# open the file in read mode
	try:
		with open(fName, 'r', encoding='utf-8') as filename:
				#jsonContent = filename.read()
				lista =json.loads(filename.read()) # populate dict 'lista'
	except FileNotFoundError as error:
		print (colors.fg.orange + colors.bold + 'Error: ' + fName.upper() + ' not found!' + colors.reset + ' Please check filename or path.')
		print (colors.reset)
		sys.exit()

	# create a backup of original file unless -c is passed
	if not checkonly :
		tempTuple = os.path.splitext(fName)
		bName = tempTuple[0] + '.bak'
		shutil.copyfile(fName, bName)

	# some init variables
	changed = 0
	not_changed = 0
	start_time = orario()

	# print some initial statistics
	print (colors.bold + '❯❯ ' + str(len(lista)) + ' remote git repos found in the file: ' + colors.fg.purple + fName)
	print (colors.reset + '❯❯ current check time: ' + colors.fg.purple + start_time.strftime("%d-%b-%Y %H:%M:%S"))
	print (colors.reset)
	print (colors.reset + '❯❯ checking for any change since last time:')
	print (colors.reset)
	# check latest commit for each repo using git ls-remote command
	for indice, x in enumerate(lista):
		repo_url = (lista[indice]['Repo_Url'])
		last_check = (lista[indice]['Last_Check'])
		current_commit = (lista[indice]['Current_Commit'])
		# print some initial info:

		print(colors.reset + '➜ ' + repo_url + ' [ ] ', end='\r') # \r  next print overwrite this output
		# get latest comming with : git ls-remote url
		process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
		stdout, stderr = process.communicate()
		last_commit = re.split(r'\t+', stdout.decode('ascii'))[0]
		
		if current_commit != last_commit:
			changed += 1
			lista[indice]['Current_Commit'] = last_commit # update commit
			print(colors.reset + '➜ ' + colors.fg.red + repo_url + ' [✘] ')
			#print(colors.fg.red + '✔ ...some changes since last time: ' + colors.bold + last_check)
		else:
			not_changed += 1
			print(colors.reset + '➜ ' + colors.fg.green + repo_url + ' [✔] ')
			#print(colors.fg.green + '✔ ...no changes since last check: ' + colors.bold + last_check)
		
		# show commits info if -v is passed
		if verbose :
			print(colors.reset + '    ➜ last check on: ' + colors.fg.purple + colors.bold + last_check)
			print(colors.reset + '    ➜ stored commit: ' + colors.bold + colors.fg.lightcyan + current_commit)
			print(colors.reset + '    ➜ latest commit: ' + colors.bold + colors.fg.yellow + last_commit)

		# update last_check value with current date/time
		lista[indice]['Last_Check'] = orario().strftime("%d-%b-%Y %H:%M:%S")
		#end loop trought dict dataset

	# close the file after all operations
	filename.close()
	# print some final statistics
	stop_time=orario()
	delta_time=stop_time - start_time
	print (colors.reset)
	print (colors.reset + f'❯❯ check completed in {delta_time.total_seconds()} sec. ' + colors.fg.red + str(changed) + colors.reset + ' repos changed. ' + colors.fg.green + str(not_changed) + colors.reset + ' repos not changed.')

	# dump updated dict 'lista' into the json file unless -c is passed
	if not checkonly :
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
			filename.close()

# main program
if __name__ == '__main__':
	check_repos()
	print (colors.reset)
	sys.exit()
