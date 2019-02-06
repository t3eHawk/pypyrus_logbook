import os
import argparse

class Data(dict):
    def __getattr__(self, name):
        return self.__getitem__(name)

class Sysinfo():
    def __init__(self, log):
        self.log = log
        self.parser = argparse.ArgumentParser()
        self.process()
        pass

    def process(self):
        self.data = Data()
        for key, value in os.environ.items():
            self.data[key] = value
        self.args, anons = self.parser.parse_known_args()
        for item in anons:
            try:
                key, value = item.split('=')
            except ValueError:
                pass
            else:
                self.data[key] = value
        pass
