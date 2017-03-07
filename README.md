# gitignore-modifier
Application that allows to easily add and remove template gitignore entries

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

##### Basic implementation

- Add

##### Not implemented

- Remove
- Create
- Update
- Clean

### Add

Adds templates to the .gitignore file. It takes any number of parameters corresponding
to the names of templates to add.

    add [names]

At the moment, only the option to add templates is available. It merely fetches the template
and appends it at the bottom of the local. It doesn't bother checking for duplicates.

You can type: `python gitignore.py add eclipse` to add the .gitignore for the Eclipse IDE.

### Remove

Removes templates from the .gitignore file. It parses the file to find appropriate
[start and end sections](#additional-info), and removes them from
the file.

    remove [names]

### Create

Creates a .gitignore file if it is not present, then adds templates to it.

    create [names]

### Update

Updates the .gitignore file by refetching up-to-date information for each template in it.

    update

### Clean

Removes all templates from the .gitignore file.

    clean
