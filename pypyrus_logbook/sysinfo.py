import os
import pip
import sys
import json
import socket
import argparse
import platform
import datetime as dt

userprms = os.path.abspath(os.path.expanduser('~/.pypyrus/prms.json'))

class Data(dict):
    def __getattr__(self, name):
        return self.get(name)

class Sysinfo():
    def __init__(self, logger):
        self.logger = logger
        self.parser = argparse.ArgumentParser()
        self.process(env=True, prms=True)
        pass

    def __str__(self):
        all = [
            f'[Environment variables: {self.env}]',
            f'[Execution variables: {self.prms}]',
            f'[Execution arguments: {self.args.__dict__}]',
            f'[Statistic variables: {self.stat}]']
        return ', '.join(all)

    __repr__ = __str__

    def process(self, env=False, prms=False, args=True, anons=True, stat=True):
        if env is True:
            self.env = Data()
            for key, value in os.environ.items():
                self.env[key.lower()] = value


        if prms is True or args is True or anons is True:
            knowns, unknowns = self.parser.parse_known_args()
            if args is True:
                self.args = knowns
            if prms is True:
                self.prms = Data()
                with open(userprms, 'r') as fh:
                    for item in json.load(fh):
                        if isinstance(item, dict) is True:
                            name = item.get('name')
                            value = item.get('value')
                            if isinstance(name, str) is True:
                                self.prms[name] = value
            if anons is True:
                self.anons = []
            for item in unknowns:
                try:
                    key, value = item.split('=')
                except ValueError:
                    if anons is True:
                        self.anons.append(item)
                else:
                    if prms is True:
                        self.prms[key.lower()] = value

        if stat is True:
            self.stat = Data()
            stat = {
                'app': self.logger.app,
                'desc': self.logger.desc,
                'version': self.logger.version,
                'hostname': platform.node(),
                'ip': socket.gethostbyname(socket.gethostname()),
                'user': os.getlogin(),
                'pid': os.getpid(),
                'system': platform.platform(),
                'python':
                    f'{platform.python_version()}-{platform.architecture()[0]}',
                'pyexe': sys.executable,
                'script': os.path.abspath(sys.argv[0]),
                'compiler': platform.python_compiler(),
                'pip': pip.__version__,
                'loctime':
                    dt.datetime.now().isoformat(sep=' ', timespec='seconds')}
            self.stat.update(stat)
        pass

    def configure(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        self.process(args=True, stat=False)
        pass
