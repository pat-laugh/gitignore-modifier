#!/usr/bin/env python3
# Copyright 2017 Patrick Laughrea
# Licensed under the Apache License, Version 2.0

local_path = None
local_path_line = 4 # for local set and reset, 0-based index
online_path = 'https://raw.githubusercontent.com/github/gitignore/master/'

import sys, os, urllib.request, re
from enum import Enum

name_gitignore = '.gitignore'
junk_lines = []
gitignores = {}
used_gitignores = []

class Option(Enum):
    NONE = 0
    UNKNOWN = 1
    ADD = 2
    CREATE = 3
    REMOVE = 4
    UPDATE = 5
    CLEAR = 6
    LOCAL = 7

options = {
    'add': Option.ADD,
    'create': Option.CREATE,
    'remove': Option.REMOVE,
    'update': Option.UPDATE,
    'clear': Option.CLEAR,
    'local': Option.LOCAL
}

def main(argc, argv):
    option = get_option(argc, argv)
    if option == Option.NONE:
        sys.exit('Error: no argument provided')
    elif option == Option.UNKNOWN:
        print('Error: unknown option "%s"' % argv[1])
        print_similar_names(argv[1].lower(), options.keys())
        sys.exit(1)
    elif not valid_argc(argc, option):
        sys.exit('Error: invalid number of arguments for "%s"' % argv[1])
    elif option != Option.LOCAL and not check_file_gitignore(option):
        sys.exit('Error: no %s file found' % name_gitignore)
    
    if local_path is not None:
        set_names_local()
    
    if option == Option.ADD:
        [add(name) for name in argv[2:]]
    elif option == Option.CREATE:
        if argc == 2:
            sys.exit(0)
        [add(name) for name in argv[2:]]
    elif option == Option.REMOVE:
        [remove(name) for name in argv[2:]]
    elif option == Option.UPDATE:
        update()
    elif option == Option.CLEAR:
        clear()
    elif option == Option.LOCAL:
        local(argv)
        sys.exit(0)
    write_file(name_gitignore)

def get_option(argc, argv):
    if argc <= 1:
        return Option.NONE
    return options.get(argv[1].lower(), Option.UNKNOWN)

def valid_argc(argc, option):
    if option == Option.ADD:
        return argc > 2
    elif option == Option.CREATE:
        return argc >= 2
    elif option == Option.REMOVE:
        return argc > 2
    elif option == Option.UPDATE:
        return argc == 2
    elif option == Option.CLEAR:
        return argc == 2
    else: #option == Option.LOCAL:
        return argc == 3 or argc == 4

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

def get_re_gitignore(tag):
    return re.compile(r'^\s*#+\s*gitignore-%s:([!-.0-~]+/)*([!-.0-~]+)$' % tag)

re_start = get_re_gitignore('start')
def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            m = re_start.match(line)
            if m is None:
                junk_lines.append(line)
            else:
                parse_gitignore(f, m.group(2))
    if len(junk_lines) > 0:
        last_line = junk_lines[-1]
        if last_line[-1] != '\n':
            junk_lines[-1] = last_line + os.linesep

re_end = get_re_gitignore('end')
def parse_gitignore(f, name):
    gitignore_lines = []
    for line in f:
        m = re_end.match(line)
        if m is None or m.group(2) != name:
            gitignore_lines.append(line)
        else:
            gitignores.update({name.lower(): gitignore_lines})
            return
    sys.exit('Error: the start tag for "%s" is not matched by a corresponding end tag' % name)

def get_gitignore_tag(tag, name):
    return '##gitignore-%s:%s\n' % (tag, name)

def write_file(filename):
    f = open(filename, 'w')
    f.writelines(junk_lines)
    for name, lines in gitignores.items():
        f.write(get_gitignore_tag('start', names[name]))
        f.writelines(lines)
        f.write(get_gitignore_tag('end', names[name]))
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
    if len(similar_names) > 0:
        print('Did you mean one of these?')
        for n in similar_names: print('\t' + n)

def error_unknown_gitignore(name):
    print('Error: unknown gitignore "%s"' % name)
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
        data = urllib.request.urlopen(url).readlines()
        lines = [line.decode('utf-8') for line in data]
    last_line = lines[-1]
    if last_line[-1] != '\n':
        lines[-1] = last_line + os.linesep
    check_gitignore_links(lines, name)
    return lines

re_gitignore_link = re.compile(r'^(#|\s)*([!-.0-~]+/)*([!-.0-~]+)\.gitignore$')
def check_gitignore_links(lines, linker):
    for line in lines:
        m = re_gitignore_link.match(line)
        if m is None:
            continue
        name = m.group(3).lower()
        if name not in used_gitignores:
            print('%s -> %s' % (linker, name))
            update_gitignores(name)

def remove(name):
    lower = name.lower()
    if lower in used_gitignores:
        return
    used_gitignores.append(lower)
    if lower not in names:
        error_unknown_gitignore(name)
        return
    try:
        gitignores.pop(lower)
        print('%s removed' % name)
    except KeyError:
        print('Error: %s not in file' % name)

