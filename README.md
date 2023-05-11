# Toolchain for writing General Game Players

This simple script allows you to build
and organize sophisticated general game playing (GGP)
projects. Currently, players are defined by a single `.html` file,
which means that projects are either confined to a single file
or require a lot of tedious, error-prone manual copy-and-paste if functionality
is spread across different files.

This script allows you to define *only* the functionality
for the player that you are creating, avoiding all the boilerplate
and copying and pasting. It also allows you to manage larger projects
by generating an `html` file from a template and (potentially multiple)
javascript files. Finally, it allows you to load web workers
in a natural and easy way.

## Setup
Make sure you have python and pip installed. Then run the following
in a terminal:

```
pip install ggp-template
```

## Usage

To create a new player from the sample template, run

```
python -m ggp.new myplayer.js
```

To build an HTML file from a player, run

```
python -m ggp.make myplayer.js --ident=your_identifier
```

You can build multiple javascript files by simply passing multiple
arguments (no dependency resolution is done; the scripts are added
to the HTML file in the order they are passed in):

```
python -m ggp.make lib.js myplayer.js --ident=your_identifier
```

## Options

The `make` subcommand takes the following options:
  - `worker` Worker scripts are added after main scripts using `type=javascript/worker`, which means they are not run by the browser, but their ids can still be passed to `loadWorker`.
  - `template` The template HTML file to use (defaults to sample.html from http://ggp.stanford.edu/gamemaster/gameplayers/sample.html)
  - `ident` The identifier for your player
  - `strategy` The strategy name that is displayed on the page
  - `title` The title for the page (defaults to the strategy and identifier)

While javascript files are converted to `data:text,` (hence URI encoded),
none of the other parameters are escaped. Therefore,
if the `title` contains valid HTML, it will simply be inserted into the HTML
file without any extra escaping.

All script tags will be created with an `id` corresponding by default to the stem of the file.
This is useful for loading web workers (see below).

## Using WebWorkers

If any `--worker` flags are passed, an extra file `loadworker.js` is automatically loaded.
To use `loadWorker`, in any file, simply call:

```
const worker = loadWorker(scriptId, dependencies, nestedDependencies);
```

Here, `scriptId` is the id of a script that was passed into `ggp.make`. Note that the default
id for a file is the file name stem (e.g. the id for `myplayer/lib/shuffle.js` would be `shuffle`).
You can change the id by passing it explicitly if you wish: `python -m ggp.make myplayer/lib/shuffle.js,newid` would
load `myplayer/lib/shuffle.js` with id `newid`.

If the worker itself needs to load new workers, pass those workers and their dependencies into `nestedDependencies`.
Note that this worker will then have access to the script to pass it into `nestedDependencies` itself, so this
allows arbitrarily nested WebWorkers.

Note that all main worker scripts should be prefixed with `--worker`, so that the browser does not execute them on 
the top page. Files that simply define utility functions, however, can be loaded without `--worker`,
even if they are used only by web workers.

## Recommendations

Most editors will allow you to set up a custom build
command. In vscode, for example, you can create a `tasks.json`
file in the project directory and set this to be the default
build task as described [here](https://code.visualstudio.com/docs/editor/tasks).

If you want more sophisticated tooling, such as automatic dependency resolution
or compiling from e.g. Typescript, use `webpack`.
