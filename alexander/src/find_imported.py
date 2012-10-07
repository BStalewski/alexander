'''
Module used to find names imported from other modules.
Analyzes code in file with regular expressions, does not import it.

At first removes comments and merges lines with continuation byte (\),
then it finds the following patterns:
1) r'^\s*import\s+.+?$'
2) r'^\s*from\s+[a-zA-Z._0-9]+\s+import.+?$'
and extracts modules' names from them.
'''

import re
import argparse


def scan_files(filepaths):
    '''Return imported names by files specified by filepaths.'''
    return {filepath: scan_file(filepath) for filepath in filepaths}

def scan_file(filepath):
    '''Return imported names by file specified by filepath.'''
    scanned_file = open(filepath)
    code = scanned_file.read()
    no_comments_code = remove_comments(code)
    clean_code = replace_cont_char(no_comments_code)
    return find_imports(clean_code)

def remove_comments(code):
    '''Return code without comments.'''
    symbol = None
    no_comments_lines = []

    for line in code.split('\n'):
        line_without_comments, symbol = remove_comments_from_line(line, symbol)
        no_comments_lines.append(line_without_comments)

    return '\n'.join(no_comments_lines)

def remove_comments_from_line(line, comment_symbol=None):
    '''Return tuple containing line without commented part and actual
    comment symbol: \'\'\' or """ if this line is inside comment block,
    otherwise None.'''
    if comment_symbol:
        end_found = find_first_symbol(line, [comment_symbol])
        comment_symbol = None if end_found else comment_symbol
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
            repeated = find_first_symbol(line[search_start:], [comment_symbol])
            comment_symbol = None if repeated else comment_symbol
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
    if first_found[0] == len(line):
        return None
    else:
        return first_found

def replace_cont_char(code):
    '''Replace continuation characters with single space.'''
    return re.sub(r'\\\n', ' ', code)

def find_imports(code):
    '''Return list of modules that this module imports from. Work on code
       without comments and continuation characters.'''
    module_imports = re.finditer(r'^\s*import\s+.+?$',
                                 code, flags=re.MULTILINE|re.DOTALL)
    from_imports = re.finditer(r'^\s*from\s+[a-zA-Z._0-9]+\s+import.+?$',
                               code, flags=re.MULTILINE|re.DOTALL)

    names = set()
    for from_stat in from_imports:
        names |= get_from_import_names(from_stat.group())
    for import_stat in module_imports:
        names |= get_import_names(import_stat.group())

    return sorted(names)

def get_import_names(import_str):
    '''Return set of module names from import statement.'''
    names = set()
    import_cut_str = re.sub(r'^\s*import\s+', '', import_str)
    import_parts = import_cut_str.split(',')
    for part in import_parts:
        clean_part = part.strip()
        mod_name = clean_part.split()[0] if ' ' in clean_part else clean_part
        names.add(mod_name)

    return names

def get_from_import_names(from_str):
    '''Return set of module names from 'from import' statement
       in the following form: from a import b, c -> {'a.b', 'a.c'}.'''
    from_cut_str = re.sub(r'^\s*from\s+', '', from_str)
    import_cut_str = re.sub(r'\s+import\s+', ' ', from_cut_str)
    as_cut_str = re.sub(r'\s+as\s+[a-zA-Z_0-9]+\s*', '', import_cut_str)
    parts = as_cut_str.split()
    from_part = parts[0]
    return {from_part + '.' + what_part.strip(',') for what_part in parts[1:]}

if __name__ == '__main__':
    descr = 'Pass paths to files to be checked which modules they import.'
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('paths', metavar='PATH', nargs='+',
                        help='paths to files to be checked')
    args = parser.parse_args()
    
    print(scan_files(args.paths))

