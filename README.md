# gitignore-modifier
Application that allows to easily add and remove template gitignore entries.

Written in Python 3.6.

## Concept

The .gitignore templates are taken from [here](https://github.com/github/gitignore).

Any template that you type must match (case-insensitive) the name of one of the templates there.
The name is the name of the file without the extension. So for, the pattern [Eclipse](https://github.com/github/gitignore/blob/master/Global/Eclipse.gitignore), the name would be
"Eclipse".

The program searches the current repository (from which the program is called) to find
a .gitignore file.

#### Additional info

Each .gitignore template is preceded by a line `#gitignore-start:<dir/><name>.gitignore` and is followed by
a line `#gitignore-end:<dir/><name>.gitignore`. `<dir/>` is there for patterns within a
subdirectory. For instance, for Eclipse, the `<dir/><name>` part would print `Global/Eclipse`.

## Errors
On Mac, there may be an error using urllib. To fix it, you can call
`pip install --upgrade certifi` to update the certifi package.

## Current functionality

- Add
- Create
- Remove
- Update
- Clean
- Local

### Add

Adds templates to the .gitignore file. It takes any number of parameters corresponding
to the names of templates to add.

    add [names]

If the .gitignore file does not exist, creates a new one.

Existing templates are updates and new ones are added.

### Remove

Removes templates from the .gitignore file. It parses the file to find appropriate
[start and end sections](#additional-info), and removes them from the file.

    remove [names]

If the .gitignore file does not exist, does nothing.

### Create

If the .gitignore file does not exist, creates a new one, else **overwrites** it.

Then does the equivalent of `add` if there are template names.

    create [names]?

### Update

Updates the .gitignore file by refetching up-to-date information for each template in it.

    update

If the .gitignore file does not exist, does nothing.

Equivalent to using `add` with all the templates to update.

### Clean

Removes all templates from the .gitignore file.

    clean

If the .gitignore file does not exist, does nothing.

### Local

Local has two suboptions:
 -  Set: must be followed by a path name. It sets a local directory to fetch gitignore
    templates from.
 -  Reset: resets the local directory to `None`.

What happens is that in the script there is a variable called `local_path`. If it set
to `None`, then gitignore templates are fetched from the link given above. If it is
set to anything else, then they're fetched from the specified directory. After execution,
that variable is changed within the script itself. `set` makes it equal to a string equal
to the path given and `reset` makes it equal to `None`.

For instance, `local set /Users/Pat-Laugh/gitignore` would make it so when `add c++`
is called, the file "/Users/Pat-Laugh/gitignore/C++.gitignore" is fetched. The directory
provided must be correct. It is only checked when a file is actually fetched. If it is
incorrect, then an error will be thrown (at the moment it is an uncaught error).

## Gitignore links

Adding the name of a gitignore template within another template will make the parser
automatically fetch that template. For example, the template for Fortran consists of a
single line "`C++.gitignore`". This tells the parser to fetch the C++ gitignore. There
can be multiple links, they can be put on anywhere within the file, but must be the only
thing in a line. Putting them in a comment (adding '#' before them) is allowed.

## Examples

You can type: `python gitignore.py add eclipse java` to add the templates for the
Eclipse IDE and Java language.

Type `python gitignore.py add linux macos windows` to add related templates.

`add` and create `create` behave nearly the same way. Most of the time it's probably better to
use `add` than `create`, unless you specifically want to make sure there are only the templates
that you pass as parameters in the .gitignore file.

Type `python gitignore.py remove eclipse java` to remove the templates previously added.

Type `python gitignore.py update` to update current templates.

Type `python gitignore.py clear` to remove all templates.
