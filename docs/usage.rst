Basic usage
===========

.. py:currentmodule:: python_log_indenter

Loading
-------

This subclasses a standard :py:class:`logging.LoggerAdapter`, so you simply wrap your standard logger object in this and
use it as normal.  The :py:class:`IndentedLoggerAdapter` has the same methods as the normal :py:class:`logging.Logger`,
so you dont have to change any existing code.

Example::

    from python_log_indenter import IndentedLoggerAdapter
    import logging

    logging.basicConfig(level=logging.DEBUG)
    log = IndentedLoggerAdapter(logging.get_logger(__name__))

You can also chance the default number of spaces used for indenting, as well as chance the character used (see
:doc:`advanced` for more information)

Changing the indent level
-------------------------

Once you have loaded the IndentedLoggerAdapter, you can change the level of the indents as you go using the .add / .sub
methods::


    >>> log.info('test1')
    >>> log.add()
    >>> log.info('test2')
    >>> log.sub()
    >>> log.info('test3')

Will result in a log looking like::

    INFO:root:test1
    INFO:root:    test2
    INFO:root:test3

You can also add or subtract multiple levels by passing an int to :py:meth:`IndentedLoggerAdapter.add`
or :py:meth:`IndentedLoggerAdapter.sub`::

    >>> log.info('test1')
    >>> log.add(3)
    >>> log.info('test2')
    >>> log.sub(2)
    >>> log.info('test3')

    # returning
    INFO:root:test1
    INFO:root:            test2
    INFO:root:    test3

In addition, the :py:meth:`IndentedLoggerAdapter.add` and :py:meth:`IndentedLoggerAdapter.sub`:: are chainable (along
with several of the other methods).  This means you can clean up your code to look like::

    >>> log.info('test1')
    >>> log.add().info('test2').sub()
    >>> log.info('test3')

Other Features
++++++++++++++

There are several other features included in this library, these are documented in the :doc:`advanced` section.  These
including:

Push/Pop:
    The ability to push or pop indent levels from a FILO queue.

Memories:
    The ability to store indent levels into a named memory location.

Formatable as fields:
    The ability to add the indent as a field to the :py:class:`logging.LogRecord` so that it can be included or not
    based on the format string and the handler.

Shortcuts:
    Shortcut methods for many of the fields for quicker usage.
