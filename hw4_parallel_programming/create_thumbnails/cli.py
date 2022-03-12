import argparse
from pathlib import Path


class PathCheck(argparse.Action):
    '''Applies file existence check.'''
    def __call__(self, parser, namespace, values, option_string) -> None:
        if values.exists() and values.is_file():
            setattr(namespace, self.dest, values)
        else:
            # this Error raises because of beautiful output
            raise argparse.ArgumentError(None, f'{values} file was not found.')


class PositiveCheck(argparse.Action):
    '''Applies positiveness check.'''
    def __call__(self, parser, namespace, values, option_string) -> None:
        try:
            it = iter(values)
        except TypeError:
            it = [values]

        if any(map(lambda x: x <= 0, it)):
            raise argparse.ArgumentError(None,
                                         (f'{option_string} value(s) '
                                          'must be positive ({values} given)'))

        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(
    prog='create_thumbnails',
    description='Downloads images and make thumbnails from it.'
)

parser.add_argument('source', type=Path, action=PathCheck,
                    help=('path to file containing links to the images '
                          '(one link per line)'))
parser.add_argument('-jobs', type=int, default=1, action=PositiveCheck,
                    help='number of threads to use (default: %(default)s)')
parser.add_argument('-max_res', nargs=2, type=int, default=(100, 100),
                    action=PositiveCheck, metavar=('X', 'Y'),
                    help='max resolution of thumbnails (default: %(default)s)')
parser.add_argument('-dest_dir', default='./thumbnails/', type=Path,
                    help=('path to directory to store results '
                          '(created if not exsist) (default: %(default)s)'))
