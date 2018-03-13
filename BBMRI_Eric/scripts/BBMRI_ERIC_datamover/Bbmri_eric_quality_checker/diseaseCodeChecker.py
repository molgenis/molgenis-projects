import re, sys, os
from Bbmri_eric_quality_checker.DiseaseCodeFixer import DiseaseCodeFixer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class DiseaseCodeChecker():
    def __init__(self):
        self.fixes = DiseaseCodeFixer().fixes
        self.valid_disease_types = []

    def parse_disease_types(self):
        for i, line in enumerate(
                open(ROOT_DIR.replace("Bbmri_eric_quality_checker", "data_model") + "/eu_bbmri_eric_disease_types.csv")):
            if i != 0:
                line = line.split(",")
                self.valid_disease_types.append(line[0][1:len(line[0])-1])

    def is_code_in_list(self, code, list):
        if code in list:
            return True
        else:
            return False

    def has_wildcard(self, code):
        pattern = r"(urn:miriam:icd:[A-Z]{1}\d{0,2})(\*)"
        if re.match(pattern, code):
            return True
        else:
            return False

    def check_code(self, code):
        log = []
        self.parse_disease_types()
        if not self.is_code_in_list(code, self.valid_disease_types):
            log.append('Diagnosis code not valid: ' + code)
            log.append('CRITICAL')
            log.append('COLLECTION DIAGNOSIS CODE NOT VALID')
            if code in self.fixes:
                return [log, self.fixes[code]]
            else:
                return [log, False]
        else:
            return [None, None]