Installation and initial setup
==============================

To install the indented log helper, first get it using :py:mod:`pip`::

    pip install python_log_indenter


Since this is, in effect, a logging adapter, you simply wrap your logger in the IndentedLoggerAdapter class::

    from python_log_indenter import IndentedLoggerAdapter
    import logging

    log = IndentedLoggerAdapter(logging.get_logger(__name__))

You can now use it as you would any other log::

    log.debug('this is a debug log entry')

see the :doc:`usage` page for examples of how to use this.