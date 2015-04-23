Python Log Indenter Helper Class
================================

A python helper class that provides automatic indenting for logging.

* Documentation: http://python-log-indenter.readthedocs.org/en/latest/
* Source code at: https://github.com/dstrohl/Python_log_indenter

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



.. image:: https://travis-ci.org/dstrohl/Python_log_indenter.svg?branch=master
    :target: https://travis-ci.org/dstrohl/Python_log_indenter