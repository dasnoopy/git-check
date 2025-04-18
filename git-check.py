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
		white = '\033[37m'
		
		darkgrey = '\033[90m'
		lightred = '\033[91m'
		lightgreen = '\033[92m'
		yellow = '\033[93m'
		lightblue = '\033[94m'
		pink = '\033[95m'
		lightcyan = '\033[96m'

		bold_red  ='\033[1;31m'
		bold_green='\033[1;32m'
		bold_yellow='\033[1;33m'
		bold_blue='\033[1;34m'
		bold_purple='\033[1;35m'
		bold_cyan='\033[1;36m'
		bold_white='\033[1;37m'

		italic_bold_red='\033[1;3;31m'
		italic_bold_green='\033[1;3;32m'
		italic_bold_yellow='\033[1;3;33m'
		italic_bold_blue='\033[1;3;34m'
		italic_bold_purple='\033[1;3;35m'
		italic_bold_cyan='\033[1;3;36m'
		italic_bold_white='\033[1;3;37m'

	class bg:
		black = '\033[40m'
		red = '\033[41m'
		green = '\033[42m'
		orange = '\033[43m'
		blue = '\033[44m'
		purple = '\033[45m'
		cyan = '\033[46m'
		lightgrey = '\033[47m'

from functools import lru_cache
@lru_cache(maxsize=32)

def cursor(visible):
	if visible:
		# show terminal cursor
		print('\033[?25h', end="")
		print (colors.reset,end='\r')
	else:
		#hide terminal cursor
		print('\033[?25h', end="")
		print (colors.reset,end='\r')


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
		help='show more commit info while checking git repos')

parser.add_argument('-c','--check-only', action='store_true', dest='check_only', default=False,
		help='do not update commit info in the json file and do not create the backup file')

parser.add_argument('-l','--list', action='store_true', dest='list_repos', default=False,
		help='show list of git repos defined in the json file and days since latest commit')

parser.add_argument('-s','--sort', action='store_true', dest='sort_git', default=False,
			help='sort json objects by last change date key (ascending order) and update the json file')

parser.add_argument('-a','--add', action='store', dest='add_git',
			help='append a new git url entry in the json file')

parser.add_argument('-f','--find', action='store', dest='find_text',
			help=' find text in url entry')

parser.add_argument('-r','--remove', action='store', dest='entry_pos',type=checker,
	help='delete specific numbered entry from the json file')

parser.add_argument('jsonfile', type=pathlib.Path, 
		help='a json file with a git repos list to check')

parser.add_argument('-n','--new', action='store_true', dest='new_commit', default=False,
			help='report only repos with new commits')

args = parser.parse_args()

fName=str(args.jsonfile)
verbose=args.verbose
checkonly=args.check_only
listurls=args.list_repos
addentry=args.add_git
findTxt=args.find_text
delentry=args.entry_pos
sortObj=args.sort_git
newCommit=args.new_commit

# formatted datetime string
def orario ():
	return datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")

