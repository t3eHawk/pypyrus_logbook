import pypyrus_logbook as logbook
import time

log = logbook.getlogger(file=True, extension='txt')

log.info('Hello! How you doing?')
log.file.close()
log.info('Are you still there?')
time.sleep(1)
log.file.open()
log.info('Hello again!')
