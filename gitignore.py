import sys, os, urllib.request, re
from enum import Enum

name_gitignore = '.gitignore'
ext_gitignore = name_gitignore
file_gitignore = None

junk_lines = []
gitignores = dict()

class Option(Enum):
    NONE = 0
    UNKNOWN = 1
    ADD = 2
    CREATE = 3
    REMOVE = 4
    UPDATE = 5
    CLEAR = 6

def main(argc, argv):
    option = get_option(argc, argv)
    if option == Option.NONE:
        sys.exit('Error: no argument provided')
    elif option == Option.UNKNOWN:
        sys.exit('Error: unknown option "%s"' % argv[1])
    elif not valid_argc(argc, option):
        sys.exit('Error: invalid number of arguments for "%s"' % argv[1])
    elif not check_file_gitignore(option):
        sys.exit('Error: no %s file found' % name_gitignore)
        
    if option == Option.ADD:
        [add(name) for name in argv[2:]]
    elif option == Option.CREATE:
        if argc == 2:
            create_file()
            sys.exit(0)
        [add(name) for name in argv[2:]]
    elif option == Option.REMOVE:
        [remove(name) for name in argv[2:]]
    elif option == Option.UPDATE:
        update()
    elif option == Option.CLEAR:
        clear()
    write_file(name_gitignore)

def get_option(argc, argv):
    if argc <= 1:
        return Option.NONE
    return {
        'add': Option.ADD,
        'create': Option.CREATE,
        'remove': Option.REMOVE,
        'update': Option.UPDATE,
        'clear': Option.CLEAR
    }.get(argv[1].lower(), Option.UNKNOWN)

def valid_argc(argc, option):
    if option == Option.ADD:
        return argc > 2
    elif option == Option.CREATE:
        return argc >= 2
    elif option == Option.REMOVE:
        return argc > 2
    elif option == Option.UPDATE:
        return argc == 2
    else:
        return argc == 2

def check_file_gitignore(option):
    if option == Option.CREATE:
        return True
    if os.path.isfile(name_gitignore):
        parse_file(name_gitignore)
        return True
    if option == Option.ADD:
        create_file()
        return True
    return False

def create_file():
    open(name_gitignore, 'w')
    print("%s created" % name_gitignore)

re_start = re.compile('^\\s*#\\s*gitignore-%s:([!-.0-~]+/)*([!-.0-~]+)$' % 'start')
def parse_file(filename):
    f = open(filename, 'r')
    it = iter(f.readlines())
    f.close()
    while True:
        try:
            line = next(it)
            if line == '\n':
                continue;
            m = re_start.match(line)
            if m is None:
                junk_lines.append(line)
            else:
                parse_gitignore(it, m.group(2));
        except StopIteration:
            break

re_end = re.compile('^\\s*#\\s*gitignore-%s:([!-.0-~]+/)*([!-.0-~]+)$' % 'end')
def parse_gitignore(it, name):
    gitignore_lines = []
    while True:
        try:
            line = next(it)
            m = re_end.match(line)
            if m is None or m.group(2) != name:
                gitignore_lines.append(line)
            else:
                gitignores.update({name.lower(): gitignore_lines})
                return
        except StopIteration:
            sys.exit('Error: the start tag for "%s" is not matched by a corresponding end tag' % name)

def write_file(filename):
    f = open(filename, 'w')
    for line in junk_lines:
        f.write(line)
    for name, lines in gitignores.items():
        f.write('\n#gitignore-%s:%s\n' % ('start', names[name]))
        for line in lines:
            f.write(line)
        f.write('\n#gitignore-%s:%s\n' % ('end', names[name]))
    f.close()

def add(name):
    lower = name.lower()
    if lower not in names:
        print('Error: unknown gitignore ' + name)
        return
    update = lower in gitignores
    gitignores.update({lower: get_item_lines(lower)})
    if update:
        print('%s updated' % name)
    else:
        print('%s added' % name)

def get_item_lines(name):
    item = names[name] + ext_gitignore
    url = link + item
    data = urllib.request.urlopen(url).readlines()
    lines = []
    for line in data:
        lines.append(line.decode('utf-8'))
    if len(lines) == 1:
        return check_one_liner(lines[0], name)
    return lines;

re_one_liner = re.compile('^([!-.0-~]+)\.gitignore$')
def check_one_liner(line, name):
    m = re_one_liner.match(line)
    lower = m.group(1).lower()
    if m is None or lower == name:
        return [line]
    return get_item_lines(lower)

def remove(name):
    lower = name.lower()
    if lower not in names:
        print('Error: unknown gitignore ' + name)
        return
    try:
        gitignores.pop(lower)
        print('%s removed' % name)
    except KeyError:
        print('%s not in file' % name)

def update():
    for name in gitignores.keys():
        gitignores.update({name: get_item_lines(name)})
    print('file updated')

def clear():
    gitignores.clear()
    print('file cleared')

link = 'https://raw.githubusercontent.com/github/gitignore/master/'

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