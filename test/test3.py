# Using errors.

import logbook

log = logbook.Log('test', console = True)

def divide(i, const = 1):
  try:
    const/i
  except:
    log.error()
  else:
    log.ok()

divide(1)
divide(0)

def divide(i, const = 1):
  try:
    const/i
  except:
    log.critical()
  else:
    log.ok()

divide(0)