def update():
    for name in gitignores.keys():
        update_gitignores(name)

def clear():
    gitignores.clear()
    print('file cleared')

def set_local_path(path):
    with open(__file__, 'r') as f:
        lines = f.readlines()
    if path is None:
        lines[local_path_line] = 'local_path = None\n'
    else:
        lines[local_path_line] = "local_path = '%s'\n" % path
    with open(__file__, 'w') as f:
        f.writelines(lines)

def local(argv):
    global local_path
    if argv[2] == 'set':
        if len(argv) != 4:
            sys.exit('Error: local set needs a directory')
        new_local_path = argv[3]
        if new_local_path[-1] != os.sep:
            new_local_path += os.sep
        try:
            os.chdir(new_local_path)
            local_path = new_local_path
            set_names_local()
        except (LookupError) as e:
            sys.exit('Error: %s' % e)
        except (TypeError, FileNotFoundError) as e:
            sys.exit('Error: path is invalid')
        set_local_path(new_local_path)
        print('local path set to "%s"' % new_local_path)
    elif argv[2] == 'reset':
        set_local_path(None)
        print('local path reset')
    elif argv[2] == 'show':
        if local_path is None:
            print('local path is not set')
        else:
            print('local path set to "%s"' % local_path)
    else:
        sys.exit('Error: option local only accepts "set" and "reset"')


def set_names_local():
    curr_dir = os.getcwd()
    names.clear()
    os.chdir(local_path)
    add_names_local('.')
    os.chdir(curr_dir)

re_gitignore_file = re.compile(r'([^.]+)\.gitignore')
def add_names_local(subdir):
    it = os.scandir(subdir)
    while True:
        try:
            dir_entry = next(it)
            if dir_entry.is_file():
                m = re_gitignore_file.match(dir_entry.name)
                if m is not None:
                    name = m.group(1)
                    lower = m.group(1).lower()
                    if lower in names:
                        raise LookupError('more than one gitignore file called "%s"' % lower)
                    if subdir == '.':
                        names.update({lower: name})
                    else: # skip the ./
                        names.update({lower: subdir[2:] + os.sep + name})
            elif dir_entry.is_dir():
                name = subdir + os.sep + dir_entry.name
                add_names_local(name)
        except StopIteration:
            break

