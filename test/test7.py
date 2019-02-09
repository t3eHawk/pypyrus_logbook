# Reopen.

import pypyrus_logbook as logbook
import time

log = logbook.Log('test')
log.header(test = 'Hello World!')
log.info('Before reopen.')
time.sleep(1)
log.reopen()
log.info('After reopen.')
