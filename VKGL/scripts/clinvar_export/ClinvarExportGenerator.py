from excelFile import ExcelFile
from ProgressBar import ProgressBar


class ClinvarExportGenerator:
    def __init__(self, lab_variants, lab_name):
        clinvar_sheets = ['READ_ME', 'SubmissionInfo', 'Variant', 'ExpEvidence', 'Deletes']
        print("Writing output for {}...".format(lab_name))
        self.clinvarExport = ExcelFile('clinvar_template.xlsx', clinvar_sheets)
        self.variantInfo = self.configure_variant_sheet()
        self.expEvidenceInfo = self.configure_ExpEvidence_sheet()
        self.process_variants(lab_variants)
        self.clinvarExport.save_to_new_file( 'export/{}_clinvar_export.xlsx'.format(lab_name))
        print('{}_clinvar_export.xlsx created'.format(lab_name))

    def process_variants(self, variants):
        """NAME: process_variants
        INPUT: variants (list of dictionary with the information needed for submission)
        PURPOSE: process all variants classified by the lab"""
        progress = ProgressBar(len(variants))
        progress.get_next(0)
        for i, variant in enumerate(variants):
            self.process_variant(variant, self.variantInfo)
            self.process_variant(variant, self.expEvidenceInfo)
            progress.get_next(i+1)
        progress.get_next(len(variants))
        print(progress.get_done_message('min'))

    def process_variant(self, variant, info):
        """NAME: process_variant
        PURPOSE: convert the data of one variant to the clinvar export format (save in excel file)"""
        row = info['sheet'].find_first_empty_row(2)
        for column in info['columns']:
            columnId = info['columns'][column]
            sheet = info['sheet']
            if column in info['defaults']:
                sheet.alter(columnId, row, info['defaults'][column])
            else:
                values = [variant[attr] for attr in info['mapping'][column]]
                value = str(':'.join(values))
                sheet.alter(columnId, row, value)


    def configure_variant_sheet(self):
        """NAME: configure_variant_sheet
        PURPOSE: set up the mapping between variant and the variant sheet of clinvar and set up the variant sheet
        OUTPUT: variant_info (a dictionary with a mapping from the VKGL variant to the Clinvar variant sheet, for some
        clinvar columns default values, the clinvar column names and the sheet in which the information is stored)"""
        sheet = self.clinvarExport.sheets['Variant']

        variant_info = {
            'mapping': {
                'variant_col': ['transcript', 'cDNA'],
                'condition_value_col': ['omim'],
                'clinical_significance_col': ['classification'],
                'gene_symbol_col': ['gene']
            },
            'defaults': {
                'condition_type_col': 'OMIM'
            },
            'columns': {
                'variant_col': 'A',
                'condition_type_col': 'B',
                'condition_value_col': 'C',
                'clinical_significance_col': 'E',
                'gene_symbol_col': 'R'
            },
            'sheet': sheet
        }

        return variant_info

    def configure_ExpEvidence_sheet(self):
        """NAME: configure_ExpEvidence_sheet
        PURPOSE: set up the mapping between variant and the ExpEvidence sheet of clinvar and set up the ExpEvidence sheet
        OUTPUT: expEvidence (a dictionary with a mapping from the VKGL variant to the Clinvar ExpEvidence sheet, for some
        clinvar columns default values, the clinvar column names and the sheet in which the information is stored)"""
        sheet = self.clinvarExport.sheets['ExpEvidence']

        expEvidence = {
            'mapping': {
                'variant_col': ['transcript', 'cDNA'],
                'condition_value_col': ['omim']
            },
            'defaults': {
                'condition_type_col': 'OMIM',
                'collection_method_col': 'clinical testing',
                'allele_origin_col': 'germline',
                'affected_status_col': 'yes'
            },
            'columns': {
                'variant_col': 'A',
                'condition_type_col': 'B',
                'condition_value_col': 'C',
                'collection_method_col': 'E',
                'allele_origin_col': 'F',
                'affected_status_col': 'G'
            },
            'sheet': sheet
        }

        return expEvidence


def main():
    testVariant = [
        {"id":"test","chromosome":"7","POS":26093141,"stop":26093141,"REF":"C","ALT":"A","gene":"HFE","cDNA":"c.845C>A","transcript":"y","protein":"x","type":"snp","location":"exonic","exon":"4","effect":"nonsynonymous","classification":"Pathogenic","comments":{"comments":"-"},"lab_upload_date":"2017-10-05 09:35:11","timestamp":"2017-06-15T10:37:55Z", 'omim':'123456'},
        {"id": "test2", "chromosome": "7", "POS": 26093141, "stop": 26093141, "REF": "C", "ALT": "A", "gene": "HFE",
         "cDNA": "c.845C>A", "transcript": "y", "protein": "x", "type": "snp", "location": "exonic", "exon": "4",
         "effect": "nonsynonymous", "classification": "Pathogenic", "omim": '123456'}
    ]
    ClinvarExportGenerator(testVariant, 'test')


if __name__ == '__main__':
    main()
