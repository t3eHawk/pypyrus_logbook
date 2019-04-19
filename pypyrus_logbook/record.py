import os
import sys
import datetime as dt

class Record():
    """This class describes the record. Record is an instance that is going
    to be logged as separated line or set of lines in the logger.
    """
    def __init__(
        self, logger, rectype, message, error=False,
        format=None, error_format=None, **kwargs
    ):
        self.logger = logger
        frame = self.__catch_frame()
        f_code = frame.f_code
        flname = f_code.co_filename
        objname = f_code.co_name

        self.__format = format or logger.formatter.record

        self.datetime = dt.datetime.now()
        self.isotime = self.datetime.isoformat(sep=' ', timespec='seconds')

        self.flname = os.path.splitext(os.path.basename(flname))[0]
        self.objname = objname if objname != '<module>' else 'main'
        self.rectype = logger.rectypes[rectype]

        self.div = logger.formatter.div

        message = str(message if error is False else logger.formatter.error)
        self.message = message.format(**self.__dict__, **kwargs)
        pass

    def __str__(self):
        return self.create()

    __repr__ = __str__

    def create(self, css=False):
        string = self.__format.format(**self.__dict__)
        return string

    def __catch_frame(self):
        """Catch frame from file where methods of module was called."""
        frame = sys._getframe()
        module_dir = os.path.dirname(__file__)
        while True:
            if module_dir != os.path.dirname(frame.f_code.co_filename):
                return frame
            else:
                frame = frame.f_back
