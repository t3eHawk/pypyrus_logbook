import pypyrus_logbook as logbook

log1 = logbook.getlogger()
print(id(log1))
log2 = logbook.getlogger()
print(id(log2))
log3 = logbook.getlogger('testy')
print(id(log3))
print(log3.file.status)
log3.info('hi')
print(type(log3))
