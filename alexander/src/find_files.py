'''
Module used to find in given directories files which names
meet one of crieterions.
'''

import argparse
import os
import re
import fnmatch

class CriterionException(Exception):
    '''Wrong search criterion(regular expression).'''
    pass

def dir_files(dirname, criterions, all_needed):
    '''Return files that meet naming criterions inside dirname
       directory's subtree.
    '''
    correct_names = []
    full_criterions = translate_criterions(criterions)
    check_criterions(full_criterions)
    all_names = os.listdir(dirname)
    print('all_names', all_names)
    for name in all_names:
        full_path = create_path(dirname, name)
        if os.path.isfile(full_path):
            print('File {0} in directory {1}'.format(name, dirname))
            if criterions_met(name, full_criterions, all_needed):
                print('File {0} is OK'.format(name))
                correct_names.append(full_path)
        else:
            print('Directory {0} in directory {1}'.format(name, dirname))
            correct_names += dir_files(full_path, full_criterions, all_needed)

    return correct_names

def translate_criterions(criterions):
    '''Change forms of criterions so that they can be passed to
       module re: glob -> re.
       Return criterions in translated form'''
    return [fnmatch.translate(criterion) for criterion in criterions]

def check_criterions(criterions):
    '''Return True if passed criterions are correct, False otherwise.'''
    for criterion in criterions:
        try:
            re.compile(criterion)
        except re.sre_constants.error:
            raise CriterionException('Bad criterion' + criterion)

def criterions_met(name, criterions, all_needed):
    '''Return True if file does meet naming criterions, False otherwise.'''
    criterion_check = (criterion_met(name, crit) for crit in criterions)
    if all_needed:
        return all(criterion_check)
    else:
        return any(criterion_check)

def criterion_met(name, criterion):
    '''Return True if file does meet naming criterion, False otherwise.'''
    return re.match(criterion, name) is not None

def create_path(dirname, name):
    '''Simple function that returns path created from concatenating dirname
       and name.
    '''
    return os.path.join(dirname, name) if dirname != '.' else name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specify search criterions.')
    parser.add_argument('--dirs', metavar='.', nargs='+',
                       help='root search directories')
    parser.add_argument('--names', metavar='criterion', nargs='*',
                       help='file name criterions')
    parser.add_argument('--any', action='store_true',
                       help='any criterion met by file name suffices',
                       default=False)
    print('START')
    args = parser.parse_args()
    print(args)
    print('END')

