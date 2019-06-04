import pypyrus_logbook as logbook
import time


log = logbook.getlogger(file=True, extension='txt')
log.info('Before configuration.')

time.sleep(1)

log.configure(directory='logs/{root.logger.start_date:%Y%m%d}',
              format='{isodate}|{rectype:<10}|{flname:<10}|{message}\n')
log.info('After configuration.')
