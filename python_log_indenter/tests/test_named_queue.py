__author__ = 'dstrohl'

import unittest
from python_log_indenter.pli import NamedFiloQueue


class TestFILOQUEUE(unittest.TestCase):
    def test_filo(self):
        nfq = NamedFiloQueue(empty_answer='Empty')

        self.assertEqual(nfq(), 'Empty')

        nfq.push(10).push(20).push(30)

        self.assertEqual(nfq(), 30)
        self.assertEqual(nfq.pop(), 30)
        self.assertEqual(nfq.pop(), 20)
        self.assertEqual(nfq.pop(), 10)
        self.assertEqual(nfq.pop(), 'Empty')
        self.assertEqual(nfq.pop(), 'Empty')

        nfq.push(10, 'ten').push(20, 'twenty').push(30, 'thirty')

        tmp_test = 'Pos: 2 / Name: thirty / Value: 30\nPos: 1 / Name: twenty / Value: 20\nPos: 0 / Name: ten / Value: 10'

        self.assertEqual(nfq.dump(), tmp_test)

        self.assertEqual(nfq.pop('twenty'), 20)
        self.assertEqual(len(nfq), 1)

        nfq.push(10).push(20).push(30)

        self.assertEqual(nfq.pop(2), 20)

        with self.assertRaises(KeyError):
            nfq.pop('blah')


