import pypyrus_logbook as logbook


log = logbook.getlogger(control=False)

log.head()

for i in range(10):
  log.info('Iteration # %s with {rectype}.' % i)
  log.error('Iteration # %s with {rectype}.' % i)
  log.warning('Iteration # %s with {rectype}.' % i)
  log.critical('Iteration # %s with {rectype}.' % i)
