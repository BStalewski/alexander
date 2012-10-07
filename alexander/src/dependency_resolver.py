'''
Module resolves dependencies: gets file and dependencies from its
code and figures out which exactly those dependencies are:
standard library module, package module, module from pythonpath.
'''

import os.path

class ResolverError(Exception):
    '''Unable to find module.'''
    pass


def resolve(filepath, modules):
    '''Return list of modules(as files' names) that this file
       under filepath depends on.'''
    #non_std_modules = filter(lambda mod: not is_std_mod(filepath, mod), modules)
    #return [find_mod(mod, filepath) for mod in non_std_modules]
    return [find_mod(mod, filepath) for mod in modules]

# useless
def is_std_mod(filepath, mod):
    '''Return True if mod for file with path filepath is standard,
       False otherwise.'''
    return False

def find_mod(name, filepath):
    '''Find file that represents module with the given name from the
       filepath point of view.'''
    if is_pkg_dir(os.path.dirname(filepath)) and is_pkg_import(name):
        return find_pkg_import(name, filepath)
    else:
        return None

def is_pkg_import(name):
    return name.startswith('.')

def find_pkg_import(mod_name, filepath):
    if not mod_name.startswith('..'):
        msg = ('Unable to find package import: {0} from file {1}'.
               format(mod_name, filepath))
        raise ResolverError(msg)
    
    if mod_name.startswith('...'):
        curr_path = os.path.dirname(os.path.dirname(filepath))
        mod_path = mod_name[3:]
    elif mod_name.startswith('..'):
        curr_path = os.path.dirname(filepath)
        mod_path = mod_name[2:]

    for mod_name in mod_path.split('.'):
        
        pass

def find_in_subtree(name, filepath):
    '''Try to find file that represents module with the given name in the
       path. If there is such a file, return its path, otherwise None.'''
    pass

def find_in_pythonpath(name):
    '''Try to find file that represents module with the given name in any of
       directories pointed at by PYTHONPATH.'''
    pass

def find_in_pth(name, filepath):
    '''Try to find file that represents module with the given name
       using pth files found in project root.'''
    pass
    
def is_pkg_dir(dirpath):
    init_path = os.path.join(dirpath, '__init__.py')
    return os.path.isfile(init_path)

'''
resolve C:\\p1\p2\p3\file1.py mod1 mod3
#resolve "p3\\file1.py" --prefix="C:\\p1\p2" --version=3 mod1 mod3
--> ['p1\p2\mod1', 'p1\p2\mod3']
'''
