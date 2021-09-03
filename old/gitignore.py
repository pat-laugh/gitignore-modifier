#!/usr/bin/env python
# Copyright 2017 Patrick Laughrea
# Licensed under the Apache License, Version 2.0

local_path = None
local_path_line = 4 # for local set and reset, 0-based index
online_path = 'https://raw.githubusercontent.com/github/gitignore/master/'
self_path = 'https://raw.githubusercontent.com/pat-laugh/gitignore-modifier/master/gitignore.py'
version = [1, 6, 0, 'prod']
version_line = 8

import sys, os, re, ast
from subprocess import call
py_v3 = sys.version_info[0] == 3
if py_v3:
	import urllib.request
else:
	import urllib2

def printerr(s):
	sys.stderr.write(s + os.linesep)

name_gitignore = '.gitignore'
junk_lines = []
gitignores = {}
used_gitignores = []

class Option:
	NONE = 0
	UNKNOWN = 1
	ADD = 2
	CREATE = 3
	REMOVE = 4
	UPDATE = 5
	CLEAR = 6
	LOCAL = 7
	LIST = 8
	SELF_UPDATE = 9
	DICT = 10
	HELP = 11
	VERSION = 12

options = {
	'add': Option.ADD,
	'create': Option.CREATE,
	'remove': Option.REMOVE,
	'update': Option.UPDATE,
	'clear': Option.CLEAR,
	'local': Option.LOCAL,
	'list': Option.LIST,
	'self-update': Option.SELF_UPDATE,
	'dict': Option.DICT,
	'help': Option.HELP,
	'--help': Option.HELP,
	'version': Option.VERSION,
	'--version': Option.VERSION,
}

def print_options():
	print('    add         Adds templates to the .gitignore file')
	print('    create      Creates a new .gitignore file')
	print('    remove      Removes templates from the .gitignore file')
	print('    update      Updates each template in the .gitignore file')
	print('    clear       Removes all templates from the .gitignore file')
	print('    local       --> Type "local help" for suboptions')
	print('    list        Prints a sorted list of all templates in the .gitignore file')
	print('    self-update Updates this program')
	print('    dict        Prints a dictionary of template names and paths')
	print('    help        Prints this information')
	print('    version     Prints the current version')

def main(argc, argv):
	check_expand_list(argv)
	check_modifiers(argv)
	option = get_option(argv)
	if option == Option.NONE:
		printerr('Error: no argument provided.')
		print('Options are:')
		print_options()
		sys.exit(1)
	elif option == Option.UNKNOWN:
		printerr('Error: unknown option "%s".' % argv[1])
		print_similar_names(argv[1].lower(), options.keys())
		sys.exit(1)
	elif option == Option.LOCAL:
		option_local(argc, argv)
		sys.exit(0)
	elif option == Option.SELF_UPDATE:
		option_self_update(argc, argv)
		sys.exit(0)
	elif option == Option.HELP:
		print('Options are:')
		print_options()
		sys.exit(0)
	elif option == Option.VERSION:
		if len(version) <= 3 or version[3] == 'prod':
			print('%d.%d.%d' % (version[0], version[1], version[2]))
		else:
			print('%d.%d.%d-%s-%d' % (version[0], version[1], version[2], version[3], version[4] if len(version) >= 5 else 0))
		sys.exit(0)
	elif option == Option.DICT:
		if local_path is not None:
			set_names_local(local_path)
		print(names)
		sys.exit(0)
	
	if local_path is not None:
		set_names_local(local_path)
	
	if not check_file_gitignore(option):
		sys.exit('Error: no %s file found.' % name_gitignore)
	
	if option == Option.ADD:
		option_add(argv)
	elif option == Option.CREATE:
		if len(argv) == 2:
			sys.exit(0)
		option_add(argv)
	elif option == Option.REMOVE:
		option_remove(argv)
	elif option == Option.UPDATE:
		option_update(argv)
	elif option == Option.CLEAR:
		option_clear(argv)
	elif option == Option.LIST:
		option_list(argv)
		sys.exit(0)
	write_file(name_gitignore)

