# Reset.

import logbook
import time

log = logbook.Log('test', extension = 'txt')
log.info('Before reset.')
time.sleep(1)
log.reset()
log.info('After reset.')
