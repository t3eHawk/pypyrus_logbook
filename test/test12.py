# General look of one page log.

import logbook

log = logbook.Log('test', control=True)

log.head()

for i in range(10):
  log.info('Iteration # %s with {rectype}.' % i)
  log.error('Iteration # %s with {rectype}.' % i)
  log.warning('Iteration # %s with {rectype}.' % i)
  log.critical('Iteration # %s with {rectype}.' % i)
