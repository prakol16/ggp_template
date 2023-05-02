from urllib.parse import quote
import argparse
from argparse import ArgumentParser


sample_js = """//==============================================================================
// The code below defines a basic legal player.
// Autogenerated by ggp_template.py
// Replace the definitions of ping, start, play, stop, abort with your code.
//==============================================================================

var role = 'robot';
var startclock = 10;
var playclock = 10;

var library = [];
var roles = [];
var state = [];
var move = 'nil';

//==============================================================================

function ping() {
    return 'ready'
}

function start(r, rs, sc, pc) {
    role = r;
    library = definemorerules([], rs.slice(1));
    roles = findroles(library);
    state = findinits(library);
    startclock = numberize(sc);
    playclock = numberize(pc);
    return 'ready'
}

function play(move) {
    if (move !== nil) {
        state = simulate(move, state, library)
    };
    if (findcontrol(state, library) !== role) {
        return false
    };
    return findlegalx(state, library)
}

function stop(move) {
    return false
}

function abort() {
    return false
}

//==============================================================================
// End of player code
//=============================================================================="""

sample = """<html>

<!--=======================================================================-->

<head>
  <title>$TITLE</title>
  <script type='text/javascript' src='http://epilog.stanford.edu/javascript/epilog.js'></script>
  <script type='text/javascript' src='http://gamemaster.stanford.edu/javascript/localstorage.js'></script>
  <script type='text/javascript' src='http://gamemaster.stanford.edu/reasoning/general.js'></script>
  <script type='text/javascript'>
    var manager = 'manager';
    var player = '$IDENT';
  </script>
$SCRIPTS
</head>

<!--=======================================================================-->

<body bgcolor='#aabbbb' onload='doinitialize()'>
  <center>
    <table width='720' cellspacing='0' cellpadding='40' bgcolor='#ffffff'>
      <tr>
        <td>

<!--=======================================================================-->

<center>
  <table width='640' cellpadding='0'>
    <tr>
      <td width='180' align='center' valign='center'>
        <img width='130' src='http://gamemaster.stanford.edu/images/ggp.jpg'/>
      </td>
      <td align='center'>
        <span style='font-size:18pt'>&nbsp;</span>
        <span style='font-size:32pt'>Gamemaster</span><br/>
      </td>
      <td width='180' align='center' style='color:#000066;font-size:18px'>
        <i>General<br/>Game<br/>Playing</i>
      </td>
    </tr>
  </table>
</center>

<!--=======================================================================-->

<br/>
<table width='640' cellpadding='8' cellspacing='0' bgcolor='#f4f8f8' border='1'>
  <tr height='40'>
     <td align='center'>
<table style='color:#000066;font-size:18px'>
  <tr>
    <td>
Protocol: localstorage<br/>
Strategy: $STRATEGY<br/>
Identifier: <span id='player'>$IDENT</span> <img src="http://gamemaster.stanford.edu/images/pencil.gif" onclick='doplayer()'/>
    </td>
  </tr>
</table>
    </td>
  </tr>
</table>
<br/>

<!--=======================================================================-->

<center>
  <br/>
  <textarea id='transcript' style='font-family:courier' rows='30' cols='80' readonly></textarea>
</center>

<!--=======================================================================-->

        </td>
      </tr>
    </table>
  </center>
</body>

<!--=======================================================================-->

</html>
"""


def create_html_file(files, template, ident, strategy, title):
    if title is None:
        title = strategy + " " + ident
    if template is None:
        template = sample
    scripts = (file.read() for file in files)
    script_html = "\n".join(f'<script type="text/javascript" src="data:application/javascript,{quote(script, safe="")}"></script>'
                            for script in scripts)
    return template.replace("$SCRIPTS", script_html).replace("$IDENT", ident) \
        .replace("$STRATEGY", strategy).replace("$TITLE", title)


def make(args):
    result = create_html_file(args.filename, args.template, args.ident, args.strategy, args.title)
    print(result, file=args.out)


def new_proj(args):
    print(sample_js, file=args.out)


if __name__ == "__main__":
    parser = ArgumentParser(
                    prog='ggp_template',
                    description='Automatically generate a template for your player')
    subparsers = parser.add_subparsers(dest='subcommand', required=True, help='Specify whether to create a new project (new) or compile (make)')
    make_parse = subparsers.add_parser("make", help="Compile a list of javascript files")
    make_parse.add_argument('filename', nargs="+", type=argparse.FileType('r'))
    make_parse.add_argument('--template', help='The template HTML file to use (defaults to a sample.html from '
                                           'http://ggp.stanford.edu/gamemaster/gameplayers/sample.html)')
    make_parse.add_argument('--ident', help='The identifier for your player', default='template')
    make_parse.add_argument('--strategy', help='The strategy name that is displayed on the page', default='secret')
    make_parse.add_argument('--title', help='The title for the page (defaults to the strategy and identifier)')
    make_parse.add_argument('--out', help='The html file to write to (defaults to stdout)', type=argparse.FileType('w'), default='-')
    make_parse.set_defaults(func=make)

    new_proj_parse = subparsers.add_parser("new", help="Create a new js player from the sample template")
    new_proj_parse.add_argument('out', help='The js file to write to (defaults to stdout)', type=argparse.FileType('w'), nargs='?', default='-')
    new_proj_parse.set_defaults(func=new_proj)

    args = parser.parse_args()
    args.func(args)