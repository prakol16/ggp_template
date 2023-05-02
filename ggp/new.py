from pathlib import Path
from argparse import ArgumentParser, FileType

base_template_path = Path(__file__).parent / "templates"

with open((base_template_path / "sample.js").resolve()) as f:
    sample_js = f.read()

if __name__ == "__main__":
    parser = ArgumentParser(
                    prog='ggp.new',
                    description='Automatically generate a template for your player')
    parser.add_argument('out', help='The js file to write to (defaults to main.js)',
                        type=FileType('w'), nargs='?', default='main.js')
    args = parser.parse_args()
    print(sample_js, file=args.out)
