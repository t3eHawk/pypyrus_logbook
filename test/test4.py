# Using headers.

import pypyrus_logbook as logbook

log = logbook.Logger('test', file=False)
log.head()

log.head(test='Hello World!')

log.configure(headers=['app', 'desc', 'timestamp'])
log.head('test2', test3='Hello World!')
