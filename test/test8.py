# Close and open.

import pypyrus_logbook as logbook
import time

log = logbook.Logger('test', extension = 'txt')

log.info('Hello! How you doing?')
time.sleep(1)
log.close()
log.open()
log.info('Hello again!')
