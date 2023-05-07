import os.path
from urllib.parse import quote
from pathlib import Path
from argparse import ArgumentParser, FileType

base_template_path = Path(__file__).parent / "templates"

with open((base_template_path / "sample.html").resolve()) as f:
    sample_html = f.read()


def create_html_file(files, workers, template, ident, strategy, title):
    if title is None:
        title = ident + " " + strategy
    if template is None:
        template = sample_html
    worker_scripts = ((file.read(), script_id) for (file, script_id) in workers)
    scripts = (file.read() for file in files)
    worker_html = "\n".join(
        f'<script type="javascript/worker" id="{script_id}" src="data:application/javascript,{quote(script, safe="")}'
        for script, script_id in worker_scripts)
    script_html = "\n".join(
        f'<script type="text/javascript" src="data:application/javascript,{quote(script, safe="")}"></script>'
        for script in scripts)
    return template.replace("$SCRIPTS", worker_html + "\n" + script_html).replace("$IDENT", ident) \
        .replace("$STRATEGY", strategy).replace("$TITLE", title)


def make(args):
    result = create_html_file(args.filename, args.worker, args.template, args.ident, args.strategy, args.title)
    print(result, file=args.out)


def parse_worker(args):
    ls = args.split(",", 1)
    path = Path(ls[0])
    file = open(path, "r")
    if len(ls) == 1:
        script_id = path.stem
    else:
        script_id = ls[1]
    return file, script_id


if __name__ == "__main__":
    parser = ArgumentParser(
                    prog='ggp.make',
                    description='Automatically generate an HTML for your player given the javascript source')
    parser.add_argument('filename', nargs="*", type=FileType('r'))
    parser.add_argument('--worker', action='append', type=parse_worker,
                        help='Worker scripts are added before main scripts using type=javascript/worker.'
                             ' If you pass a comma-separated tuple, the second value is used as the id.'
                             ' Otherwise, the default id is the filename.')
    parser.add_argument('--template', help='The template HTML file to use (defaults to sample.html from '
                                           'http://ggp.stanford.edu/gamemaster/gameplayers/sample.html)')
    parser.add_argument('--ident', help='The identifier for your player', default='template')
    parser.add_argument('--strategy', help='The strategy name that is displayed on the page', default='secret')
    parser.add_argument('--title', help='The title for the page (defaults to the strategy and identifier)')
    parser.add_argument('--out', help='The html file to write to (defaults to out.html)',
                            type=FileType('w'), default='out.html')
    make(parser.parse_args())
