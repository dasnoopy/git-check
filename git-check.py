#!/usr/bin/python3
#
# @author: Andrea Antolini (https://github.com/Dasnoopy)
# @license: GNU General Public License v3.0
# @link: https://github.com/dasnoopy/git-check

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

# function to convert the input and 
# check a value or value range
def checker(a):
	num = int(a)
	if num == 0 :
		raise argparse.ArgumentTypeError('Invalid value!')
	return num

# passing arguments and/or define some variabiles
# Create the parser
parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', dest='verbose', default=False,
		help='show more info while checking git repos')

parser.add_argument('-c','--check-only', action='store_true', dest='check_only', default=False,
		help='do not update commit info in the json file and do not create the backup file')

parser.add_argument('-l','--list', action='store_true', dest='list_repos',default=False,
		help='numbered list of git repos defined in the json file')

parser.add_argument('-a','--add', action='store', dest='add_git',
			help='append a new git url entry in the json file')

parser.add_argument('-r','--remove', action='store', dest='entry_pos',type=checker,
	help='delete specific numbered entry from the json file')

parser.add_argument('jsonfile', type=pathlib.Path, 
		help='a json file with a git repos list to check')

args = parser.parse_args()

fName=str(args.jsonfile)
verbose=args.verbose
checkonly=args.check_only
listurls=args.list_repos
addentry=args.add_git
delentry=args.entry_pos

# formatted datetime string
def orario ():
	return datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")

def check_for_links(text: str) -> list:
    """Checks if a given text contains HTTP links.
    :param text: Any provided text.
    :type text: str
    :returns: Search results.
    """
    return re.findall(r"(?P<url>https?://[^\s]+)", text, re.IGNORECASE)

def print_error(err: str):
	print (colors.reset + '[e] ' + colors.fg.red + fName + err + colors.reset + ' Please verify and try again...')
	sys.exit(1)

# function to append to JSON entry (--list argument)
def show_json():
	with open(fName,'r', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		try:
			lista =json.load(filename) # populate dict 'lista'
		except json.decoder.JSONDecodeError:
			print_error(' is malformed or not a json file.')
		# append new dict element
		for indice, x in enumerate(lista):
			print (colors.reset + '[' + '{:>3}'.format(str(indice + 1)) + '] ' + colors.fg.lightgreen + lista[indice]['Repo_Url'])

# function to append to JSON entry (--add url argument)
def append_json(entry):
	with open(fName,'r+', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		try:
			lista =json.load(filename) # populate dict 'lista'
		except json.decoder.JSONDecodeError:
			print_error(' is malformed or not a json file.')
		# append new dict element if not already exist
		# create a temp list of all git urls
		urllist=[]
		for indice, x in enumerate(lista):
			urllist.append(lista[indice]['Repo_Url'])
		#check if passed url already exist
		if entry['Repo_Url'] in urllist:
			print(colors.reset + '[i] ' + entry['Repo_Url']  + colors.fg.red + ' already exist in ' + colors.reset + fName + '...')
			sys.exit()
		else:
			lista.append(entry)
		# Sets file's current position at offset.
		filename.seek(0)
		# write changes
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
		print('[i] ' + colors.bold + addentry + colors.reset + ' added to ' + fName + '...')

def remove_json(indice):
	with open(fName,'r+', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		lista = json.load(filename)
		# remove element
		try:
			lista.pop(indice - 1)
		except (IndexError):
			print('[e] Please check passed entry value: '+ colors.reset + colors.fg.red + 'range must be from 1 to ' + str(len(lista)) + '...' + colors.reset)
			sys.exit()
		# write changes
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
		print(colors.reset + '[i] Entry [' + str(indice) + colors.reset +'] removed from to ' + fName)

def check_repos():
	# open the file in read mode
	with open(fName, 'r', encoding='utf-8') as filename:
			try:
				# create a backup of original file unless --check-only is passed
				if not checkonly:
					tempTuple = os.path.splitext(fName)
					bName = tempTuple[0] + '.bak'
					shutil.copyfile(fName, bName)
				# populate list
				lista =json.load(filename) # populate dict 'lista'
			except json.decoder.JSONDecodeError:
				print_error(' is malformed or not a json file.')
	# init some variables
	changed = 0
	not_changed = 0
	unavail = 0
	start_time = datetime.datetime.now()

	# print some initial statistics
	print (colors.reset + '[i] ' + str(len(lista)) + ' remote git repos found in: ' + colors.bold + colors.fg.purple + fName)
	print (colors.reset + '[i] Last time check   : ' + colors.bold + colors.fg.purple + lista[0]['Last_Check'])
	print (colors.reset + '[i] Current time check: ' + colors.bold + colors.fg.purple + orario())

	for indice, x in enumerate(lista):
		repo_url = lista[indice]['Repo_Url']
		last_check = lista[indice]['Last_Check']
		current_commit = lista[indice]['Current_Commit']

		progress = str(int(100 * (indice + 1) / (len(lista)))) + '%'
		print(colors.reset + '[' + f"{progress:>4}" + '] ' + repo_url + ' [ ] ', end='\r') # \r  next print overwrite this output

		# get latest comming with : git ls-remote url
		process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
		stdout, stderr = process.communicate()
		last_commit = re.split(r'\t+', stdout.decode('ascii'))[0]
		if last_commit: # if latest commit is not empty git repo should be available then...
			if current_commit != last_commit:
				changed += 1
				lista[indice]['Current_Commit'] = last_commit # update commit
				print(colors.reset + '[' + f"{progress:>4}" + '] ' + colors.fg.lightred + repo_url + ' [✘] ')
			else:
				not_changed += 1
				print(colors.reset + '[' + f"{progress:>4}" + '] ' + colors.fg.lightgreen + repo_url + ' [✔] ')

			# show commits info if --verbose is passed
			if verbose:
				print(colors.reset + '  ➜ last check on: ' + colors.bold + last_check)
				print(colors.reset + '  ➜ stored commit: ' + colors.bold + current_commit)
				print(colors.reset + '  ➜ latest commit: ' + colors.bold + last_commit)

			# update last_check value with current date/time
			lista[indice]['Last_Check'] = orario()
		else: #if last_commit is empty probably thereis an issue accesing the git repo
			last_commit = current_commit
			unavail += 1
		#end loop trought dict dataset

	# print some final statistics
	delta_time=datetime.datetime.now() - start_time
	print (colors.reset + f'[i] check completed in {delta_time.total_seconds()} sec. ' + colors.fg.yellow + str(unavail) + colors.reset + ' errors. ' + colors.fg.red + str(changed) + colors.reset + ' repos changed. ' + colors.fg.lightgreen + str(not_changed) + colors.reset + ' repos not changed.')

	# dump updated dict 'lista' into the json file unless --check-only is passed
	if not checkonly :
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)

# main program
if __name__ == '__main__':

	# clean screen 
	## os.system('clear')
	print(colors.reset,end='\r')

	# check if json file exist
	if not os.path.exists(fName):
		print_error(' not found!')

	# parse arguments
	if listurls:
		show_json()
	elif addentry:
		if check_for_links(addentry):
			entry = {
					"Repo_Url":addentry,	
					"Last_Check": orario(),	
					"Current_Commit": secrets.token_hex(20)
					}
			append_json(entry)
		else:
			print (colors.reset + colors.bold + '[e] Wrong url format!' + colors.reset + ' Please verify and try again.')
			sys.exit()
	elif delentry:
		remove_json(delentry)
	else:
		check_repos()

print(colors.reset,end='\r')
sys.exit(0)
