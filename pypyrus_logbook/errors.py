# Base exception.
class Error(Exception):
    pass

# When user tries to use closed logger.
class StatusException(Error):
    def __init__(self, message = None, *args, **kwargs):
        message = message or 'Operations on closed logger are not allowed.'
        super().__init__(message, *args, **kwargs)
        pass
