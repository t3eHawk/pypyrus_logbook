# Reset.

import pypyrus_logbook as logbook
import time

log = logbook.Logger('test', extension = 'txt')
log.info('Before reset.')
time.sleep(1)
log.reset()
log.info('After reset.')