def check_expand_list(argv):
	for param in argv:
		if (param[0] == '[' and param[-1] == ']'):
			index = argv.index(param)
			try:
				l = ast.literal_eval(param)
			except ValueError:
				sys.exit('Error: could not evaluate "%s"' % param)
			argv.pop(index)
			for item in l:
				argv.insert(index, item)
				index += 1

def check_modifiers(argv):
	if ('-f' in argv):
		modifier_file(argv, argv.index('-f'))
	elif ('--file' in argv):
		modifier_file(argv, argv.index('--file'))

def modifier_file(argv, index):
	global name_gitignore
	index_filename = index + 1;
	if (index_filename >= len(argv)):
		sys.exit('Error: a filename must be provided for modifier -f or --file.')
	if (len(argv) <= 3):
		sys.exit('Error: modifier %s must be used with an option' % argv[index])
	name_gitignore = argv[index_filename]
	argv.pop(index_filename)
	argv.pop(index)

def get_option(argv):
	if len(argv) <= 1:
		return Option.NONE
	return options.get(argv[1].lower(), Option.UNKNOWN)

def check_file_gitignore(option):
	if option == Option.CREATE:
		create_file()
	elif os.path.isfile(name_gitignore):
		parse_file(name_gitignore)
	elif option == Option.ADD:
		create_file()
	else:
		return False
	return True

def create_file():
	open(name_gitignore, 'w')
	print('%s created' % name_gitignore)

def exit_invalid_arguments(option_name):
	sys.exit('Error: invalid arguments for "%s".' % option_name)

def option_add(argv):
	if len(argv) < 3:
		exit_invalid_arguments(argv[1])
	for name in argv[2:]:
		add(name)

def option_remove(argv):
	if len(argv) < 3:
		exit_invalid_arguments(argv[1])
	for name in argv[2:]:
		remove(name)

def get_re_gitignore(tag):
	return re.compile(r'^\s*#+\s*gitignore-%s:([!-.0-~]+(/|\\))*([!-.0-~]+)\s*$' % tag)

re_start = get_re_gitignore('start')
def parse_file(filename):
	errors = []
	with open(filename, 'r') as f:
		for line in f:
			m = re_start.match(line)
			if m is None:
				junk_lines.append(line)
			else:
				name = m.group(3)
				parse_gitignore(f, name)
				if name.lower() not in names:
					errors.append(name)
	if len(errors) > 0:
		if len(errors) == 1:
			printerr('There was an error while parsing the %s file.' % name_gitignore)
			error_unknown_gitignore(errors[0])
		else:
			printerr('There were multiple errors while parsing the %s file.' % name_gitignore)
			for n in errors:
				error_unknown_gitignore(n)
		sys.exit(1)
	if len(junk_lines) > 0:
		last_line = junk_lines[-1]
		if last_line[-1] != '\n':
			junk_lines[-1] = last_line + os.linesep

re_end = get_re_gitignore('end')
def parse_gitignore(f, name):
	gitignore_lines = []
	for line in f:
		m = re_end.match(line)
		if m is None or m.group(3) != name:
			gitignore_lines.append(line)
		else:
			gitignores.update({name.lower(): gitignore_lines})
			return
	printerr('There was an error while parsing the %s file.' % name_gitignore)
	sys.exit('Error: the start tag for "%s" is not matched by a corresponding end tag.' % name)

def get_gitignore_tag(tag, name):
	return '##gitignore-%s:%s\n' % (tag, name)

def write_file(filename):
	f = open(filename, 'w')
	f.writelines(junk_lines)
	for name, lines in gitignores.items():
		f.write(get_gitignore_tag('start', name))
		f.writelines(lines)
		f.write(get_gitignore_tag('end', name))
	f.close()

def close_similarity(s1, s2):
	if abs(len(s1) - len(s2)) > 2:
		return False
	set1, set2 = set(s1), set(s2)
	len_set1, len_set2 = len(set1), len(set2)
	if abs(len_set1 - len_set2) > 2:
		return False
	common_letters = set1.intersection(set2)
	len_cl = len(common_letters)
	return len_set1 - len_cl < 2 and len_set2 - len_cl < 2

