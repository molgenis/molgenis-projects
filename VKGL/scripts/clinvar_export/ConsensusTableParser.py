from MolgenisConfigParser import MolgenisConfigParser
from ProgressBar import ProgressBar
from ClinvarExportGenerator import ClinvarExportGenerator
import molgenis
import math
import json


class ConsensusTableParser:
    """ConsensusTableParser gets the variants from the consensus table,
    retrieves the lab information of the variants with consensus and only one omim disease code,
    output is written for each lab """
    def __init__(self, raw_file="raw.json", use_raw=False, export=True):
        self.config = MolgenisConfigParser("config.txt").config
        labs = self.config['labs'].split(',')
        self.labClassifications = dict((lab, []) for lab in labs)
        if use_raw:
            self.raw_file = open(raw_file)
            print("Reading from server skipped, reading from previously generated {}".format(raw_file))
            self.parse_raw()
        else:
            self.raw_file = open(raw_file, "w")
            self.session = molgenis.Session(self.config['url'])
            self.session.login(self.config['account'], self.config['password'])
            self.get_paginated_table_content()
            self.session.logout()
            self.save_raw_output()
        if export:
            self.write_output()

    def parse_table_content_page(self, page):
        """NAME: parse_table_content_page
        INPUT: page (the items on the page returned by the REST API)
        PURPOSE: Here we get the first batch of items from the molgenis API and process its rows.
        Item passes and is saved when there is one omim disease code and the consensus classification is equal to
        (Likely) benign(x), (Likely) pathogenic(x), VUS(x)"""
        for row in page:
            omim_length = len(row['disease'])
            consensus_classification = row['consensus_classification']
            if omim_length == 1 and (consensus_classification.startswith('(Likely)') or consensus_classification.startswith('VUS')):
                for lab in dict.keys(self.labClassifications):
                    if lab.lower() in row:
                        omim = row['disease'][0]['mim_number']
                        lab_id = row[lab +'_classification']['id']
                        self.save_lab_info(lab_id, lab, omim)

    def save_lab_info(self, lab_id, lab, omim):
        """NAME: save_lab_info
        INPUT:  lab_id (the id of the variant in this specific lab)
                lab (the name of the lab e.g. UMCG)
                omim (the omim number of the variant)
        PURPOSE: get the variant information in the lab table, add omim number, delete unnecessary components,
        and save it"""
        labTable = 'VKGL_' + lab
        variant = self.session.getById(labTable, lab_id)
        variant['omim'] = omim
        del variant['_meta']
        del variant['_href']
        del variant['comments']
        self.labClassifications[lab].append(variant)

    def get_paginated_table_content(self):
        """NAME: get_paginated_table_content
        PURPOSE:  This function will retrieve the items in the consensus table per 10.000, for each page,
        we call parse_table_content_page"""
        total = self.session.get_total("VKGL_consensus")
        num = 10000
        times = math.ceil(total/num)
        print("Processing data:\n")
        progress = ProgressBar(total)
        progress.get_next(0)
        for iter in range(times):
            start = ((iter+1)*num) - num
            consensusItems = self.session.get('VKGL_consensus', num=num, start=start)
            self.parse_table_content_page(consensusItems)
            progress.get_next(start + num)
        progress.get_next(total)
        print(progress.get_done_message('min'))

    def save_raw_output(self):
        """NAME: save_raw_output
        PURPOSE: Write output of processing step to file so we don't have to redo it after the run fails for writing to
        excel."""
        self.raw_file.write(json.dumps(self.labClassifications))
        self.raw_file.close()

    def parse_raw(self):
        """NAME: parse_raw
        PURPOSE: Parses the raw file generated during a previous round."""
        with self.raw_file as file:
            file_content = file.read()
            input = json.loads(file_content)
            self.labClassifications = input

    def write_output(self):
        """NAME: write_output
        PURPOSE: write an excel file for each lab in the clinvar template format"""
        print("Writing output files: ")
        for i, lab in enumerate(self.labClassifications):
            ClinvarExportGenerator(self.labClassifications[lab], lab)



def main():
    # Export from raw
    # ConsensusTableParser(True, True)
    # Produce a raw without export
    # ConsensusTableParser(use_raw=False, export=True, raw_file="raw.json")
    # Run defaults
    ConsensusTableParser()


if __name__ == '__main__':
    main()
