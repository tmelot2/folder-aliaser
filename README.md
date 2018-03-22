# Folder Aliaser

Alias your project folders quickly and easily! Right-click on any top-level folder in the Side Bar and choose "Alias
Folder". It's helpful to resolve name collisions or to provide friendlier names for folders.

This plugin works by **modifying your current `sublime-project` file**. Specifically, it edits the `name` property of
items in the `folders` array. If this is an issue, then the current version of this plugin won't work for you, but
please let me know so I can look at alternative solutions!

# Installation
When it's finished and I publish it, install via Package Control ([installation instructions](https://packagecontrol.io/installation) and [usage guide](https://packagecontrol.io/docs/usage)).

# Usage
Right-click on any top-level folder in the Side Bar, choose "Alias Folder", and type the alias you want. Simple!

# Contributions, issues, questions, etc.
TODO

# Thanks
This project was inspired by [rablador's FolderAlias](https://bitbucket.org/rablador/folderalias) plugin and a desire to provide an easier way to alias folders without having to manually edit a JSON file.

# License
The code is free to use. This is my first Sublime Text plugin so there are a ton of comments. Should be pretty easy to follow.
