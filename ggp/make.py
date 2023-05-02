from urllib.parse import quote
from pathlib import Path
from argparse import ArgumentParser, FileType

base_template_path = Path(__file__).parent / "templates"

with open((base_template_path / "sample.html").resolve()) as f:
    sample_html = f.read()


def create_html_file(files, template, ident, strategy, title):
    if title is None:
        title = ident + " " + strategy
    if template is None:
        template = sample_html
    scripts = (file.read() for file in files)
    script_html = "\n".join(
        f'<script type="text/javascript" src="data:application/javascript,{quote(script, safe="")}"></script>'
        for script in scripts)
    return template.replace("$SCRIPTS", script_html).replace("$IDENT", ident) \
        .replace("$STRATEGY", strategy).replace("$TITLE", title)


def make(args):
    result = create_html_file(args.filename, args.template, args.ident, args.strategy, args.title)
    print(result, file=args.out)


if __name__ == "__main__":
    parser = ArgumentParser(
                    prog='ggp.make',
                    description='Automatically generate an HTML for your player given the javascript source')
    parser.add_argument('filename', nargs="+", type=FileType('r'))
    parser.add_argument('--template', help='The template HTML file to use (defaults to sample.html from '
                                               'http://ggp.stanford.edu/gamemaster/gameplayers/sample.html)')
    parser.add_argument('--ident', help='The identifier for your player', default='template')
    parser.add_argument('--strategy', help='The strategy name that is displayed on the page', default='secret')
    parser.add_argument('--title', help='The title for the page (defaults to the strategy and identifier)')
    parser.add_argument('--out', help='The html file to write to (defaults to out.html)',
                            type=FileType('w'), default='out.html')
    make(parser.parse_args())
