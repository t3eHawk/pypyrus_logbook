import pypyrus_logbook as logbook


log = logbook.getlogger()

for i in range(10):
    log.info(f'The record number {i}')
