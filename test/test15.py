import pypyrus_logbook as logbook

log = logbook.Log('test', console=True)

for i in range(10):
    log.info(f'The record number {i}')
