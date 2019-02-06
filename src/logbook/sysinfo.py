import os
import argparse

class _Data(dict):
    def __init__(self, mistake_allowed=True):
        self.mistake_allowed = mistake_allowed

    def __getattr__(self, name):
        if self.mistake_allowed:
            return self.get(name)
        else:
            return self[name]

class Sysinfo():
    def __init__(self, log):
        self.log = log
        self.parser = argparse.ArgumentParser()
        self.process()
        pass

    def __repr__(self):
        print(f'{self.data.sys} \n {self.data.exe}')
    
    def __str__(self):
        return f'{self.data.sys} \n {self.data.exe}'

    def process(self):
        """Provides access 
        to args - self.data.exe['key']
        to sys_env  - self.data.sys['key'] """

        self.data = _Data(mistake_allowed=False)
        self.data['sys'] = _Data()
        self.data['exe'] = _Data()

        for key, value in os.environ.items():
            self.data.sys[key] = value

        self.args, anons = self.parser.parse_known_args()
        for item in anons:
            try:
                key, value = item.split('=')
            except ValueError:
                msg =f"""Error parsing {item}.
                Make sure form is "key=value" """
                raise ValueError(msg)
            else:
                self.data.exe[key] = value
        pass


def test():
    c = Sysinfo('test')
    print(c)

if __name__ == '__main__':
    test()