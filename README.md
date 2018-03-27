# Folder Aliaser

Alias your project folders quickly and easily! Right-click on any top-level folder in the Side Bar and choose "Alias
Folder...". It's helpful to resolve name collisions or to provide friendlier names for folders.

This plugin works by **modifying your current `sublime-project` file**. Specifically, it edits the `name` property of
items in the `folders` array. If this is an issue, then the current version of this plugin won't work for you, but
please let me know so I can look at alternative solutions!

There exists a similar project (FolderAlias, see Thanks below) that is no longer maintained. This project exists to be
simpler (from both user and code perspectives) and maintained.

# Installation
Install via Package Control ([installation instructions](https://packagecontrol.io/installation) and [usage guide](https://packagecontrol.io/docs/usage)).

Open the Goto Anything palette, run Package Control: Install Package, and select Folder Aliaser.

# Usage
Right-click on any top-level folder in the Side Bar, choose "Alias Folder", and type the alias you want. Simple!

# Contributions, issues, questions, etc.
Please feature branch from `master` and submit a pull request. And please submit any issues you find!

This is my first Sublime Text plugin so there are a ton of comments; should be pretty easy to follow.

# Thanks
This project was inspired by [rablador's FolderAlias](https://bitbucket.org/rablador/folderalias) plugin and a desire to provide an easier way to alias folders without having to manually edit a JSON file.

# License
The code is free to use.