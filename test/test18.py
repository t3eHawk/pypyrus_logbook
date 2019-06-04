import pypyrus_logbook as logbook

log = logbook.getlogger()

log.sysinfo.add('-t', '--test', required=False, type=int)
print(log.sysinfo)
print(log.sysinfo.anons)
