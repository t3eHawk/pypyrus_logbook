import pypyrus_logbook as logbook
import time

log = logbook.getlogger(file=True, extension='txt')
log.info('Hello there!')

time.sleep(1)
log.info('Logger going to be restatered now')
log.restart()

log.head()
time.sleep(1)
log.info('This logger has a header and the next should also have')
log.restart()

log.info(f'This logger started at {log.start_date}')
time.sleep(1)
log.restart()
log.info(f'And this logger started at {log.start_date}')