names = {
    'actionscript' : 'Actionscript',
    'ada' : 'Ada',
    'agda' : 'Agda',
    'android' : 'Android',
    'appengine' : 'AppEngine',
    'appceleratortitanium' : 'AppceleratorTitanium',
    'archlinuxpackages' : 'ArchLinuxPackages',
    'autotools' : 'Autotools',
    'c++' : 'C++',
    'c' : 'C',
    'cfwheels' : 'CFWheels',
    'cmake' : 'CMake',
    'cuda' : 'CUDA',
    'cakephp' : 'CakePHP',
    'chefcookbook' : 'ChefCookbook',
    'clojure' : 'Clojure',
    'codeigniter' : 'CodeIgniter',
    'commonlisp' : 'CommonLisp',
    'composer' : 'Composer',
    'concrete5' : 'Concrete5',
    'coq' : 'Coq',
    'craftcms' : 'CraftCMS',
    'd' : 'D',
    'dm' : 'DM',
    'dart' : 'Dart',
    'delphi' : 'Delphi',
    'drupal' : 'Drupal',
    'episerver' : 'EPiServer',
    'eagle' : 'Eagle',
    'elisp' : 'Elisp',
    'elixir' : 'Elixir',
    'elm' : 'Elm',
    'erlang' : 'Erlang',
    'expressionengine' : 'ExpressionEngine',
    'extjs' : 'ExtJs',
    'fancy' : 'Fancy',
    'finale' : 'Finale',
    'forcedotcom' : 'ForceDotCom',
    'fortran' : 'Fortran',
    'fuelphp' : 'FuelPHP',
    'gwt' : 'GWT',
    'gcov' : 'Gcov',
    'gitbook' : 'GitBook',
    'go' : 'Go',
    'gradle' : 'Gradle',
    'grails' : 'Grails',
    'haskell' : 'Haskell',
    'igorpro' : 'IGORPro',
    'idris' : 'Idris',
    'java' : 'Java',
    'jboss' : 'Jboss',
    'jekyll' : 'Jekyll',
    'joomla' : 'Joomla',
    'julia' : 'Julia',
    'kicad' : 'KiCad',
    'kohana' : 'Kohana',
    'labview' : 'LabVIEW',
    'laravel' : 'Laravel',
    'leiningen' : 'Leiningen',
    'lemonstand' : 'LemonStand',
    'lilypond' : 'Lilypond',
    'lithium' : 'Lithium',
    'lua' : 'Lua',
    'magento' : 'Magento',
    'maven' : 'Maven',
    'mercury' : 'Mercury',
    'metaprogrammingsystem' : 'MetaProgrammingSystem',
    'nanoc' : 'Nanoc',
    'nim' : 'Nim',
    'node' : 'Node',
    'ocaml' : 'OCaml',
    'objective-c' : 'Objective-C',
    'opa' : 'Opa',
    'opencart' : 'OpenCart',
    'oracleforms' : 'OracleForms',
    'packer' : 'Packer',
    'perl' : 'Perl',
    'phalcon' : 'Phalcon',
    'playframework' : 'PlayFramework',
    'plone' : 'Plone',
    'prestashop' : 'Prestashop',
    'processing' : 'Processing',
    'purescript' : 'PureScript',
    'python' : 'Python',
    'qooxdoo' : 'Qooxdoo',
    'qt' : 'Qt',
    'r' : 'R',
    'ros' : 'ROS',
    'rails' : 'Rails',
    'rhodesrhomobile' : 'RhodesRhomobile',
    'ruby' : 'Ruby',
    'rust' : 'Rust',
    'scons' : 'SCons',
    'sass' : 'Sass',
    'scala' : 'Scala',
    'scheme' : 'Scheme',
    'scrivener' : 'Scrivener',
    'sdcc' : 'Sdcc',
    'seamgen' : 'SeamGen',
    'sketchup' : 'SketchUp',
    'smalltalk' : 'Smalltalk',
    'stella' : 'Stella',
    'sugarcrm' : 'SugarCRM',
    'swift' : 'Swift',
    'symfony' : 'Symfony',
    'symphonycms' : 'SymphonyCMS',
    'tex' : 'TeX',
    'terraform' : 'Terraform',
    'textpattern' : 'Textpattern',
    'turbogears2' : 'TurboGears2',
    'typo3' : 'Typo3',
    'umbraco' : 'Umbraco',
    'unity' : 'Unity',
    'unrealengine' : 'UnrealEngine',
    'vvvv' : 'VVVV',
    'visualstudio' : 'VisualStudio',
    'waf' : 'Waf',
    'wordpress' : 'WordPress',
    'xojo' : 'Xojo',
    'yeoman' : 'Yeoman',
    'yii' : 'Yii',
    'zendframework' : 'ZendFramework',
    'zephir' : 'Zephir',
    
    'anjuta' : 'Global/Anjuta',
    'ansible' : 'Global/Ansible',
    'archives' : 'Global/Archives',
    'bazaar' : 'Global/Bazaar',
    'bricxcc' : 'Global/BricxCC',
    'cvs' : 'Global/CVS',
    'calabash' : 'Global/Calabash',
    'cloud9' : 'Global/Cloud9',
    'codekit' : 'Global/CodeKit',
    'darteditor' : 'Global/DartEditor',
    'dreamweaver' : 'Global/Dreamweaver',
    'dropbox' : 'Global/Dropbox',
    'eclipse' : 'Global/Eclipse',
    'eiffelstudio' : 'Global/EiffelStudio',
    'emacs' : 'Global/Emacs',
    'ensime' : 'Global/Ensime',
    'espresso' : 'Global/Espresso',
    'flexbuilder' : 'Global/FlexBuilder',
    'gpg' : 'Global/GPG',
    'jdeveloper' : 'Global/JDeveloper',
    'jetbrains' : 'Global/JetBrains',
    'kdevelop4' : 'Global/KDevelop4',
    'kate' : 'Global/Kate',
    'lazarus' : 'Global/Lazarus',
    'libreoffice' : 'Global/LibreOffice',
    'linux' : 'Global/Linux',
    'lyx' : 'Global/LyX',
    'matlab' : 'Global/Matlab',
    'mercurial' : 'Global/Mercurial',
    'microsoftoffice' : 'Global/MicrosoftOffice',
    'modelsim' : 'Global/ModelSim',
    'momentics' : 'Global/Momentics',
    'monodevelop' : 'Global/MonoDevelop',
    'netbeans' : 'Global/NetBeans',
    'ninja' : 'Global/Ninja',
    'notepadpp' : 'Global/NotepadPP',
    'otto' : 'Global/Otto',
    'redcar' : 'Global/Redcar',
    'redis' : 'Global/Redis',
    'sbt' : 'Global/SBT',
    'svn' : 'Global/SVN',
    'slickedit' : 'Global/SlickEdit',
    'stata' : 'Global/Stata',
    'sublimetext' : 'Global/SublimeText',
    'synopsysvcs' : 'Global/SynopsysVCS',
    'tags' : 'Global/Tags',
    'textmate' : 'Global/TextMate',
    'tortoisegit' : 'Global/TortoiseGit',
    'vagrant' : 'Global/Vagrant',
    'vim' : 'Global/Vim',
    'virtualenv' : 'Global/VirtualEnv',
    'visualstudiocode' : 'Global/VisualStudioCode',
    'webmethods' : 'Global/WebMethods',
    'windows' : 'Global/Windows',
    'xcode' : 'Global/Xcode',
    'xilinxise' : 'Global/XilinxISE',
    'macos' : 'Global/macOS'
}

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)