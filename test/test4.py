# Using headers.

import logbook

log = logbook.Log('test', console = True)
log.header()

log.header(test = 'Hello World!')

log.configure(headers = ['app', 'desc', 'timestamp'])
log.header('test2', test3 = 'Hello World!')
