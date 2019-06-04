import pypyrus_logbook as logbook


log = logbook.getlogger()

info = 'Very interesting information'
log.info(info)
log.debug(info)
log.error(info)
log.warning(info)
log.critical(info)
