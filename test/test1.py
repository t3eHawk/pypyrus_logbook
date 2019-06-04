import pypyrus_logbook as logbook


log = logbook.getlogger()
print(logbook.catalog)

log = logbook.getlogger(name='test', file=False)
print(logbook.catalog)
