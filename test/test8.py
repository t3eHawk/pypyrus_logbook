# Close and open.

import logbook
import time

log = logbook.Log('test', extension = 'txt')

log.info('Hello! How you doing?')
time.sleep(1)
log.close()
log.open()
log.info('Hello again!')
