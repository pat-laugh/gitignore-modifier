import sys, os

name_gitignore = '.gitignore'
file_gitignore = None

def main(argc, argv):
    check_file_gitignore()
    if argc <= 1:
        print('no argument provided')
        sys.exit(0)
    if argv[1] == 'add':
        check_args(argc, argv, add)
    elif argv[1] == 'remove':
        check_args(argc, argv, remove)
    elif argv[1] == 'update':
        update()
    elif argv[1] == 'clear':
        clear()
    else:
        print('unknown argument', argv[1])

def check_file_gitignore():
    for item in os.listdir():
        if os.path.isfile(name_gitignore):
            file_gitignore = open(name_gitignore, 'a')
            return
    print('no', name_gitignore, 'file found')
    sys.exit(1)

def check_args(argc, argv, func):
    if argc <= 2:
        print('expected gitignore name')
    for name in argv[2:]:
        func(name)

def add(name):
    lower = name.lower()
    if lower not in names:
        print('unknown gitignore', name)
    pass

def remove(name):
    lower = name.lower()
    if lower not in names:
        print('unknown gitignore', name)
    pass

def update():
    pass

def clear():
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