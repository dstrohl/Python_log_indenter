Advanced usage
==============

.. py:currentmodule:: python_log_indenter

the py:class:`IndentedLoggerAdapter` has several other methods and usages for advanced usage.

Push / Pop
----------
:py:meth:`IndentedLoggerAdapter.push` and :py:meth:`IndentedLoggerAdapter.pop` allow you to add an indent level to a
first in last out queue (FILO so that you can save an indent level and go back to it, even if you dont remember what it
was.

Example::

    >>> log.info('test1').push().add()
    >>> log.info('test2')
    >>> log.add().info('test3')
    >>> log.pop().info('test4')

    # returning

    INFO:root:test1
    INFO:root:    test2
    INFO:root:        test3
    INFO:root:test4

This can be helpfull if you are changing indents across methods or functions::

    def test1():
    log.info('entering test function').add()

    # do something ...

    log.push()  # save the location
    log.add().debug('entering the loop')
    for i in range(3):
        sub_test(i)

    log.pop()    # getting the saved location
    log.debug('leaving function')

    def sub_test(cnt):
        log.debug('sub_test_loop %d', cnt)

        # do some loopy thing ...
        log.a().debug('doing loopy stuff').s()

    # returns

    INFO:root:entering test function
    DEBUG:root:    entering the loop
    DEBUG:root:        sub_test_loop 0
    DEBUG:root:            doing loopy stuff
    DEBUG:root:        sub_test_loop 1
    DEBUG:root:            doing loopy stuff
    DEBUG:root:        sub_test_loop 2
    DEBUG:root:            doing loopy stuff
    DEBUG:root:    leaving the function

Especially if you forget to return to the same level as before.  For example, if we run the above test1() function three
times we would see::

    INFO:root:entering test function
    DEBUG:root:    entering the loop
    DEBUG:root:        sub_test_loop 0
    DEBUG:root:            doing loopy stuff
    DEBUG:root:        sub_test_loop 1
    DEBUG:root:            doing loopy stuff
    DEBUG:root:        sub_test_loop 2
    DEBUG:root:            doing loopy stuff
    DEBUG:root:    leaving the function
    INFO:root:    entering test function
    DEBUG:root:        entering the loop
    DEBUG:root:            sub_test_loop 0
    DEBUG:root:                doing loopy stuff
    DEBUG:root:            sub_test_loop 1
    DEBUG:root:                doing loopy stuff
    DEBUG:root:            sub_test_loop 2
    DEBUG:root:                doing loopy stuff
    DEBUG:root:        leaving the function
    INFO:root:        entering test function
    DEBUG:root:            entering the loop
    DEBUG:root:                sub_test_loop 0
    DEBUG:root:                    doing loopy stuff
    DEBUG:root:                sub_test_loop 1
    DEBUG:root:                    doing loopy stuff
    DEBUG:root:                sub_test_loop 2
    DEBUG:root:                    doing loopy stuff
    DEBUG:root:            leaving the function

if we had used :py:meth:`IndentedLoggerAdapter.push` and :py:meth:`IndentedLoggerAdapter.pop` at the beginning and end
of the method, we would have cleared out the building indent.

Push / Pop by name
++++++++++++++++++

You can also push and pop by name, this allows you to set a name while pushing an indent level, then return to that
point in the queue without having to do multiple pop's.

For example::

    def test1():
    log.push('test1_function')
    log.info('entering test function').add()

    # do something ...

    log.add().debug('entering the loop')
    log.push()
    for i in range(3):
        sub_test(i)

    log.debug('leaving function')

    # This pops TWO levels from the queue, the first one (Just above the "for / in") and returns to the first .push()
    log.pop('test1_function')

    def sub_test(cnt):
        log.debug('sub_test_loop %d', cnt)

        # do some loopy thing ...
        log.a().debug('doing loopy stuff').s()

    # returns

    INFO:root:entering test function
    DEBUG:root:    entering the loop
    DEBUG:root:        sub_test_loop 0
    DEBUG:root:            doing loopy stuff
    DEBUG:root:        sub_test_loop 1
    DEBUG:root:            doing loopy stuff
    DEBUG:root:        sub_test_loop 2
    DEBUG:root:            doing loopy stuff
    DEBUG:root:    leaving the function

In addition, you can pass the indent level to the .push() (without changing the current level), and you can pass the
number of levels to go back to the .pop()::

    >>> log.info('test1').push(2).add()
    >>> log.info('test2')
    >>> log.add().info('test3').push()
    >>> log.info('test4')
    >>> log.pop().info('test5')

    # returning

    INFO:root:test1
    INFO:root:        test2
    INFO:root:            test3
    INFO:root:            test4
    INFO:root:test4

Memories
--------

:py:meth:`IndentedLoggerAdapter.mem_save`, :py:meth:`IndentedLoggerAdapter.mem`, and
:py:meth:`IndentedLoggerAdapter.mem_clear` You also can store indent levels using named storage locations, this allows
you to setup indent levels for specific things and recall them as needed.::

    >>> log.mem_save('level1',1)
    >>> log.mem_save('level2',2)
    >>> log.mem_save('level3',3)
    >>> log.info('test0')
    >>> log.mem('level1').info('test1')
    >>> log.info('test2')
    >>> log.mem('level2').info('test3')
    >>> log.mem('level3').info('test4')
    >>> log.mem('level1').info('test5')

    # returning

    INFO:root:test0
    INFO:root:    test1
    INFO:root:    test2
    INFO:root:        test3
    INFO:root:            test4
    INFO:root:test5

If you do not pass an indent level to .mem_save() it will save the current level.

Formatting
----------
By default the library will add the indent to the beginning of the message string, however if you want more control
over the formatting of the log string, you can change the behaivior to set the indent_str as a
:py:class:`logging.LogRecord` property, which can then be access by format strings set in the logging configuration.

This allows you to use the indenting for console logging, but not for log files (or any other mix you want).  In
addition, the indent_level is available as well if you want to pass that into the formatting string.

These are available using the "indent_str" and "indent_level" keywords in the formatting string.

As an example of a useless format::

    logging.basicConfig(format='%(name)-8s: %(levelname)-8s : level %(indent_level) : indent <%(indent_str)s> : %(message)s')
    log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.', auto_add=False)

    log.info('test1')
    log.add(3)
    log.info('test2')
    log.sub(2)
    log.info('test3')

    # returning
    root    : INFO     : level 0 : indent <> : test 1
    root    : INFO     : level 3 : indent <            > : test 1
    root    : INFO     : level 1 : indent <    > : test 1

for better examples, see the logging cookbook on the :py:mod:`logging`

Shortcuts
---------
Shortcut methods have also been defined to assist in making these faster to enter (not that the names are very long to
begin with).

+-----------------+----------+
| Method          | Shortcut |
+=================+==========+
| .indent_level() | .i()     |
+-----------------+----------+
| .add()          | .a()     |
+-----------------+----------+
| .sub()          | .s()     |
+-----------------+----------+
| .pop()          | .po()    |
+-----------------+----------+
| .push()         | .pu()    |
+-----------------+----------+
| .mem()          | .m()     |
+-----------------+----------+
| .mem_save()     | .ms()    |
+-----------------+----------+
| .mem_clear()    | .mc()    |
+-----------------+----------+

Also, you can access memory location using dictionary methods, for example::

    >>> log['level1'] = 1
    >>> log['level2'] = 2
    >>> log['level3'] = 3
    >>> log.info('test0')
    >>> log['level1'].info('test1')
    >>> log.info('test2')
    >>> log['level2'].info('test3')
    >>> log['level3'].info('test4')
    >>> log['level1'].info('test5')

    # returning

    INFO:root:test0
    INFO:root:    test1
    INFO:root:    test2
    INFO:root:        test3
    INFO:root:            test4
    INFO:root:test5

Changing indent size and indent character
-----------------------------------------

When loading the :py:class:`IndentedLoggerAdapter` you can choose to set the size of the indent and the character used
to create the indent.

For example::

    logging.basicConfig(level=logging.DEBUG)
    log = IndentedLoggerAdapter(logging.getLogger(), spaces=1, indent_char='.')

    log.a().info('test 1')
    log.s().error('test 2')
    log.a(3).debug('test 3')
    log.push().warning('test 4')
    log.a(1).critical('test 5')
    log.pop().critical('test 6')

    INFO:root:.test 1
    ERROR:root:test 2
    DEBUG:root:...test 3
    WARNING:root:...test 4
    CRITICAL:root:....test 5
    CRITICAL:root:...test 6

See the :doc:`api` section for information on the api for specific parameters.