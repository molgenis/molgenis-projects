class MolgenisConfigParser():
    def __init__(self, file):
        self.config = self.parse(open(file))

    def parse(self, file):
        config = {}
        for line in file.readlines():
            values = line.split('=')
            config[values[0]] = values[1].replace('\n', '')
        return config