.. Python Loger Indenter and Helper documentation master file, created by
   sphinx-quickstart on Tue Apr 21 10:34:53 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Log Indenter documentation
============================================

This module helps by allowing you to indent the lines in your log entries to make it easier to read when you are dealing
with complex loops and calls (especially with debug level logging)

This subclasses a standard :py:class:`logging.LoggerAdapter` and allows you to control the indent level of your message.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   usage
   advanced
   api

This will allow you to turn logs that would normally look like this::

    root    DEBUG   Loading system
    root    DEBUG   Checking for the right record
    root    DEBUG   Checking record 1
    root    DEBUG   Checking name
    root    DEBUG   Not the right record
    root    DEBUG   Checking record 2
    root    DEBUG   checking name
    root    DEBUG   Name checks, checking phone number
    root    DEBUG   Phone number checks, VALID record!
    root    DEBUG   Returning record 2

Into something like this::

    root    DEBUG   Loading system
    root    DEBUG       Checking for the right record
    root    DEBUG           Checking record 1
    root    DEBUG               Checking name
    root    DEBUG                   Not the right record
    root    DEBUG           Checking record 2
    root    DEBUG               checking name
    root    DEBUG                   Name checks, checking phone number
    root    DEBUG               Phone number checks, VALID record!
    root    DEBUG           Returning record 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

