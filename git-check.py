#!/usr/bin/python3
#
# git-check by Andrea Antolini
# written for python 3.10.x

# TODO list / improvement
# check if url passed is valid
# better argument management

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
import secrets


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
## os.system('clear')
print(colors.reset,end='\r')

# passing arguments and/or define some variabiles
# Create the parser
# function to convert the input and 
# check a value or value range
def checker(a):
    num = int(a)
      
    if num < 1 :
        raise argparse.ArgumentTypeError('invalid value!!!')
    return num


parser = argparse.ArgumentParser()

parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
		help='show commits info while checking git repos')

parser.add_argument('--check-only', action='store_true', default=False, dest='check_only',
		help='do not update filename with last commit info')

parser.add_argument('--list', action='store_true', dest='list_urls',
		help='show git repos defined in the json file')

parser.add_argument('--add', action='store', dest='add_git_url',
		help='append a new git url to check in the json file')

parser.add_argument('--remove', action='store', dest='entry_num',type=checker,
	help='delete entry nr. xx from the json file')

parser.add_argument('jsonfile', type=pathlib.Path, 
		help='a json file with a git repos list to check')

args = parser.parse_args()

fName=str(args.jsonfile)
verbose=args.verbose
checkonly=args.check_only
listurls=args.list_urls
addentry=args.add_git_url
delentry=args.entry_num

# formatted datetime string
def orario ():
	return datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")

def show_error(errore):
	print (colors.fg.red + colors.bold + '❯❯ Error: ' + fName.upper() + errore + colors.reset + ' Please check filename or path and try again!')
	print (colors.reset)
	sys.exit()

# function to append to JSON entry (--add url argument)
def show_list():
	with open(fName,'r', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		lista = json.load(filename)
		# append new dict element
		for indice, x in enumerate(lista):
			print ('➜ ' + '{:>3}'.format(str(indice + 1)) + ' - ' + lista[indice]['Repo_Url'])
		filename.close()

# function to append to JSON entry (--add url argument)
def append_json(entry):
	with open(fName,'r+', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		lista = json.load(filename)
		# append new dict element
		lista.append(entry)
		# Sets file's current position at offset.
		filename.seek(0)
		# write changes
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
			filename.close()
		print('❯❯ ' + colors.fg.green + addentry + colors.reset +' added to ' + colors.fg.purple + fName)

def remove_json(num):
	with open(fName,'r+', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		lista = json.load(filename)
		# remove element
		try:
			lista.pop(num - 1)
		except (IndexError):
			print('>> Check entry value : range must be 1 to ' + str(len(lista)))
			sys.exit()
		# write changes
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
			filename.close()
		print('❯❯ Entry nr.' + colors.fg.green + str(num) + colors.reset +' removed from to ' + colors.fg.purple + fName)

def check_repos():
	# open the file in read mode
	with open(fName, 'r', encoding='utf-8') as filename:
			try:
				lista =json.load(filename) # populate dict 'lista'
			except json.decoder.JSONDecodeError:
				show_error(' malformed!')

	# create a backup of original file unless --check-only is passed
	if not checkonly:
		tempTuple = os.path.splitext(fName)
		bName = tempTuple[0] + '.bak'
		shutil.copyfile(fName, bName)

	# init some variables
	changed = 0
	not_changed = 0
	start_time = datetime.datetime.now()

	# print some initial statistics
	print (colors.bold + '❯❯ ' + str(len(lista)) + ' remote git repos found in the file: ' + colors.fg.purple + fName)
	print (colors.reset + '❯❯ current check time: ' + colors.fg.purple + orario())
	print (colors.reset)
	print (colors.reset + '❯❯ checking for any change since last time:')
	print (colors.reset)
	# check latest commit for each repo using git ls-remote command
	for indice, x in enumerate(lista):
		repo_url = (lista[indice]['Repo_Url'])
		last_check = (lista[indice]['Last_Check'])
		current_commit = (lista[indice]['Current_Commit'])
		print(colors.reset + '➜ ' + str(indice + 1).zfill(2) + ' - ' + repo_url + ' [ ] ', end='\r') # \r  next print overwrite this output
		# get latest comming with : git ls-remote url
		process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
		stdout, stderr = process.communicate()
		last_commit = re.split(r'\t+', stdout.decode('ascii'))[0]
		
		if current_commit != last_commit:
			changed += 1
			lista[indice]['Current_Commit'] = last_commit # update commit
			print(colors.reset + '➜ ' + colors.fg.lightred + str(indice + 1).zfill(2) + ' - ' + repo_url + ' [✘] ')
		else:
			not_changed += 1
			print(colors.reset + '➜ ' + colors.fg.lightgreen + str(indice + 1).zfill(2) + ' - ' + repo_url + ' [✔] ')
		
		# show commits info if --verbose is passed
		if verbose:
			print(colors.reset + '  ➜ last check on: ' + colors.bold + last_check)
			print(colors.reset + '  ➜ stored commit: ' + colors.bold + current_commit)
			print(colors.reset + '  ➜ latest commit: ' + colors.bold + last_commit)

		# update last_check value with current date/time
		lista[indice]['Last_Check'] = orario()
		#end loop trought dict dataset
	# close the file after all operations
	filename.close()
	# print some final statistics
	
	delta_time=datetime.datetime.now() - start_time
	print (colors.reset)
	print (colors.reset + f'❯❯ check completed in {delta_time.total_seconds()} sec. ' + colors.fg.red + str(changed) + colors.reset + ' repos changed. ' + colors.fg.green + str(not_changed) + colors.reset + ' repos not changed.')

	# dump updated dict 'lista' into the json file unless --check-only is passed
	if not checkonly :
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
			filename.close()

# main program
if __name__ == '__main__':

	# check if json file exist
	if not os.path.exists(fName):
		show_error(' not found!')
  
    # if --add is passed...
	if addentry:
		entry = {"Repo_Url":addentry,	"Last_Check": orario(),	"Current_Commit": secrets.token_hex(20) }
		append_json(entry)
	# if --list is passed
	elif listurls:
		show_list()
	# if --remove is passed
	elif delentry:
		remove_json(delentry)
	else:
		check_repos()

print (colors.reset)
sys.exit()
