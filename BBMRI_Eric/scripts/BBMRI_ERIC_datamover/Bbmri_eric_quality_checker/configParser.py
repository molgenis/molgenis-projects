from Bbmri_eric_quality_checker.textfile import Textfile
import sys

class ConfigParser():
    def __init__(self):
        try:
            self.configFile = Textfile('config.txt').file
            self.config = self.parse_config()
        except FileNotFoundError:
            print('Your configfile should be called: config.txt. An example of the fileformat can be found in config_example.txt')
            sys.exit()
    def parse_config(self):
        config = {}
        for line in self.configFile:
            info = line.split('=')
            config[info[0]] = info[1].strip('\n')
        return config

if __name__ == "__main__":
    cp = ConfigParser()
    print(cp.config)