import os
import sys
import time
import platform
import traceback
import datetime as dt
import pypyrus_logbook as logbook

from .output import Root
from .header import Header
from .record import Record
from .sysinfo import Sysinfo
from .formatter import Formatter

class Logger():
    """Main API for using and managing the logs."""
    def __init__(
        self, app=None, desc=None, version=None, status=True, console=True,
        file=True, email=False, html=False, table=False, directory=None,
        filename=None, extension=None, smtp=None, db=None, format=None,
        info=True, debug=False, warning=True, error=True, critical=True,
        alarming=True, control=True, maxsize=(1024*1024*10), maxdays=1,
        maxlevel=2, maxerrors=False
    ):
        # Attributes describing the application.
        self._app = app
        self._desc = desc
        self._version = version

        # Some logger important attributes
        self._start_timestamp = dt.datetime.now()
        self.rectypes = {
            'none': 'NONE', 'info': 'INFO', 'debug': 'DEBUG',
            'warning': 'WARNING', 'error': 'ERROR', 'critical': 'CRITICAL'}
        self.messages = {
            'ok': 'OK', 'success': 'SUCCESS', 'fail': 'FAIL'}
        self._with_error = False
        self._count_errors = 0

        # Complete the initial configuration.
        self.configure(
            status=status, console=console, file=file, email=email, html=html,
            table=table, directory=directory, filename=filename,
            extension=extension, smtp=smtp, db=db, format=format, info=info,
            debug=debug, warning=warning, error=error, critical=critical,
            alarming=alarming, control=control, maxsize=maxsize,
            maxdays=maxdays, maxlevel=maxlevel, maxerrors=maxerrors)

        # Output shortcuts.
        self.console = self.root.console
        self.file = self.root.file
        self.email = self.root.email
        self.html = self.root.html
        self.table = self.root.table

        logbook.catalog[self.app] = self
        pass

    def __str__(self):
        return f'<Logger object "{self._app}">'

    __repr__ = __str__

    def configure(
        self, status=None, console=None, file=None, email=None, html=None,
        table=None, directory=None, filename=None, extension=None, smtp=None,
        db=None, format=None, info=None, debug=None, warning=None, error=None,
        critical=None, alarming=None, control=None, maxsize=None, maxdays=None,
        maxlevel=None, maxerrors=None
    ):
        """Main method to configure the logger and all its elements."""
        if hasattr(self, 'root') is False:
            self.root = Root(
                self, console=console, file=file, email=email, html=html,
                table=table, status=status, directory=directory,
                filename=filename, extension=extension, smtp=smtp, db=db)
        else:
            for key, value in {
                'console': console, 'file': file,
                'email': email, 'html': html, 'db': db
            }.items():
                if value is True:
                    getattr(self.root, key).open()
                elif value is False:
                    getattr(self.root, key).close()

            path = {}
            if directory is not None: path['dir'] = directory
            if filename is not None: path['name'] = filename
            if extension is not None: path['ext'] = extension
            if len(path) > 0:
                self.root.file.configure(**path)

            if isinstance(smtp, dict) is True:
                self.root.email.configure(**smtp)

            if isinstance(db, dict) is True:
                self.root.table.configure(**db)

        if isinstance(format, str) is True:
            format = {'record': format}

        if hasattr(self, 'formatter') is False:
            format = {} if isinstance(format, dict) is False else format
            self.formatter = Formatter(**format)
        elif isinstance(format, dict) is True:
            self.formatter.configure(**format)

        if hasattr(self, 'filters') is False:
            self.filters = {}
        for key, value in {
            'info': info, 'debug': debug, 'error': error,
            'warning': warning, 'critical': critical
        }.items():
            if isinstance(value, bool) is True:
                self.filters[key] = value

        if isinstance(maxsize, (int, float, bool)) is True:
            self._maxsize = maxsize
        if isinstance(maxdays, (int, float, bool)) is True:
            self._maxdays = maxdays
            self._calculate_timestamps()
        if isinstance(maxlevel, (int, float, bool)) is True:
            self._maxlevel = maxlevel
        if isinstance(maxerrors, (int, float, bool)) is True:
            self._maxerrors = maxerrors
        if isinstance(alarming, bool) is True:
            self._alarming = alarming
        if isinstance(control, bool) is True:
            self._control = control

        if hasattr(self, 'sysinfo') is False:
            self.sysinfo = Sysinfo(self)

        if hasattr(self, 'header') is False:
            self.header = Header(self)
        pass

    def write(self, record):
        """Direct write to the output."""
        self._check()
        self.root.write(record)
        pass

    def record(self, rectype, message, error=False, **kwargs):
        """Basic method and an interface for recording.
        By default it writes the records with the type NONE.
        That can be changed but depends on available record types.
        Local forms can be passed through the kwargs.
        They will have higher priority than forms from global config.
        """
        if self.filters.get(rectype, True) is True:
            record = Record(self, rectype, message, error=error, **kwargs)
            self.write(record)
        pass

    def info(self, message, **kwargs):
        """Record an info message."""
        rectype = 'info'
        self.record(rectype, message, **kwargs)
        pass

    def debug(self, message, **kwargs):
        """Record a message containing debug information."""
        rectype = 'debug'
        self.record(rectype, message, **kwargs)
        pass

    def error(
        self, message=None, rectype='error', format=None, alarming=None,
        level=1, **kwargs
    ):
        """Record an error message.
        If the exception was found then transform it to the forms.
        Send alarm notification if email is configurated.
        Abort the application in case of high level error.
        """
        self._with_error = True
        self._count_errors += 1

        format = self.formatter.error if format is None else format
        alarming = self._alarming if alarming is None else alarming

        # Parse the error.
        err_type, err_value, err_tb = sys.exc_info()
        if err_type is not None:
            if isinstance(format, str) is True:
                err_name = err_type.__name__
                err_value = err_value

                for tb in traceback.walk_tb(err_tb):
                    f_code = tb[0].f_code

                    err_file = os.path.abspath(f_code.co_filename)
                    err_line = tb[1]
                    err_obj = f_code.co_name

                    self.record(
                        rectype, message, error=True,
                        err_name=err_name, err_value=err_value,
                        err_file=err_file, err_line=err_line,
                        err_obj=err_obj, **kwargs)
            elif format is False:
                exception = traceback.format_exception(
                    err_type, err_value, err_tb)
                message = '\n'
                message += ''.join(exception)
                self.record(rectype, message, **kwargs)
        else:
            message = message or ''
            self.record(rectype, message, **kwargs)

        # Inform about the error.
        if alarming is True:
            self.root.email.alarm()

        # Break execution in case of critical error if permitted.
        if self._control is True:
            if level >= self._maxlevel:
                sys.exit()
            if self._maxerrors is not False:
                if self._count_errors > self._maxerrors:
                    sys.exit()
        pass

    def warning(self, message=None, **kwargs):
        """Shortcut for warning (level = 0)."""
        self.error(message, rectype='warning', level=0, **kwargs)
        pass

    def critical(self, message=None, **kwargs):
        """Shortcut for critical error (level = 2)."""
        self.error(message, rectype='critical', level=2, **kwargs)
        pass

    def head(self):
        """Generate header and record it to the output."""
        string = self.header.create()
        self.write(string)
        pass

    def subhead(self, string):
        """Generate subhead as upper-case text between two border lines and
        record it to the output.
        """
        string = f'\t{string}\n'.upper()
        self.bound()
        self.write(string)
        self.bound()
        pass

    def bound(self, div=None, length=None):
        """Draw horizontal border. Useful when need to separate different
        logger blocks.
        """
        border = self.formatter.div * self.formatter.length
        self.write(border + '\n')
        pass

    def blank(self, number=1):
        """Write blank lines."""
        string = '\n'*number
        self.write(string)

    def ok(self, **kwargs):
        """Record an ok message."""
        rectype = 'info'
        message = self.messages['ok']
        self.record(rectype, message, **kwargs)
        pass

    def success(self, **kwargs):
        """Record a success message."""
        rectype = 'info'
        message = self.messages['success']
        self.record(rectype, message, **kwargs)
        pass

    def fail(self, **kwargs):
        """Record a fail message."""
        rectype = 'info'
        message = self.messages['fail']
        self.record(rectype, message, **kwargs)
        pass

    def restart(self):
        """Open new output file to continue the logging."""
        self._start_timestamp = dt.datetime.now()
        self._calculate_timestamps()
        self.sysinfo.process()
        if self.root.file.status is True:
            self.root.file.new()
        if self.header.used is True:
            self.header.refresh()
            self.head()
        pass

    def send(self, *args, **kwargs):
        """Send email message."""
        self.root.email.send(*args, **kwargs)
        pass

    def set(self, **kwargs):
        """Set values in table."""
        self.root.table.write(**kwargs)
        pass

    def _calculate_timestamps(self):
        self.__restart_timestamp = (
            self._start_timestamp
            + dt.timedelta(days=self._maxdays))
        pass

    def _check(self):
        """Check the output file statistics to catch when current file must be
        closed and new one must be opened.
        """
        if self.root.file.status is True:
            if self._maxsize is not False:
                if self.root.file.size is not None:
                    if self.root.file.size > self._maxsize:
                        self.restart()
                        return
            if self._maxdays is not False:
                if self.__restart_timestamp.day == dt.datetime.now().day:
                    self.restart()
                    return

    @property
    def app(self):
        return self._app

    @property
    def desc(self):
        return self._desc

    @property
    def version(self):
        return self._version

    @property
    def start_timestamp(self):
        return self._start_timestamp

    @property
    def with_error(self):
        return self._with_error

    @property
    def count_errors(self):
        return self._count_errors
