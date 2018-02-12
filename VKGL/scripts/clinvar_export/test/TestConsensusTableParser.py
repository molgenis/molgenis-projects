import unittest
import sys
import json

sys.modules['molgenis'] = __import__("mock_molgenis")
sys.modules['MolgenisConfigParser'] = __import__("mock_config")
sys.path.insert(0, '..')

from ConsensusTableParser import ConsensusTableParser

class ConsensusTableTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = ConsensusTableParser(use_raw=False, export=False,
                                               raw_file=open("test.json", "w"))

    def tearDown(self):
        self.parser = None

    def test_correct_output(self):
        self.assertEqual(len(self.parser.labClassifications['lab1']), 2,
                             "Two of three cases that should pass hava a classification of lab1")
        self.assertEqual(len(self.parser.labClassifications['lab2']), 2,
                             "Two of three cases that should pass hava a classification of lab2")
        self.assertEqual(len(self.parser.labClassifications['lab3']), 3,
                             "Two of three cases that should pass hava a classification of lab3")

    def test_correct_omim_code(self):
        self.assertEqual(self.parser.labClassifications['lab1'][0]['omim'], '123456')
        self.assertEqual(self.parser.labClassifications['lab1'][1]['omim'], '456789')
        self.assertEqual(self.parser.labClassifications['lab2'][0]['omim'], '123456')
        self.assertEqual(self.parser.labClassifications['lab2'][1]['omim'], '345678')
        self.assertEqual(self.parser.labClassifications['lab3'][0]['omim'], '123456')
        self.assertEqual(self.parser.labClassifications['lab3'][1]['omim'], '456789')
        self.assertEqual(self.parser.labClassifications['lab3'][2]['omim'], '345678')

    def test_generated_raw_file_correct(self):
        raw_output = json.loads(open("test.json").read())
        output = self.parser.labClassifications
        self.assertAlmostEqual(raw_output, output)

def suite():
    tests = ['test_correct_output', 'test_correct_omim_code', 'test_generated_raw_file_correct']
    return unittest.TestSuite(map(ConsensusTableParser, tests))


if __name__ == '__main__':
    suite()
