'''
Module used to find names imported from other modules.
Analyzes code in file with regular expressions, does not import it.

checks the following patterns:
1) r'^\s*import.+?[^\\]$'
2) r'^\s*from\s+[a-zA-Z._]+\s+import.+[^\\]$'
'''

import re


def scan_files(filepaths):
    '''Return imported names by files specified by filepaths.'''
    return {filepath: scan_file(filepath) for filepath in filepaths}

def scan_file(filepath):
    '''Return imported names by file specified by filepath.'''
    scanned_file = open(filepath)
    code = scanned_file.read()
    clean_code = remove_comments(code)
    return find_imports(clean_code)



def remove_comments(code):
    '''Return code without comments.'''
    symbol = None
    no_comments_lines = []

    for line in code:
        line_without_comments, symbol = remove_comments_from_line(line, symbol)
        no_comments_lines.append(line_without_comments)

    return '\n'.join(no_comments_lines)

def remove_comments_from_line(line, comment_symbol=None):
    '''Return tuple containing line without commented part and actual
    comment symbol: \'\'\' or """ if this line is inside comment block,
    otherwise None.'''
    if comment_symbol:
        result = find_first_symbol(line, [comment_symbol])
        comment_symbol = None if result else comment_symbol
        return ('', comment_symbol)
    else:
        try:
            ind, symbol = find_first_symbol(line, ['#', "'''", '"""'])
        except TypeError:
            # no symbol found
            return (line, None)

        if symbol == '#':
            return (line[:ind], None)
        else:
            comment_symbol = symbol
            search_start = ind + len(symbol)
            result = find_first_symbol(line[search_start:], [comment_symbol])
            comment_symbol = None if result else comment_symbol
            return ('', comment_symbol)


def find_first_symbol(line, symbols):
    '''Find first occurence of any of symbols in the line of the code.
       Return tuple containing index of the found symbol and the found symbol,
       if any was found, otherwise return None.'''
    symbol_tuples = []
    for symbol in symbols:
        first_index = line.find(symbol)
        first_index = first_index if first_index != -1 else len(line)
        symbol_tuples.append((first_index, symbol))

    first_found = min(symbol_tuples)
    if first_found[1] == len(line):
        return None
    else:
        return first_found

def find_imports(code):
    '''Return list of modules that this module imports from. Use code without
    comments, because there is possibility that the module may contain code
    with commented imports or comments in the same line as import.
    '''
    module_imports = re.finditer(r'^\s*import.+?[^\\]$',
                                 code, flags=re.MULTILINE|re.DOTALL)
    # dodac dopasowanie jesli duzo \
    from_imports = re.finditer(r'^\s*from\s+[a-zA-Z._]+\s+import.+[^\\]$',
                               code, flags=re.MULTILINE|re.DOTALL)
    imported_names = {get_import_names(import_str) for import_str in module_imports}
    for from_str in from_imports:
        imported_names |= get_from_import_names(from_str)

    return imported_names

def get_import_names(import_str):
    '''Return list of module names from import statement.'''
    pass

def get_from_import_names(from_str):
    '''Return list of module names from 'from import' statement.'''
    pass
