# Empty forms.

import logbook

log = logbook.Log('test', console = True)

log.error()

log.configure(record = '{timestamp}|{source}|{rec_type}|{message}')
log.info('Source is unknown!')
