# Gitignore Modifier

CLI tool to easily add and remove Git `.gitignore` templates obtained from
https://github.com/github/gitignore. Instead of manually writing or copying what
files to ignore for your project, you can use them instead!

For instance, for projects written in Python, you can safely ignore the
directory `__pycache__/` and many other files, included in
[`Python.gitignore`](https://github.com/github/gitignore/blob/master/Python.gitignore).
Calling the following will write the contents of that file in `./.gitignore`:
```
gitignore add python
```

## Installation

This is written in Python 3.5. It also uses
https://github.com/simonwhitaker/gibo as a back end. Make sure to have the
required Python version and the gibo executable on the PATH (like in `~/bin/`).

You can then also put this project's executable on the PATH.

## Usage

-	`add [<name>...]`: create `.gitignore` if needed, and add templates
-	`clear`: remove all templates
-	`help`: display the usage text
-	`list`: list templates in `.gitignore`
-	`remove <name>...`: remove templates
-	`update [<name>...]`: update all or specified templates to latest version

## Implementation

Within the `.gitignore`, each template is preceded by the line
`##gitignore-start:<name>` and followed by the line `##gitignore-end:<name>`.
This allows the script to parse `.gitignore` file and know which templates are
already within.

To get the content of templates, the script calls
[gibo](https://github.com/simonwhitaker/gibo) and parses its output
appropriately.

## Gitignore links (do I want to do this?)

Adding the name of a gitignore template within another template will make the
parser automatically fetch that template. For example, the template for Fortran
consists of a single line "`C++.gitignore`". This tells the parser to fetch the
C++ gitignore. There can be multiple links, and they can be put on anywhere
within the file, but they must be the only thing in a line. Putting them in a
comment (adding '#' before them) is allowed.

## Caveats

The templates might include files you don't want to ignore. If so, you'll have
to manually edit the `.gitignore` file or force Git to not ignore them.
