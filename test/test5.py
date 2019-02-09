# Configuration.

import pypyrus_logbook as logbook
import time

log = logbook.Log('test', extension = 'txt')
log.info('Before configuration.')

time.sleep(1)

log.configure(
  folder = 'logs/test/%Y%m%d',
  record = '%Y/%m/%d %H:%M:%S|{rec_type:<10}|{source:<10}|{message}\n',
  source = 'LOG',
)
log.info('After configuration.')
log.info('With another source.', source = 'USER')
