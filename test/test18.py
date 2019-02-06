import logbook

log = logbook.Log('test', file=False, console=True)

from logbook.sysinfo import Sysinfo

sysinfo = Sysinfo()
print(sysinfo.args)

sysinfo.parser.add_argument('-t', '--test', required=False, type=int)
sysinfo.process()
print(sysinfo.args.test)
print(sysinfo.data.nums)