def get_similar_names(name, list_names):
	return [n for n in list_names if close_similarity(name, n)]

def print_similar_names(name, list_names):
	similar_names = get_similar_names(name, list_names)
	if len(similar_names) > 1:
		printerr('Did you mean one of these?')
		for n in similar_names:
			printerr('\t' + n)
	elif len(similar_names) == 1:
		printerr('Did you mean this?')
		printerr('\t' + similar_names[0])

def error_unknown_gitignore(name):
	printerr('Error: unknown gitignore "%s"' % name)
	print_similar_names(name, names.keys())

def add(name):
	lower = name.lower()
	if lower in names:
		update_gitignores(lower)
	else:
		error_unknown_gitignore(name)

def update_gitignores(name):
	if name in used_gitignores:
		return
	used_gitignores.append(name)
	updated = name in gitignores.keys()
	gitignores.update({name: get_item_lines(name)})
	print('%s %s' % (name, 'updated' if updated else 'added'))

def get_item_lines(name):
	if local_path is not None:
		url = local_path + names[name] + '.gitignore'
		with open(url, 'r') as f:
			lines = f.readlines()
	else:
		url = online_path + names[name] + '.gitignore'
		if py_v3:
			data = urllib.request.urlopen(url).readlines()
		else:
			data = urllib2.urlopen(url).readlines()
		lines = [line.decode('utf-8') for line in data]
	last_line = lines[-1]
	if last_line[-1] != '\n':
		lines[-1] = last_line + os.linesep
	check_gitignore_links(lines, name, update_gitignores)
	return lines

re_gitignore_link = re.compile(r'^(#|\s)*([!-.0-~]+/)*([!-.0-~]+)\.gitignore\s*$')
def check_gitignore_links(lines, linker, func):
	for line in lines:
		m = re_gitignore_link.match(line)
		if m is None:
			continue
		name = m.group(3).lower()
		if name not in used_gitignores:
			print('%s -> %s' % (linker, name))
			if name not in names:
				error_unknown_gitignore(name)
				continue
			func(name)

def remove(name):
	lower = name.lower()
	if lower in used_gitignores:
		return
	used_gitignores.append(lower)
	if lower not in names:
		error_unknown_gitignore(name)
		return
	try:
		check_gitignore_links(gitignores[lower], lower, remove)
		gitignores.pop(lower)
		print('%s removed' % name)
	except KeyError:
		printerr('Error: %s not in file.' % name)

def option_update(argv):
	if len(argv) != 2:
		exit_invalid_arguments(argv[1])
	for name in gitignores.keys():
		update_gitignores(name)

def option_clear(argv):
	if len(argv) != 2:
		exit_invalid_arguments(argv[1])
	gitignores.clear()
	print('File cleared.')

def option_list(argv):
	if len(argv) != 2:
		exit_invalid_arguments(argv[1])
	l = list(gitignores.keys())
	l.sort()
	print(l)


class OptionLocal:
	NONE = 0
	UNKNOWN = 1
	SET = 2
	RESET = 3
	SHOW = 4
	CALL = 5
	HELP = 6

options_local = {
	'set': OptionLocal.SET,
	'reset': OptionLocal.RESET,
	'show': OptionLocal.SHOW,
	'call': OptionLocal.CALL,
	'help': OptionLocal.HELP,
	'--help': OptionLocal.HELP,
}

def print_local_suboptions():
	print('      set       Sets a local directory to fetch gitignore templates from')
	print('      reset     Resets the local directory to None')
	print('      show      Shows the local path')
	print('      call      Calls a command in the local directory')
	print('      help      Prints this information')
	
