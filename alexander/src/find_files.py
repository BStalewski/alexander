'''
Module used to find in given directories files which names
meet one of crieterions.
'''

import argparse
import os
import glob

class CriterionException(Exception):
    '''Wrong search criterion(regular expression).'''
    pass

def dir_files(dirname, criterions, all_needed):
    '''Return files that meet naming criterions inside dirname
       directory's subtree.
    '''
    prev_dir = os.getcwd()
    os.chdir(dirname)
    try:
        correct_names_groups = [set(glob.glob(crit)) for crit in criterions]
        correct_names = merge_groups(correct_names_groups, all_needed)
    finally:
        os.chdir(prev_dir)
    return correct_names

def merge_groups(names_groups, all_needed):
    correct = set(names_groups[0])
    for grp in names_groups[1:]:
        correct = correct & grp if all_needed else correct | grp
    return sorted(correct)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specify search criterions.')
    parser.add_argument('--dir', metavar='.',
                       help='root search directory')
    parser.add_argument('--names', metavar='criterion', nargs='*',
                       help='file name criterions')
    parser.add_argument('--any', action='store_true',
                       help='any criterion met by file name suffices',
                       default=False)
    args = parser.parse_args()
    print(dir_files(args.dir, args.names, not args.any))

