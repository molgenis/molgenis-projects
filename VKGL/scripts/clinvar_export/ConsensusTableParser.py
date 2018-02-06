from MolgenisConfigParser import MolgenisConfigParser
import time
import molgenis, pprint, math

class ConsensusTableParser:
    def __init__(self):
        self.config = MolgenisConfigParser('config.txt').config
        self.session = molgenis.Session(self.config['url'])
        self.session.login(self.config['account'], self.config['password'])
        labs = self.config['labs'].split(',')
        self.labClassifications = dict.fromkeys(labs, [])
        self.get_paginated_table_content()

    def parse_table_content_page(self, page):
        # Here we get the first batch of items from the molgenis API and process its rows
        # Item passes and is saved when there is one omim disease code and the consensus classification is equal to
        # (Likely) benign(x), (Likely) pathogenic(x), VUS(x)
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
        labTable = 'VKGL_' + lab
        variant = self.session.getById(labTable, lab_id)
        variant['omim'] = omim
        del variant['_meta']
        del variant['_href']
        del variant['comments']
        self.labClassifications[lab].append(variant)

    def get_paginated_table_content(self):
        # This function will retrieve the items in the consensus table per 10.000, for each page,
        # we call parse_table_content_page
        total = self.session.get_total("VKGL_consensus")
        num = 10000
        times = math.ceil(total/num)
        startTime = time.time()
        for iter in range(times):
            start = ((iter+1)*num) - num
            print("Working on {}-{} of {}".format(start, start+num, total))
            consensusItems = self.session.get('VKGL_consensus', num=num, start=start)
            self.parse_table_content_page(consensusItems)
        print('Done in: ', time.time() - startTime, 'seconds')

def main():
    ConsensusTableParser()

if __name__ == '__main__':
    main()
