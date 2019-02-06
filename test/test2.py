# Declaration for console output.

import logbook

log = logbook.Log('test', console=True)

info = 'Very interesting information'
log.info(info)
log.debug(info)
log.error(info)
log.warning(info)
log.critical(info)
