import sys, os
from definitions import Definitions

class DiseaseCodeFixer:
    def __init__(self):
        self.fixes = {}
        self.open_fixes()

    def open_fixes(self):
        ROOT_DIR = Definitions().ROOT_DIR
        location = open(ROOT_DIR+'/icd10_fixes/icd10.txt')
        for line in location:
            if line.startswith('urn'):
                icd_codes = line.split('\t')
                self.fixes[icd_codes[0]] = icd_codes[1].strip('\n').split(',')


def main():
    DiseaseCodeFixer()


if __name__ == "__main__":
    main()