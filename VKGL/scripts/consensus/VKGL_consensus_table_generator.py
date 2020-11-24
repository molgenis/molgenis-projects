import math
import molgenis
from Molgenis_config_parser import MolgenisConfigParser
from omim_parser import OmimParser


class ConsensusTableGenerator():

  def __init__(self, labs, session, omim_file, consensus_table, comments_table,
      postfix):
    self.postfix = postfix
    self.comments_table = comments_table
    self.consensus_table = consensus_table
    print('Started')
    self.omim_codes = OmimParser(omim_file).codes
    print('Omim codes parsed')
    self.labs = labs
    self.session = session
    self.old_diseases = {}
    self.old_comments = {}
    self.clear_tables()
    self.lab_data = self.process_data()
    table = self.calculate_consensus()
    # self.export_csv(table)
    self.upload_consensus(table)

  def export_csv(self, table):
    csv = open('export.csv', 'w')
    header = dict.keys(table[0])
    csv.write('"')
    csv.write('","'.join(header))
    csv.write('"\n')
    for variant in table:
      for i, col in enumerate(variant):
        if i == 0:
          csv.write('"{}"'.format(variant[col]))
        else:
          csv.write(',"{}"'.format(variant[col]))
      csv.write('\n')
    csv.close()

  def process_lab(self, lab, num, start, consensus):
    print('Processing data of', lab)
    lab_data = self.session.get(lab + self.postfix, num=num, start=start)
    for variant in lab_data:
      variantId = variant['id'].replace(lab + '_', '')
      if variantId not in consensus:
        protein = ['' if 'protein' not in variant else variant['protein']][0]
        consensus[variantId] = {lab + '_classification': variant['id'],
                                'counter': {'b': 0, 'p': 0, 'v': 0},
                                'REF': variant['REF'], 'ALT': variant['ALT'],
                                'gene': variant['gene'],
                                'cDNA': variant['cDNA'], 'protein': protein,
                                'chromosome': str(variant['chromosome']),
                                'stop': str(variant['stop']),
                                'POS': str(variant['POS']),
                                'id': 'consensus_' + variantId,
                                'comments': 'consensus_' + variantId,
                                lab.lower(): variant['classification']}
        if variant['gene'] in self.omim_codes:
          consensus[variantId]['disease'] = self.omim_codes[variant['gene']]
      else:
        consensus[variantId][lab + '_classification'] = variant['id']
        consensus[variantId][lab.lower()] = variant['classification']
      if variant['classification'] == 'Benign' or variant[
        'classification'] == 'Likely benign':
        consensus[variantId]['counter']['b'] += 1
      elif variant['classification'] == 'Pathogenic' or variant[
        'classification'] == 'Likely pathogenic':
        consensus[variantId]['counter']['p'] += 1
      else:
        consensus[variantId]['counter']['v'] += 1
    return consensus

  def process_data(self):
    consensus = {}
    for lab in self.labs:
      total = self.session.get_total(lab + self.postfix)
      times = math.ceil(total / 10000)
      for time in range(times):
        start = ((time + 1) * 10000) - 10000
        num = 10000
        consensus = self.process_lab(lab, num, start, consensus)
    return consensus

  def process_consensus_chunk(self, num, start, ids):
    consensus = self.session.get(self.consensus_table, num=num, start=start)
    for row in consensus:
      ids.append(row['id'])
      self.old_diseases[row['id']] = \
      ['' if 'disease' not in row else row['disease']['mim_number']][0]
    return ids

  def delete_consensus(self, ids):
    if len(ids) > 0:
      print('Deleting consensus...')
      for chunk in self.chunks(ids, 1000):
        self.session.delete_list(self.consensus_table, chunk)

  def process_comments_chunk(self, num, start, ids):
    comments = self.session.get(self.comments_table, num=num, start=start)
    for row in comments:
      id = row['id']
      if id.startswith('consensus_'):
        ids.append(id)
        self.old_comments[id] = row['comments']
    return ids

  def delete_comments(self, ids):
    if len(ids) > 0:
      print('Deleting comments...')
      for i, chunk in enumerate(self.chunks(ids, 1000)):
        print(
        'Deleting chunk {} of {}'.format(i + 1, len(self.chunks(ids, 1000))))
        self.session.delete_list(self.comments_table, chunk)

  def clear_tables(self):
    consensus_total = self.session.get_total(self.consensus_table)
    if consensus_total > 0:
      times = math.ceil(consensus_total / 10000)
      print('Clearing consensus')
      ids = []
      for time in range(times):
        start = ((time + 1) * 10000) - 10000
        num = 10000
        ids = self.process_consensus_chunk(num, start, ids)
        # self.delete_consensus(ids)
        # print('Deleted consensus variants')
    comments_total = self.session.get_total(self.comments_table)
    ids = []
    if comments_total > 0:
      times = math.ceil(comments_total / 10000)
      print('Clearing comments')
      for time in range(times):
        start = ((time + 1) * 10000) - 10000
        num = 10000
        print(
        'Processing {} to {} of {}'.format(start, start + num, comments_total))
        ids = self.process_comments_chunk(num, start, ids)
      self.delete_comments(ids)
      print('Deleted comments')
    print('Done cleaning')
    # sys.exit()

  def calculate_consensus(self):
    molgenis_table = []
    for id in self.lab_data:
      variant = self.lab_data[id]
      b = variant['counter']['b']
      p = variant['counter']['p']
      v = variant['counter']['v']
      if b > 1 and p == 0 and v == 0:
        variant['consensus_classification'] = '(Likely) benign (' + str(b) + ')'
        variant['classification'] = 'b'
      elif b == 0 and p > 1 and v == 0:
        variant['consensus_classification'] = '(Likely) pathogenic (' + str(
          p) + ')'
        variant['classification'] = 'p'
      elif b == 0 and p == 0 and v > 1:
        variant['consensus_classification'] = 'VUS (' + str(v) + ')'
        variant['classification'] = 'v'
      elif b > 0 and p > 0:
        variant['consensus_classification'] = 'Opposite classification'
        variant['classification'] = 'op'
      elif (b > 0 and v > 0) or (p > 0 and v > 0):
        variant['consensus_classification'] = 'No consensus'
        variant['classification'] = 'no'
      elif b == 1 or v == 1 or p == 1:
        variant['consensus_classification'] = 'Classified by one lab'
        variant['classification'] = 'one'
      else:
        print('Something went wrong: ', b, v, p)
      self.lab_data[id] = variant
      del variant['counter']
      molgenis_table.append(variant)
    return molgenis_table

  def upload_comments(self):
    comments = []
    for id in self.lab_data:
      if id in self.old_comments:
        comments.append(
            {'id': 'consensus_' + id, 'comments': self.old_comments[id]})
      else:
        comments.append({'id': 'consensus_' + id, 'comments': '-'})
    comment_chunks = self.chunks(comments, 1000)
    for chunk in comment_chunks:
      self.session.add_all(self.comments_table, chunk)

  def upload_consensus(self, entities):
    self.upload_comments()
    print('Comments uploaded')
    entity_chunks = self.chunks(entities, 1000)
    for chunk in entity_chunks:
      self.session.add_all(self.consensus_table, chunk)
    print('Consensus uploaded\nDone!')

  def chunks(self, l, n=1000):
    """Yield successive n-sized chunks from l.
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks"""
    chunk_list = []
    for i in range(0, len(l), n):
      chunk_list.append(l[i:i + n])
    return chunk_list


def main():
  config = MolgenisConfigParser('config.txt').config
  labs = config['labs'].split(',')
  url = config['url']
  account = config['account']
  consensus_table = config['consensus_table']
  comments_table = config['comments_table']
  postfix = config['postfix']
  pwd = config['password']
  session = molgenis.Session(url)
  session.login(account, pwd)
  consensus = ConsensusTableGenerator(labs, session, 'omim.txt',
                                      consensus_table, comments_table, postfix)

if __name__ == '__main__':
  main()
