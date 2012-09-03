from alexander.src.find_files import dir_files
import os
import unittest

class testDir(unittest.TestCase):
    def setUp(self):
        self.prev_dir = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        print('*' * 80)

    def tearDown(self):
        os.chdir(self.prev_dir)

    def basic_test(self):
        dirname = 'testdir_1'
        criterions = ['myfile_1.py']
        all_needed = True
        expected = [os.path.join('testdir_1', 'myfile_1.py')]
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

    def same_dir_test(self):
        dirname = '.'
        criterions = ['myfile_2.py']
        all_needed = True
        expected = ['myfile_2.py']
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

    def extension_test(self):
        dirname = 'testdir_3'
        criterions = ['*.py']
        all_needed = True
        expected = [os.path.join('testdir_3', 'pyfile1.py'),
                    os.path.join('testdir_3', 'pyfile2.py')]
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

    def subdir_test(self):
        dirname = 'testdir_4'
        criterions = ['*.py']
        all_needed = True
        expected = [os.path.join('testdir_4', 'pkg', 'pyfile1.py'),
                    os.path.join('testdir_4', 'pyfile1.py'),
                    os.path.join('testdir_4', 'pyfile2.py')]
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

    def many_and_criterions_test(self):
        dirname = 'testdir_5'
        criterions = ['*py*', '*2*']
        all_needed = True
        expected = [os.path.join('testdir_5', 'pyfile2.py'),
                    os.path.join('testdir_5', 'python2.txt')]
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

    def many_optional_criterions_test(self):
        dirname = 'testdir_6'
        criterions = ['*file1*', '*on2?*']
        all_needed = False
        expected = [os.path.join('testdir_6', 'pyfile1.py'),
                    os.path.join('testdir_6', 'python2.txt'),
                    os.path.join('testdir_6', 'python22.txt')]
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

    def ored_criterion_test(self):
        dirname = 'testdir_7'
        criterions = ['*le[23]*']
        all_needed = False
        expected = [os.path.join('testdir_7', 'pyfile2.py'),
                    os.path.join('testdir_7', 'pyfile3.pyc')]
        self.assertEqual(dir_files(dirname, criterions, all_needed), expected)