def option_local(argc, argv):
	option = get_option_local(argc, argv)
	if option == OptionLocal.NONE:
		printerr('Error: no %s suboption provided.' % argv[1])
		print('Suboptions are:')
		print_local_suboptions()
		sys.exit(1)
	elif option == OptionLocal.UNKNOWN:
		printerr('Error: unknown %s suboption "%s".' % (argv[1], argv[2]))
		print_similar_names(argv[2].lower(), options_local.keys())
		sys.exit(1)
	elif option == OptionLocal.SET:
		option_local_set(argc, argv)
	elif option == OptionLocal.RESET:
		option_local_reset(argc, argv)
	elif option == OptionLocal.SHOW:
		option_local_show(argc, argv)
	elif option == OptionLocal.CALL:
		option_local_call(argc, argv)
	elif option == OptionLocal.HELP:
		print('Suboptions are:')
		print_local_suboptions()
		sys.exit(1)

def get_option_local(argc, argv):
	if argc <= 2:
		return OptionLocal.NONE
	return options_local.get(argv[2].lower(), OptionLocal.UNKNOWN)

def option_local_set(argc, argv):
	if argc != 4:
		exit_invalid_arguments('%s %s' % (argv[1], argv[2]))
	new_local_path = os.path.abspath(argv[3])
	if new_local_path[-1] != os.sep:
		new_local_path += os.sep
	set_names_local(new_local_path)
	set_local_path(new_local_path)
	print('Local path set to "%s".' % new_local_path)

def option_local_reset(argc, argv):
	if argc != 3:
		exit_invalid_arguments('%s %s' % (argv[1], argv[2]))
	set_local_path(None)
	print('Local path reset.')

def option_local_show(argc, argv):
	if argc != 3:
		exit_invalid_arguments('%s %s' % (argv[1], argv[2]))
	if local_path is None:
		print('Local path is not set.')
	else:
		print(local_path)

def option_local_call(argc, argv):
	if local_path is None:
		sys.exit('Error: local path is not set.')
	
	try:
		curr_dir = os.getcwd()
		os.chdir(local_path)
		print('Output of the call with parameters %s:\n' % argv[3:])
		print(call(argv[3:]))
		os.chdir(curr_dir)
	except (LookupError) as e:
		sys.exit('Error: %s.' % e)
	except (TypeError, IOError, OSError) as e:
		sys.exit('Error: local path or command is invalid.')

def set_local_path(path):
	with open(__file__, 'r') as f:
		lines = f.readlines()
	if path is None:
		lines[local_path_line] = 'local_path = None\n'
	else:
		lines[local_path_line] = "local_path = '%s'\n" % path.replace('\\', '\\\\')
	with open(__file__, 'w') as f:
		f.writelines(lines)

def set_names_local(path):
	try:
		curr_dir = os.getcwd()
		names.clear()
		os.chdir(path)
		add_names_local('.')
		os.chdir(curr_dir)
	except (LookupError) as e:
		sys.exit('Error: %s.' % e)
	except (TypeError, IOError, OSError) as e:
		sys.exit('Error: local path is invalid.')

re_gitignore_file = re.compile(r'([^.]+)\.gitignore')
def check_local_file(subdir, path_name):
	m = re_gitignore_file.match(path_name)
	if m is not None:
		name = m.group(1)
		lower = m.group(1).lower()
		if lower in names:
			raise LookupError('conflicting "%s" templates in local directory' % lower)
		if subdir == '.':
			names.update({lower: name})
		else: # skip the ./
			names.update({lower: subdir[2:] + os.sep + name})

def add_names_local(subdir):
	if py_v3:
		for path in os.scandir(subdir):
			path_name = path.name
			if path.is_file():
				check_local_file(subdir, path_name)
			elif path.is_dir():
				add_names_local(subdir + os.sep + path_name)
	else:
		for path_name in os.listdir(subdir):
			path = os.path.join(subdir, path_name)
			if os.path.isfile(path):
				check_local_file(subdir, path_name)
			elif os.path.isdir(path):
				add_names_local(path)

su_def_stage = 'prod'
su_def_alpha = 0
re_version = re.compile(r".*\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*'(dev|prod)'\s*(,\s*(\d+)\s*)?)?,?\s*\]")
def get_new_version(lines):
	m = re_version.match(lines[version_line])
	if m is None:
		return None
	major = int(m.group(1))
	minor = int(m.group(2))
	patch = int(m.group(3))
	stage = m.group(5) or su_def_stage
	alpha = su_def_alpha if m.group(7) is None else int(m.group(7))
	return [major, minor, patch, stage, alpha]

