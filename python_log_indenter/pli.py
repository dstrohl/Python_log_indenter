__author__ = 'Dan Strohl'
__all__ = ['NamedFiloQueue', 'IndentedLoggerAdapter']


# from logging import LoggerAdapter
import logging


class NamedFiloQueue(object):
    """
    This class is a helper class for the IndentHelperClass.  This manages a FILO queue with named slots.
    """

    def __init__(self, empty_answer=None):
        """
        :param empty_answer: What should we return if the queue is empty?
        """
        self._queue_data = []
        self._pos_names = []
        self._empty_answer = empty_answer

    def push(self, data, name=None):
        """
        Add an item to the queue
        :param data: The data to add
        :param name: The name of the slot (optional)
        :return: This returns itself so that it can be chained.
        """
        if name is not None and not isinstance(name, str):
            raise AttributeError('name parameter must be a string')
        self._queue_data.append(data)
        self._pos_names.append(name)
        return self

    def pop(self, name=None):
        """
        Pull the top item from the queue, or the named or selected item.
        :param name: If this is a string, it will pop all items up to that item, if it is an integer, it will pop that
            many items.
        :return: The data for the last pop'ed item.
        :raises: KeyError if the name does not match one in the list.
        """
        if name is None:
            try:
                self._pos_names.pop()
                return self._queue_data.pop()
            except IndexError:
                return self._empty_answer
        else:
            if isinstance(name, str):
                if name in self._pos_names:
                    try:
                        while True:
                            tmp_ret = self._queue_data.pop()
                            if self._pos_names.pop() == name:
                                return tmp_ret
                    except IndexError:
                        return self._empty_answer
                else:
                    msg = 'Error: key {} not found in queue'.format(name)
                    raise KeyError(msg)
            elif isinstance(name, int):
                for i in range(name):
                    try:
                        tmp_ret = self._queue_data.pop()
                        self._pos_names.pop()
                    except IndexError:
                        tmp_ret = self._empty_answer
                return tmp_ret
            else:
                raise AttributeError('POP must pass a string or int')

    def reset(self):
        """
        Will clear the queue
        """
        self._queue_data = []
        self._pos_names = []
        return self

    def dump(self, format_str='Pos: {pos} / Name: {name} / Value: {value}'):
        """
        Returns the current queue in string format, normally used for troubleshooting.
        :param format_str: a string used by str.format() to format the returned content.
        :return:
        """
        tmp_ret = []
        if self._queue_data:

            for i in range(len(self), 0, -1):
                tmp_ret.append(format_str.format(
                    pos=i-1,
                    name=self._pos_names[i-1],
                    value=self._queue_data[i-1],
                ))

        else:
            tmp_ret.append('NO QUEUE DATA')
        return '\n'.join(tmp_ret)

    def __call__(self):
        if self._queue_data:
            return self._queue_data[len(self._queue_data)-1]
        else:
            return self._empty_answer

    def __len__(self):
        return len(self._queue_data)

    def __contains__(self, item):
        return item in self._pos_names


