import sys, os, urllib.request
from enum import Enum

name_gitignore = '.gitignore'
ext_gitignore = name_gitignore
file_gitignore = None

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
        sys.exit('no argument provided')
    elif option == Option.UNKNOWN:
        sys.exit('unknown option "%s"' % argv[1])
    

    
    
    global file_gitignore
        
    if argv[1] == 'add':
        check_add(argc)
        [add(name) for name in argv[2:]]
    elif argv[1] == 'create':
        check_create(argc)
        [add(name) for name in argv[2:]]
    elif argv[1] == 'remove':
        check_remove(argc)
        [remove(name) for name in argv[2:]]
    elif argv[1] == 'update':
        update()
    elif argv[1] == 'clear':
        clear()
    else:
        exit_error('unknown argument ' + argv[1])
    file_gitignore.close()

def get_option(argc, argv):
    options = {
        'add': Option.ADD,
        'create': Option.CREATE,
        'remove': Option.REMOVE,
        'update': Option.UPDATE,
        'clear': Option.CLEAR
    }
    
    if argc <= 1:
        return Option.NONE
    return options.get(argv[1].lower(), Option.UNKNOWN)

def exit_error(msg):
    file_gitignore.close()
    sys.exit(msg)

def check_file_gitignore():
    for item in os.listdir():
        if os.path.isfile(name_gitignore):
            return open(name_gitignore, 'a')
    sys.exit('no %s file found' % name_gitignore)

def check_add(argc):
    if argc <= 2:
        exit_error('expected gitignore name')
    global file_gitignore
    file_gitignore = open(name_gitignore, 'a')

def check_remove(argc):
    if argc <= 2:
        exit_error('expected gitignore name')
    global file_gitignore
    file_gitignore = check_file_gitignore()

def check_create(argc):
    global file_gitignore
    file_gitignore = open(name_gitignore, 'w')
    print("%s created" % name_gitignore)
    if argc == 2:
        sys.exit(0)

def add(name):
    lower = name.lower()
    if lower not in names:
        exit_error('unknown gitignore ' + name)
    item = names[lower] + ext_gitignore
    url = link + item
    data = urllib.request.urlopen(url).read().decode('utf-8')
    file_gitignore.write('#gitignore-start:%s\n' % item)
    file_gitignore.write(data)
    file_gitignore.write('#gitignore-end:%s\n' % item)
    print('added', item)

def remove(name):
    lower = name.lower()
    if lower not in names:
        exit_error('unknown gitignore ' + name)
    pass

def update():
    file_gitignore = check_file_gitignore()
    pass

def clear():
    file_gitignore = check_file_gitignore()
    pass

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
    'cpp' : 'C++',
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