su_up_to_date = 'Already up to date.'
su_successful = 'Self-updated successfully.'
def option_self_update(argc, argv):
	if argc != 2:
		exit_invalid_arguments(argv[1])
	with open(__file__, 'r') as f:
		old_lines = f.readlines()
	if py_v3:
		data = urllib.request.urlopen(self_path).readlines()
	else:
		data = urllib2.urlopen(self_path).readlines()
	lines = [line.decode('utf-8') for line in data]
	new_v = get_new_version(lines)
	if new_v is None:
		write_self_update(lines, local_path)
		with open(__file__, 'r') as f:
			new_lines = f.readlines()
		if old_lines == new_lines:
			print(su_up_to_date)
		else:
			print(su_successful)
	else:
		if len(version) < 5:
			if len(version) < 4:
				version.append(su_def_stage)
			version.append(su_def_alpha)
		if version == new_v:
			print(su_up_to_date)
			sys.exit()
		if version[0] != new_v[0]:
			self_update_warning('Warning: new version is incompatible with current version.')
		if (version[3] != new_v[3] and new_v[3] != 'prod'):
			self_update_warning('Warning: new version is not a production version.')
		write_self_update(lines, local_path)
		print(su_successful)
		
def write_self_update(lines, local_path):
	with open(__file__, 'w') as f:
		f.writelines(lines)
	set_local_path(local_path)

def self_update_warning(warning):
	while True:
		sys.stdout.write(warning + ' Continue? (y/n) ')
		sys.stdout.flush()
		a = sys.stdin.readline().strip()[:1].lower()
		if (a == 'y'):
			break;
		if (a == 'n'):
			print('Self-update cancelled.')
			sys.exit()