def get_last_commit(url):
# get latest comming with : git ls-remote url
	try:
		process = subprocess.Popen(["git", "ls-remote", url], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
		stdout, stderr = process.communicate()
		return re.split(r'\t+', stdout.decode('ascii'))[0]
	except subprocess.CalledProcessError as  exc:
		raise OSError(exc.stderr)

def check_for_links(text: str) -> list:
    # Checks if a given text contains HTTP links.
    # param text: Any provided text.
    # type text: str
    # returns: Search results.
    return re.findall(r"(?P<url>https?://[^\s]+)", text, re.IGNORECASE)

def print_error(err: str):
	print (f"{colors.reset}:: {colors.bold}{colors.fg.italic_bold_yellow}{fName}{err}{colors.reset} Please verify and try again...")
	# show again cursor if it is hide...
	cursor(True)
	sys.exit(1)

# function to sort jsno wntries by url key (-s, --sort argument)
def sort_json():
	with open(fName,'r', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		try:
			lista =json.load(filename) # populate dict 'lista'
		except json.decoder.JSONDecodeError:
			print_error(' is malformed or not a json file.')

		# sort list by Repo_Url key
		#sortedLista = sorted(lista, key=lambda k: k['Repo_Url'], reverse=False)
		# sort list by Last_Change key
		sortedLista = sorted(lista, key=lambda k: datetime.datetime.strptime(k['Last_Change'], '%d-%b-%Y %H:%M:%S'), reverse=True)

		json_write = json.dumps(sortedLista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)

# function to show urls (-l, --list argument)
def show_json():
	with open(fName,'r', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		try:
			lista =json.load(filename) # populate dict 'lista'
		except json.decoder.JSONDecodeError:
			print_error(' is malformed or not a json file.')
		# search for the maximum len string value of 'Repo_Url' key
		# Using max() + len() + list comprehension
		maxlen = max(len(element) for element in (sub['Repo_Url'] for sub in lista) if element is not None)

		for indice, x in enumerate(lista):
			# convert last_change string in datetime var type
			last_change = datetime.datetime.strptime(lista[indice]['Last_Change'],'%d-%b-%Y %H:%M:%S').date()
			# calculate day diff and convert back to str
			delta_days = int(str((datetime.date.today() - last_change).days))
			# print url list and number of days since last commit
			if delta_days >= 30:
				color=colors.fg.red
			elif delta_days >= 15:
				color=colors.fg.yellow
			else:
				color=colors.fg.lightgreen
			print (f"{colors.reset}[{indice+1 :>3}] {color}{lista[indice]['Repo_Url']:<{maxlen}} {colors.bold}[{delta_days:>3}d]")

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
			cursor(True)
			print (f"{colors.reset}:: {entry['Repo_Url']}{colors.bold} already exists in {colors.reset}{fName}...")
			sys.exit(1)
		else:
			lista.append(entry)
		# Sets file's current position at offset.
		filename.seek(0)
		# write changes
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
		print (f":: {colors.bold}{addentry}{colors.reset} added to {fName}...")

# function to find a text into url(--find 'text')
def find_entry(text):
	with open(fName,'r+', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		try:
			lista =json.load(filename) # populate dict 'lista'
		except json.decoder.JSONDecodeError:
			print_error(' is malformed or not a json file.')
		for indice, x in enumerate(lista):
			# print url list 
			if text in lista[indice]['Repo_Url']:
				print (f"{colors.bold}[{indice+1 :>3}] {colors.reset}{colors.fg.lightgreen}{lista[indice]['Repo_Url']}{colors.reset}")

def remove_json(indice):
	with open(fName,'r+', encoding='utf-8') as filename:
		# First we load existing data into a dict.
		lista = json.load(filename)
		# remove element
		try:
			lista.pop(indice - 1)
		except (IndexError):
			print (f"{colors.reset}:: Please check passed entry value: {colors.bold}range must be from 1 to {str(len(lista))}...{colors.reset}")
			sys.exit()
		# write changes
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)
		print (f"{colors.reset}:: Entry [{str(indice)}{colors.reset}] removed from to {fName}...")
		print (f"{colors.fg.white}:: Please use -l or --list option to view updated repo list before remove any other entry.{colors.reset}")

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
	# initialize some variables
	changed = 0
	not_changed = 0
	unavail = 0
	start_time = datetime.datetime.now()

	# print some initial statistics
	print (f"{colors.reset}:: Check {str(len(lista))} remote git repos from file: {colors.bold}{fName}")
	print (f"{colors.reset}:: Last check: {colors.reset}{colors.bold}{lista[0]['Last_Check']}")

	# search for the maximum len string value of 'Repo_Url' key
	# Using max() + len() + list comprehension
	maxlen = max(len(element) for element in (sub['Repo_Url'] for sub in lista) if element is not None)

	#finally check commit changes
	for indice, x in enumerate(lista):
		repo_url = lista[indice]['Repo_Url']
		last_check = lista[indice]['Last_Check']
		last_change = lista[indice]['Last_Change']
		current_commit = lista[indice]['Current_Commit']

		progress = round(100 * (indice + 1) / len(lista))
		if not newCommit: print (f"{colors.reset}[{progress:>3}%] {repo_url:<{maxlen}} [ ]", end='\r') # \r  next print overwrite this output

		# get latest comming with : git ls-remote url
		last_commit = get_last_commit(repo_url)

		if last_commit: # if latest commit is not empty, git repo should be available, then...
			if current_commit != last_commit:
				# change occurred...
				changed += 1
				lista[indice]['Current_Commit'] = last_commit # update current commit with latest commint
				lista[indice]['Last_Change'] = orario() # update time when occured last change commit
				print (f"{colors.reset}[{progress:>3}%] {colors.fg.yellow}{repo_url:<{maxlen}}{colors.bold} [✘]")
			else:
				# nothing changed ..
				if not newCommit: print (f"{colors.reset}[{progress:>3}%] {colors.fg.lightgreen}{repo_url:<{maxlen}}{colors.bold} [✔]")

			# show commits info if --verbose is passed
			if verbose:
				print (f"{colors.reset}- remote repo commit: {colors.fg.lightcyan}{current_commit}")
				# print (f"{colors.reset}- repo last commit date: {colors.fg.white}{last_check}")
				print (f"{colors.reset}- local repo commit : {colors.fg.lightcyan}{last_commit}")
				print (f"{colors.reset}- local commit date : {colors.fg.white}{last_change}")

			# always update last_check value with current date/time
			lista[indice]['Last_Check'] = orario()
		else: # if last_commit is empty, probably, there is an issue accessing the git repo
			last_commit = current_commit
			unavail += 1
			print ()
			print (f"{colors.reset}{colors.fg.red}:: Error: {repo_url} not available! {colors.reset}")
		#end loop trought dict dataset

	# print some final statistics
	not_changed = len(lista) - changed - unavail
	delta_time=datetime.datetime.now() - start_time
	print (f"{colors.reset}:: Check remote git repos completed in {colors.bold}{delta_time.total_seconds():.2f}s: {colors.reset}{colors.fg.lightcyan}{str(not_changed)}{colors.reset} not changed. {colors.fg.lightblue}{str(changed)}{colors.reset} updated. {colors.fg.blue}{str(unavail)}{colors.reset} not available.")
	
	# dump updated dict 'lista' into the json file unless --check-only is passed
	if not checkonly :
		json_write = json.dumps(lista, indent=4, sort_keys=False)
		with open(fName, 'w', encoding='utf-8') as filename:
			filename.write(json_write)
			filename.write("\n")  # Add newline (Python JSON does not)

# main program
def main():
	# hide cursor while show output messages
	cursor(False)

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
					"Last_Change": orario(),	
					"Current_Commit": get_last_commit(addentry)
					}
			append_json(entry)
		else:
			print (f"{colors.reset}:: {colors.bold}{colors.fg.italic_bold_yellow}Wrong url format!{colors.reset} Please verify and try again.")
			sys.exit()
	elif delentry:
		remove_json(delentry)
	elif sortObj:
		sort_json()
	elif findTxt:
		find_entry(findTxt)
	else:
		check_repos()
	
	# enable cursor again and restore normal output. Then exit	
	cursor(True)
	sys.exit(0)

if __name__ == '__main__':
	main()
