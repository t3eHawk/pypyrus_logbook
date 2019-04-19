from .utils import py_file
from .logger import Logger as _Logger_
from .output import Output
from .record import Record
from .header import Header
from .formatter import Formatter

__author__ = 'Timur Faradzhov'
__copyright__ = 'Copyright 2019, The Pypyrus Logbook Project'
__credits__ = ['Timur Faradzhov']

__license__ = 'MIT'
__version__ = '0.0.2'
__maintainer__ = 'Timur Faradzhov'
__email__ = 'timurfaradzhov@gmail.com'
__status__ = 'Production'

__doc__ = 'Lightweight module for work with tables in Python.'

catalog = {}

def Logger(app=None, **kwargs):
    app = app or py_file
    logger = catalog.get(app)
    if logger is not None:
        logger.configure(**kwargs)
    else:
        logger = _Logger_(app=app, **kwargs)
    return logger

applogger = Logger(file=False, console=True, debug=True)

def info(*args, **kwargs):
    applogger.info(*args, **kwargs)
    pass

def debug(*args, **kwargs):
    applogger.debug(*args, **kwargs)
    pass

def warning(*args, **kwargs):
    applogger.warning(*args, **kwargs)
    pass

def error(*args, **kwargs):
    applogger.error(*args, **kwargs)
    pass

def critical(*args, **kwargs):
    applogger.critical(*args, **kwargs)
    pass

def configure(*args, **kwargs):
    applogger.configure(*args, **kwargs)
    pass
