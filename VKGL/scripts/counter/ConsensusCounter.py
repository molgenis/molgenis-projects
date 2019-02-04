import molgenis, sys, pprint, re
from Molgenis_config_parser import MolgenisConfigParser


class ConsensusCounter:
  def __init__(self, table, session):
    self.report = open('report.txt', 'w')
    self.write_report_header()
    self.session = session
    self.counts = {
      'p': 0,
      'b': 0,
      'v': 0,
      'op': 0,
      'one': 0,
      'no': 0
    }
    self.one_counts = {
      'Likely pathogenic': 0,
      'Pathogenic': 0,
      'Likely benign': 0,
      'Benign': 0,
      'VUS': 0
    }
    self.opposites = []
    self.process_data_in_batches(table)
    self.write_count_output()
    self.write_one_count_output()
    self.report.close()

  def write_report_header(self):
    self.report.write('OPPOSITES:\n')

  def write_opposites_line(self, variant, classifications):
    self.report.write(
        '{}:{}-{}\tREF:{}\tALT:{}\t({})\n'.format(variant['chromosome'], variant['POS'], variant['stop'],
                                                  variant['REF'], variant['ALT'], variant['gene']))
    for lab in classifications:
      self.report.write('{}: {}\n'.format(lab, classifications[lab]))
    self.report.write('\n')

  def process_data_in_batches(self, table):
    total = self.session.get_total(table)
    start = 0
    while start < total:
      batch = self.retrieve_data_batch(table, start)
      self.process_batch(batch)
      start += 10000

  def get_lab_classifications(self, variant, classification):
    possible_keys = ['amc', 'nki', 'erasmus', 'vumc', 'umcu', 'lumc', 'umcg', 'radboud']
    classifications = {}
    for key in possible_keys:
      if key in variant:
        classifications[key] = variant[key]
        if classification == 'one':
          return variant[key]
    return classifications

  def write_count_output(self):
    self.report.write('\nCOUNTS:\n')
    translation = {
      'p': '(Likely) pathogenic',
      'b': '(Likely) benign',
      'v': 'VUS',
      'op': 'Opposite classifications',
      'no': 'No consensus'
    }
    for count in self.counts:
      if count != 'one':
        self.report.write('{}: {}\n'.format(translation[count], self.counts[count]))

  def write_one_count_output(self):
    self.report.write('Classified by one lab (' + str(self.counts['one']) + '):\n')
    for count in self.one_counts:
      self.report.write('\t- {}: {}\n'.format(count, self.one_counts[count]))

  def process_batch(self, batch):
    for variant in batch:
      classification = variant['classification']['id']
      self.counts[classification] += 1
      if classification == 'one' or classification == 'op':
        classifications = self.get_lab_classifications(variant, classification)
        if classification == 'one':
          self.one_counts[classifications] += 1
        else:
          self.write_opposites_line(variant, classifications)

  def retrieve_data_batch(self, table, start):
    batch = self.session.get(table, num=10000, start=start)
    return batch


def main():
  config = MolgenisConfigParser('config.txt').config
  server = config['url']
  account = config['account']
  consensus_table = config['consensus_table']
  pwd = config['password']
  session = molgenis.Session(server)
  session.login(account, pwd)
  cc = ConsensusCounter(consensus_table, session)
  session.logout()


if __name__ == '__main__':
  main()