names = {'nanoc':'Nanoc','webmethods':'Global/WebMethods','commonlisp':'CommonLisp','xcode':'Global/Xcode','sublimetext':'Global/SublimeText','bricxcc':'Global/BricxCC','lemonstand':'LemonStand','concrete5':'Concrete5','go':'Go','jdeveloper':'Global/JDeveloper','ros':'ROS','zephir':'Zephir','kate':'Global/Kate','typo3':'Typo3','anjuta':'Global/Anjuta','cakephp':'CakePHP','textpattern':'Textpattern','elm':'Elm','modelsim':'Global/ModelSim','momentics':'Global/Momentics','fortran':'Fortran','gcov':'Gcov','ada':'Ada','libreoffice':'Global/LibreOffice','erlang':'Erlang','yeoman':'Yeoman','dm':'DM','playframework':'PlayFramework','python':'Python','monodevelop':'Global/MonoDevelop','dart':'Dart','craftcms':'CraftCMS','julia':'Julia','ninja':'Global/Ninja','vim':'Global/Vim','qt':'Qt','eiffelstudio':'Global/EiffelStudio','tortoisegit':'Global/TortoiseGit','d':'D','mercurial':'Global/Mercurial','c++':'C++','gradle':'Gradle','rhodesrhomobile':'RhodesRhomobile','xilinxise':'Global/XilinxISE','sketchup':'SketchUp','chefcookbook':'ChefCookbook','kohana':'Kohana','netbeans':'Global/NetBeans','packer':'Packer','elisp':'Elisp','tex':'TeX','sdcc':'Sdcc','turbogears2':'TurboGears2','virtualenv':'Global/VirtualEnv','scons':'SCons','scala':'Scala','delphi':'Delphi','unrealengine':'UnrealEngine','redis':'Global/Redis','jboss':'Jboss','lua':'Lua','zendframework':'ZendFramework','stata':'Global/Stata','visualstudio':'VisualStudio','eagle':'Eagle','appceleratortitanium':'AppceleratorTitanium','sbt':'Global/SBT','tags':'Global/Tags','opencart':'OpenCart','processing':'Processing','maven':'Maven','redcar':'Global/Redcar','elixir':'Elixir','bazaar':'Global/Bazaar','swift':'Swift','laravel':'Laravel','c':'C','drupal':'Drupal','synopsysvcs':'Global/SynopsysVCS','extjs':'ExtJs','ocaml':'OCaml','stella':'Stella','joomla':'Joomla','appengine':'AppEngine','waf':'Waf','clojure':'Clojure','lilypond':'Lilypond','symfony':'Symfony','yii':'Yii','sugarcrm':'SugarCRM','microsoftoffice':'Global/MicrosoftOffice','fancy':'Fancy','jenv':'Global/JEnv','terraform':'Terraform','haskell':'Haskell','cloud9':'Global/Cloud9','composer':'Composer','linux':'Global/Linux','fuelphp':'FuelPHP','archlinuxpackages':'ArchLinuxPackages','plone':'Plone','phalcon':'Phalcon','cfwheels':'CFWheels','mercury':'Mercury','java':'Java','codeigniter':'CodeIgniter','symphonycms':'SymphonyCMS','gpg':'Global/GPG','episerver':'EPiServer','slickedit':'Global/SlickEdit','rails':'Rails','perl':'Perl','emacs':'Global/Emacs','archives':'Global/Archives','dreamweaver':'Global/Dreamweaver','expressionengine':'ExpressionEngine','wordpress':'WordPress','scheme':'Scheme','matlab':'Global/Matlab','coq':'Coq','kdevelop4':'Global/KDevelop4','notepadpp':'Global/NotepadPP','macos':'Global/macOS','lazarus':'Global/Lazarus','ruby':'Ruby','jetbrains':'Global/JetBrains','igorpro':'IGORPro','eclipse':'Global/Eclipse','cvs':'Global/CVS','labview':'LabVIEW','r':'R','magento':'Magento','rust':'Rust','lyx':'Global/LyX','objective-c':'Objective-C','ansible':'Global/Ansible','oracleforms':'OracleForms','visualstudiocode':'Global/VisualStudioCode','xojo':'Xojo','smalltalk':'Smalltalk','metaprogrammingsystem':'MetaProgrammingSystem','umbraco':'Umbraco','cmake':'CMake','vvvv':'VVVV','kicad':'KiCad','scrivener':'Scrivener','gwt':'GWT','vagrant':'Global/Vagrant','leiningen':'Leiningen','prestashop':'Prestashop','unity':'Unity','otto':'Global/Otto','actionscript':'Actionscript','android':'Android','lithium':'Lithium','codekit':'Global/CodeKit','qooxdoo':'Qooxdoo','cuda':'CUDA','node':'Node','nim':'Nim','finale':'Finale','gitbook':'GitBook','flexbuilder':'Global/FlexBuilder','darteditor':'Global/DartEditor','dropbox':'Global/Dropbox','idris':'Idris','calabash':'Global/Calabash','agda':'Agda','svn':'Global/SVN','autotools':'Autotools','ensime':'Global/Ensime','sass':'Sass','jekyll':'Jekyll','windows':'Global/Windows','seamgen':'SeamGen','grails':'Grails','purescript':'PureScript','espresso':'Global/Espresso','textmate':'Global/TextMate','forcedotcom':'ForceDotCom','opa':'Opa'}

msg_error = 'Error: there was an error'
msg_error_url = 'maybe there is no Internet connection'
msg_error_permission = 'make sure you can write on the executable file'
if __name__ == '__main__':
	if py_v3:
		try:
			main(len(sys.argv), sys.argv)
		except urllib.error.URLError:
			printerr('%s -- %s.' % (msg_error, msg_error_url))
		except PermissionError:
			printerr('Error: permission denied -- %s.' % msg_error_permission)
	else:
		try:
			main(len(sys.argv), sys.argv)
		except urllib2.URLError:
			printerr('%s -- %s.' % (msg_error, msg_error_url))
		except IOError:
			printerr('%s -- %s.' % (msg_error, msg_error_permission))