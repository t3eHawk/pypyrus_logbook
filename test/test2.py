# Declaration for console output.

import pypyrus_logbook as logbook

log = logbook.Logger('test', file=False)

info = 'Very interesting information'
log.info(info)
log.debug(info)
log.error(info)
log.warning(info)
log.critical(info)
