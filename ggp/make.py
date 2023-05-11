from urllib.parse import quote
from pathlib import Path
from argparse import ArgumentParser, FileType

base_template_path = Path(__file__).parent / "templates"


def make_script_tags(files, tag_type):
    scripts = ((file.read(), script_id) for file, script_id in files)
    return "\n".join(
        f'<script type="{tag_type}" id="{script_id}" '
        f'src="data:application/javascript,{quote(script, safe="")}"></script>'
        for script, script_id in scripts)


def create_html_file(files, workers, template, ident, strategy, title):
    if title is None:
        title = ident + " " + strategy
    if template is None:
        template = open((base_template_path / "sample.html").resolve())
    if len(workers) > 0:
        files.append((open((base_template_path / "loadworker.js").resolve()), "loadworker"))
    worker_html = make_script_tags(workers, "javascript/worker")
    script_html = make_script_tags(files, "text/javascript")
    return template.read().replace("$SCRIPTS", worker_html + "\n" + script_html).replace("$IDENT", ident) \
        .replace("$STRATEGY", strategy).replace("$TITLE", title)


def make(args):
    result = create_html_file(args.filename, args.worker, args.template, args.ident, args.strategy, args.title)
    print(result, file=args.out)


def parse_file_id_list(args):
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
    parser.add_argument('filename', nargs="*", type=parse_file_id_list,
                        help='List of main files to add.'
                             ' If you pass a comma-separated tuple, the second value is used as the id.'
                             ' Otherwise, the default id is the filename.')
    parser.add_argument('--worker', action='append', type=parse_file_id_list, default=[],
                        help='Worker scripts are added after main scripts using type=javascript/worker,'
                             ' which means they are not run by the browser, but their ids can still be'
                             ' passed to `loadWorker`.')
    parser.add_argument('--template', help='The template HTML file to use (defaults to sample.html from '
                                           'http://ggp.stanford.edu/gamemaster/gameplayers/sample.html)',
                        type=FileType('r'))
    parser.add_argument('--ident', help='The identifier for your player', default='template')
    parser.add_argument('--strategy', help='The strategy name that is displayed on the page', default='secret')
    parser.add_argument('--title', help='The title for the page (defaults to the strategy and identifier)')
    parser.add_argument('--out', help='The html file to write to (defaults to out.html)',
                            type=FileType('w'), default='out.html')
    make(parser.parse_args())
