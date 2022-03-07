import argparse
from pathlib import Path


class DirsCheck(argparse.Action):
    '''Check paths for existence and correspondense to directorys.'''
    def __call__(self, parser, namespace, values, option_string) -> None:
        try:
            iter(values)
        except TypeError:
            values = [values]

        for value in values:
            if not value.exists():
                raise argparse.ArgumentError(
                    None, f'{value} directory was not found.')
            elif not value.is_dir():
                raise argparse.ArgumentError(
                    None, f'{value}  is not a directory.')
        setattr(namespace, self.dest, values)


arg_parser = argparse.ArgumentParser(
    prog='ls',
    description='Lists information about directory contents.'
)

# Accepts multiple directories but requires all of directories to be valid
arg_parser.add_argument('dirs', type=Path, action=DirsCheck,
                        default=Path.cwd(), nargs='*',
                        help=('directory to list files for (default: ./)'))
arg_parser.add_argument('-l', action='store_true',
                        help='use long listing format')
arg_parser.add_argument('-a', action='store_true',
                        help='do not ignore entries starting with .')
