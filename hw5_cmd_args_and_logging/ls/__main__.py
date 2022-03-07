from .cli import arg_parser
from .display_utils import display, display_header
from .fs_utils import get_contents

args = arg_parser.parse_args()

for dir in args.dirs:
    print(str(dir) + ':')
    if args.l and args.a:
        display_header()
        display(get_contents(dir, all_files=True), is_long=True)
    elif args.l:
        display_header()
        display(get_contents(dir), is_long=True)
    elif args.a:
        display(get_contents(dir, all_files=True))
    else:
        display(get_contents(dir))
    print('\n\n', end='')
