import pypyrus_logbook as logbook

log = logbook.getlogger()
log.write('Doing...')
log.write('done')
log.blank()

log.line('In progress...')
log.line('Still in progress...')
log.write('Finished')
