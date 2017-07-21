#!/usr/bin/env python
# Copyright 2017 Patrick Laughrea
# Licensed under the Apache License, Version 2.0
README = '''
## Purpose

This is a script to update names in the `gitignore.py` file.

## Requirements

The gitignore repository must have been cloned on the machine at `~/gitignore`.
The directory where this script is run must contain the `gitignore.py` file to
update.

## Concept

The `gitignore.py` file is read to determine where the `names` variable is
located. Its location is considered as the first occurence of an unindented
`names` variable.

`gitignore.py` is then used to call:
- `local set ~/gitignore`, to set the local path
- `local call git pull`, to update the directory's contents
- `dict`, to get all the key-values
- `local reset`, to reset the local path

The option `dict` returns the key-values of all the gitignore templates. If the
old and new values differ, then the `names` variable in the `gitignore.py` file
is set to be equal to the new value, after it's been stripped of all spaces.
'''

import sys, os, subprocess, ast

def main(argc, argv):
	dir_name = os.path.dirname(os.path.abspath(__file__))
	os.chdir(dir_name)
	filename = 'gitignore.py'
	with open(filename, 'r') as f:
		lines = f.readlines()
	path_gitignore = os.path.join(os.path.expanduser('~'), 'gitignore')
	location_names = get_location_names(lines)
	print_and_call('./%s local set %s' % (filename, path_gitignore))
	print_and_call('./%s local call git pull' % filename)
	names = ast.literal_eval(print_and_call('./%s dict' % filename))
	print_and_call('./%s local reset' % filename)
	old_names = get_old_names(lines[location_names])
	if old_names == names:
		print('Names are up to date.')
	else:
		lines[location_names] = 'names = %s\n' % str(names).replace(' ', '')
		with open(filename, 'w') as f:
			f.writelines(lines)
		print('Names updated.')
	
def get_location_names(lines):
	counter = 0
	for line in lines:
		if line[0:5] == 'names':
			break
		counter += 1
	return counter

def print_and_call(cmd):
	print(cmd)
	return subprocess.check_output(cmd.split())

def get_old_names(line):
	return ast.literal_eval(line[line.find('{'):])

if __name__ == '__main__':
	main(len(sys.argv), sys.argv)