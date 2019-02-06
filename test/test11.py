# Direct output.

import logbook

log1 = logbook.Log('test', console = True)
log1.output('Hello world\n')

log2 = logbook.Log('test')
log2.output('Hello world\n')
