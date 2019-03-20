from .logger import Logger
from .header import Header
from .output import Output
from .record import Record
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

main = Logger(file=False, console=True, debug=True)

def info(*args, **kwargs):
    main.info(*args, **kwargs)
    pass

def debug(*args, **kwargs):
    main.debug(*args, **kwargs)
    pass

def warning(*args, **kwargs):
    main.warning(*args, **kwargs)
    pass

def error(*args, **kwargs):
    main.error(*args, **kwargs)
    pass

def critical(*args, **kwargs):
    main.critical(*args, **kwargs)
    pass

def configure(*args, **kwargs):
    main.configure(*args, **kwargs)
    pass
