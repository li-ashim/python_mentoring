from datetime import datetime
from pathlib import Path
from typing import Iterator


def _get_file_type(file: Path) -> str:
    """Return type of file in Unix notation."""
    checks = {name[3:]: check for name, check in Path.__dict__.items()
              if name.startswith('is_')}
    for ftype, check in checks.items():
        if check(file):
            return ftype


def get_contents(dir: Path, all_files=False) -> Iterator[dict]:
    """
    Generate dicts with information about files in dir.

    :param dir: Path of directory in which contents are observed
    :param all_files: Flag telling whether hidden files should be included
    """
    files = (file for file in dir.iterdir()
             if all_files or not file.name.startswith('.'))

    for file in files:
        stats = file.stat()
        res = {}
        res['name'] = file.name
        res['type'] = _get_file_type(file)
        res['last_mod'] = datetime.fromtimestamp(
            stats.st_mtime).isoformat(sep=' ', timespec='seconds')
        res['size'] = stats.st_size
        res['nlink'] = stats.st_nlink
        res['mode'] = stats.st_mode

        yield res
