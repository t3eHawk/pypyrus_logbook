import pypyrus_logbook as logbook

log = logbook.Log('test', file=False, console=True)

log.sysinfo.configure('-t', '--test', required=False, type=int)
print(sysinfo)
