from alexander.src.find_imported import scan_files
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
        filepaths = ['file1.py']
        expected = {
            'file1.py': [
                'a1', 'a2', 'a3', 'a4', 'a5',
                'b2', 'b4', 'b5', 'c5',
                'd1.x', 'd2.x', 'd2.y', 'd3.x', 'd3.y'
            ]
        }
        self.assertEqual(scan_files(filepaths), expected)

    def cont_char_test(self):
        filepaths = ['file2.py']
        expected = {
            'file2.py': [
                'a1', 'a2', 'a3', 'b1', 'b2', 'b3',
                'c1.x', 'c2.y', 'c3.y', 'c3.y2'
            ]
        }
        self.assertEqual(scan_files(filepaths), expected)

    def false_positives_test(self):
        filepaths = ['file3.py']
        expected = {
            'file3.py': []
        }
        self.assertEqual(scan_files(filepaths), expected)

    def whitespace_test(self):
        filepaths = ['file4.py']
        expected = {
            'file4.py': [
                'a1', 'a2', 'a3', 'a4', 'b1', 'b3',
                'c1.x', 'c2.x', 'c3.x'
            ]
        }
        self.assertEqual(scan_files(filepaths), expected)

    def many_files_test(self):
        filepaths = ['file1.py', 'file4.py']
        expected = {
            'file1.py': [
                'a1', 'a2', 'a3', 'a4', 'a5',
                'b2', 'b4', 'b5', 'c5',
                'd1.x', 'd2.x', 'd2.y', 'd3.x', 'd3.y'
            ],
            'file4.py': [
                'a1', 'a2', 'a3', 'a4', 'b1', 'b3',
                'c1.x', 'c2.x', 'c3.x'
            ]
        }
        self.assertEqual(scan_files(filepaths), expected)

    def nested_paths_test(self):
        path1 = os.path.join('dir_1', 'nested.py')
        path2 = os.path.join('dir_2', 'dir_2_1', 'double_nested.py')
        filepaths = [path1, path2]
        expected = {}
        expected[path1] = ['a1', 'b1']
        expected[path2] = ['b1', 'c1.x']
        self.assertEqual(scan_files(filepaths), expected)

