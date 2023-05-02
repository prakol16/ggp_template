# Toolchain for Writing General Game Players

This simple script allows you to build
and organize sophisticated general game playing (GGP)
projects. Currently, players are defined by a single `html` file,
which means that projects are either confined to a single file
or require a lot of tedious, error-prone manual copy-and-paste if functionality
is spread across different files.

This script allows you to define *only* the functionality
for the player that you are creating, avoiding all the boilerplate
and copying and pasting. It also allows you to manage slightly larger projects
by generating an `html` file from a template and (potentially multiple)
given javascript files.

## Usage

To create a new player from the sample template, run

```
python ggp_template.py new myplayer.js
```

To build an HTML file from a player, run

```
python ggp_template.py make myplayer.js --out=out.html --ident=your_identifier
```

You can build multiple javascript files by simply passing multiple
arguments (no dependency resolution is done; the scripts are added
to the HTML file in the order they are passed in):

```
python ggp_template.py make lib.js myplayer.js --out=out.html --ident=your_identifier
```

## Options

The `make` subcommand takes the following options:
  - `template` The template HTML file to use (defaults to [sample.html](http://ggp.stanford.edu/gamemaster/gameplayers/sample.html))        
  - `ident` The identifier for your player
  - `strategy` The strategy name that is displayed on the page
  - `title` The title for the page (defaults to the strategy and identifier)
  - `out` The html file to write to (defaults to stdout)

While javascript files are convereted to `data:text,` (hence URI encoded),
none of the other options are escaped. Therefore,
if the `title` contains valid HTML, it will simply be inserted into the HTML
file without any extra escaping.

## Recommendations

Add this repository to your PYTHONPATH so that you can
access the file from anywhere.

Most editors will allow you to set up a custom build
command. In vscode, for example, you can create a `tasks.json`
file in the project directory and set this to be the default
build task as described [here](https://code.visualstudio.com/docs/editor/tasks).
