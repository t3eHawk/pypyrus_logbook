import pypyrus_logbook as logbook


log = logbook.getlogger()
log.head()

log.header.include(test='Hello World!')
log.head()

log.header.exclude('user')
log.head()
