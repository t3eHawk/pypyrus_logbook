# Direct output.

import pypyrus_logbook as logbook

log1 = logbook.Logger('test', console = True)
log1.output('Hello world\n')

log2 = logbook.Logger('test')
log2.output('Hello world\n')
