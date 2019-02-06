# Limit by size of file.

import logbook
import time

log = logbook.Log('test', console=True, max_size=1024*1.5)

log.head()
for i in range(25):
  time.sleep(1)
  log.info(i)
