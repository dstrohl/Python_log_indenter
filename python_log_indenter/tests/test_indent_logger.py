__author__ = 'dstrohl'

import unittest
import logging
from testfixtures import LogCapture
from python_log_indenter.pli import IndentedLoggerAdapter
from testfixtures import compare

class TestIndentedLogging(unittest.TestCase):
    def test_passthrough_logging(self):

        with LogCapture() as l:
            log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.')
            log.info('test info')
            log.error('test error')
            log.debug('test debug')
            log.warning('test warning')
            log.critical('test critical')

        tmp_ret = (
            ('root', 'INFO', 'test info'),
            ('root', 'ERROR', 'test error'),
            ('root', 'DEBUG', 'test debug'),
            ('root', 'WARNING', 'test warning'),
            ('root', 'CRITICAL', 'test critical'),

            )

        l.check(*tmp_ret)

    def test_basic_indented_logging(self):

        with LogCapture() as l:
            log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.')
            log.a().info('test 1').s()
            log.error('test %d', 2)
            log.a(3).debug('test 3')
            log.push().warning('test 4')
            log.a(1).critical('test 5')
            log.pop().critical('test 6')

        tmp_ret = (
            ('root', 'INFO', '.test 1'),
            ('root', 'ERROR', 'test 2'),
            ('root', 'DEBUG', '...test 3'),
            ('root', 'WARNING', '...test 4'),
            ('root', 'CRITICAL', '....test 5'),
            ('root', 'CRITICAL', '...test 6'),
            )

        l.check(*tmp_ret)

    def test_indented_logging_in_extra(self):

        # logging.basicConfig(level=logging.DEBUG,
        #                    format='%(name)-12s: %(levelname)-8s indent: %(indent_str)s : %(message)s')
        # log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.', auto_add=False)

        logging.basicConfig(level=logging.DEBUG)
        log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.')

        log.a().info('test 1')
        log.s().error('test 2')
        log.a(3).debug('test 3')
        log.push().warning('test 4')
        log.a(1).critical('test 5')
        log.pop().critical('test 6')

        with LogCapture() as l:
            logging.basicConfig(format='%(name)-12s: %(levelname)-8s %(indent_str)s%(message)s')
            log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.', auto_add=False)
            log.a().info('test 1')
            log.s().error('test 2')
            log.a(3).debug('test 3')
            log.push().warning('test 4')
            log.a(1).critical('test 5')
            log.pop().critical('test 6')

        tmp_ret = (
            (0, 1),
            (1, 0),
            (2, 3),
            (3, 3),
            (4, 4),
            (5, 3),
            )

        for t in tmp_ret:
            offset = t[0]
            indent_level = str(t[1])
            indent_str = self.make_indent_str(t[1])

            compare(l.records[offset].indent_level, indent_level)
            compare(l.records[offset].indent_str, indent_str)

    def make_indent_str(self, size, string='.'):
        tmp_ret = ''
        for i in range(size):
            tmp_ret += string

        return tmp_ret