__author__ = 'dstrohl'

import unittest
from python_log_indenter.pli import IndentHelper


class TestIndentedHelper(unittest.TestCase):
    def test_indented_helper(self):

        sh = IndentHelper(spaces=1, indent_char='.')
    
        self.assertEqual(sh(), "")
    
        sh.a(2)

        sh += 3
        tmp_test = len(sh)
        self.assertEqual(tmp_test, 5)

        sh -= 3
        self.assertEqual(len(sh), 2)
    
        sh.indent_set(3)

        self.assertEqual(sh(0), '...')
    
        self.assertEqual(str(sh.a()), '....')

        self.assertEqual(sh.s().__, '...')
    
        self.assertEqual(sh.indent(), '...')
    
        sh.push()
        self.assertEqual(sh.a().indent(), '....')
        
        self.assertEqual(sh.a(2).indent(), '......')
        
        self.assertEqual(sh.pop().indent(), '...')
    
        self.assertEqual(sh.a().indent(indent_char='-'), '----')
        
        sh.push('pop1')
        self.assertEqual(sh(), '....')
        
        self.assertEqual(sh(-1), '...')
    
        self.assertEqual(sh.push(1).indent(), '...')

        self.assertEqual(sh.pop().indent(), '.')

        sh.a(6).push()
        sh.a(3).push()

        self.assertEqual(sh.pop('pop1').__, '....')
    
        sh['key1'] = 2
        self.assertEqual(sh(), '....')

        self.assertEqual(sh['key1'], '..')

        self.assertEqual(sh.indent(5), '.....')
    
        self.assertEqual(sh(), '..')

        self.assertEqual(str(sh), '..')
    
        self.assertEqual(int(sh), 2)


