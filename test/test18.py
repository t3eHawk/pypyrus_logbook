import pypyrus_logbook as logbook

log = logbook.Logger('test', file=False, console=True)

log.sysinfo.configure('-t', '--test', required=False, type=int)
print(log.sysinfo.args)
print(log.sysinfo.anons)
