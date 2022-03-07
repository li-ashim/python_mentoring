from typing import Iterator

from colorama import Fore

# File type -- color mapping
colors = {'dir': Fore.CYAN}

# Reserved space for table fields
MODE = 6
NLINK = 2
SIZE = 8
LAST_MOD = 16


def display_header() -> None:
    '''Display header of table.'''
    print('Mode'.ljust(MODE),
          'Links'.ljust(NLINK),
          'Length'.ljust(SIZE),
          'Last modified'.ljust(LAST_MOD),
          'Name', sep='\t')


def display(gen: Iterator, is_long: bool = False) -> None:
    if is_long:
        for item in gen:
            print(str(item['mode']).ljust(MODE),
                  str(item['nlink']).ljust(NLINK),
                  str(item['size']).ljust(SIZE),
                  item['last_mod'].ljust(LAST_MOD),
                  colors.get(item['type'], '') + item['name'], sep='\t')
            print(Fore.RESET, end='')
    else:
        for item in gen:
            print(colors.get(item['type'], '') + item['name'], end='\t')
            print(Fore.RESET, end='')