class IndentHelperMixin(object):

    def __init__(self, *args, **kwargs):
        """
        :keyword int spaces: Sets the number of spaces for each indent
        :keyword str indent_char: Sets the character or string used for each indent space.
        """

        spaces = kwargs.pop('spaces', 4)
        indent_char = kwargs.pop('indent_char', ' ')

        self._current_indent = 0
        self._indent_spaces = spaces
        self._indent_char = indent_char
        self._indent_mems = {}
        self._pop_queue = NamedFiloQueue(empty_answer=0)
        self._string_lookup = {}
        self._trouble_flag = False

        super(IndentHelperMixin, self).__init__(*args, **kwargs)

    '''
    ====================================
    indent control methods
    ====================================
    '''

    def indent_set(self, indent=0):
        """
        Sets the indent to this level

        :param int indent: the indent level
        :return: Self
        """
        self._current_indent = indent
        return self

    def add(self, indent=1):
        """
        Adds this to the indent level

        :param int indent: the number to add to the indent level
        :return: Self
        """
        self._current_indent += indent
        return self

    def sub(self, indent=1):
        """
        Subtracts this from the indent level

        :param int indent: the number to subtract from the indent level
        :return: Self
        """
        self._current_indent -= indent
        if self._current_indent < 0:
            self._current_indent = 0
        return self

    def indent_get(self):
        return self._current_indent

    @property
    def indent_level(self):
        """
        Returns the current indent level

        :rtype: int
        """
        return self._current_indent

    '''
    ====================================
    memory control methods
    ====================================
    '''

    def mem_save(self, key, indent=None):
        """
        Saves an indent to a specified memory key

        :param str key: The key / name to save to
        :param int indent: The indent to be saved, if None, this saves the current indent.
        :return: Self
        """
        if indent is not None:
            tmp_indent = indent
        else:
            tmp_indent = self._current_indent

        self._indent_mems[key] = tmp_indent

        return self

    def mem(self, key):
        """
        Sets the current indent to the memory at location "key"

        :param str key: The key / name to pull from
        :return: Self
        """
        self._current_indent = self._indent_mems[key]
        return self

    def mem_clear(self, key):
        """
        Removes (deletes) the memory location at the specified key.

        :param str key: The key / name to delete.
        :return: Self
        """
        if key in self._indent_mems:
            del self._indent_mems[key]

    '''
    ====================================
    push-pop methods
    ====================================
    '''

    def push(self, *args):
        """
        Saves an indent to the top of a FILO queue.

        This takes 0-2 arguments, if arguments are passed, the argument that is a string willl be used as the key,
        the argument that is an int will be used as the indent.  if two strings or two int's are passed, unpredictable
        results will occur.

        :argument str key: The name to save to, if no string is passed, this will add an un-named item to the queue.
        :param int indent: The indent to be saved, if None, this saves the current indent.
        :return: Self
        """

        new_indent = self._current_indent
        name = None

        if len(args) > 2:
            raise AttributeError('Only 2 arguments can be passed to PUSH')
        else:
            for arg in args:
                if isinstance(arg, str):
                    name = arg
                elif isinstance(arg, int):
                    new_indent = arg

        if new_indent is None:
            new_indent = self._current_indent

        self._pop_queue.push(new_indent, name=name)
        return self

    def pop(self, name=None):
        """
        Returns an indent to the top of a FILO queue.

        :param name: This behaives differently depending on what type of data is passed:

            int:
                If an int is passed, this will pop that many items from the top of the queue.
            str:
                If a string is passed, this will pop all items from the top of the queue until it reaches that named
                item.  if that item does not exist, it will raise a KeyError.
        :return: Self
        """
        self._current_indent = self._pop_queue.pop(name=name)
        return self

    '''
    ====================================
    support methods
    ====================================
    '''

    def debug_indent(self):
        tmp_ret = ['Indent Spaces  : ', self._indent_spaces,
                   'Current Indent : ', self._current_indent,
                   'Memories       : ', self._indent_mems,
                   'Push Queue     : \n', self._pop_queue.dump()]

        return '\n'.join(tmp_ret)

    '''
    ====================================
    printing methods
    ====================================
    '''

    def indent(self, indent=None, indent_char=None, mem=None, pop=None, indent_len=None):

        if indent_len is None:
            indent_len = self._indent_spaces
        if pop is not None:
            self.pop(pop)
        if mem is not None:
            self.mem(mem)
        if indent_char is None:
            indent_char = self._indent_char

        if indent is None:
            indent = self._current_indent

        ind = indent_len * indent
        tmp_ret = ''
        for i in range(ind):
            tmp_ret += indent_char

        return tmp_ret

    def indent_str(self):
        return self.indent()

    '''
    ====================================
    magic methods
    ====================================
    '''

    def __call__(self, indent=None):
        if indent is not None:
            if isinstance(indent, int):
                self.add(indent)

            elif isinstance(indent, str):
                if indent in self._indent_mems:
                    j = self[indent]

                elif indent in self._pop_queue:
                    self.pop(indent)

        return self.indent()

    def __iadd__(self, other):
        self._current_indent += other
        return self

    def __isub__(self, other):
        self._current_indent -= other
        return self

    def __len__(self):
        return self._current_indent

    def __getitem__(self, item):
        self.mem(item)
        return self.indent()

    def __setitem__(self, key, value):
        self.mem_save(key, value)

    def __delitem__(self, key):
        self.mem_clear(key)

    def __int__(self):
        return self._current_indent

    '''
    ====================================
    Shortcuts
    ====================================
    '''

    @property
    def __(self):
        return self.indent()

    def i(self, indent=0):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.indent_set`
        """
        return self.indent_set(indent)

    def a(self, indent=1):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.add`
        """
        return self.add(indent)

    def s(self, indent=1):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.sub`
        """
        return self.sub(indent)

    def ms(self, key=None, indent=None):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.mem_save`
        """
        return self.mem_save(key, indent)

    def m(self, key=None):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.mem`
        """
        return self.mem(key)

    def mc(self, key=None):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.mem_clear`
        """
        return self.mem_clear(key)

    def po(self, name=None):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.pop`
        """
        return self.pop(name)

    def pu(self, *args):
        """
        Shortcut method for :py:meth:`IndentedLoggerAdapter.push`
        """
        return self.push(*args)


class IndentHelper(IndentHelperMixin):

    def __init__(self, *args, **kwargs):
        super(IndentHelper, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.indent()

    def __repr__(self):
        tmp_ret = 'SpaceHelper, level {} indent'.format(self._current_indent)
        return tmp_ret


class IndentedLoggerAdapter(IndentHelperMixin, logging.LoggerAdapter):
    """

    """

    def __init__(self, logger, extra=None, auto_add=True, **kwargs):
        """
        Overrides the init and parameters from :py:class:`logging.Logger`, however adds it adds some functions.

        :param bool auto_add: this controls how the indent is handled, if this is True (default) the indent is automatically
            added to the beginning of the message before it is passed to the logging engine.  If False, the indent is
            passed as part of the :py:class:`logging.LogRecord` as the parameter .indent_str.  this allows access to
            the indent by custom formatting commands if needed.

        :param int spaces: Sets the number of spaces for each indent
        :param str indent_char: Sets the character or string used for each indent space.

        The other thing that this adds is the ability to chain some of the key methods so that it can be combined in
        single lines of code.  the methods that have been modified are:

        * :py:meth:`IndentedLoggerAdapter.debug`
        * :py:meth:`IndentedLoggerAdapter.info`
        * :py:meth:`IndentedLoggerAdapter.warning`
        * :py:meth:`IndentedLoggerAdapter.error`
        * :py:meth:`IndentedLoggerAdapter.critical`
        * :py:meth:`IndentedLoggerAdapter.exception`
        * :py:meth:`IndentedLoggerAdapter.log`
        """
        super(IndentedLoggerAdapter, self).__init__(logger, extra or {}, **kwargs)
        self._current_level = None
        self._auto_add = auto_add

    def process(self, msg, kwargs):
        if self._auto_add:
            msg = str(self.__)+msg
        else:
            if 'extra' not in kwargs:
                kwargs['extra'] = {}

            kwargs['extra']['indent_level'] = str(self.indent_level)
            kwargs['extra']['indent_str'] = str(self.__)

        return msg, kwargs

    def debug(self, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).debug(msg, *args, **kwargs)
        return self

    def info(self, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).info(msg, *args, **kwargs)
        return self

    def warning(self, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).warning(msg, *args, **kwargs)
        return self

    def error(self, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).error(msg, *args, **kwargs)
        return self

    def exception(self, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).exception(msg, *args, **kwargs)
        return self

    def critical(self, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).critical(msg, *args, **kwargs)
        return self

    def log(self, level, msg, *args, **kwargs):
        super(IndentedLoggerAdapter, self).log(level, msg, *args, **kwargs)
        return self
