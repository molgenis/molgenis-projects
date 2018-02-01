from excelFile import ExcelFile


class ClinvarExportGenerator:
    def __init__(self, lab_variants, lab_name):
        clinvar_sheets = ['READ_ME', 'Variant', 'ExpEvidence', 'Deletes']
        self.clinvarExport = ExcelFile('clinvar_template.xlsx', clinvar_sheets)
        self.variantInfo = self.configure_variant_sheet()
        self.expEvidenceInfo = self.configure_ExpEvidence_sheet()
        self.process_variants(lab_variants)
        self.clinvarExport.save_to_new_file(lab_name+'_clinvar_export.xlsx')

    def process_variants(self, variants):
        for variant in variants:
            self.process_variant(variant, self.variantInfo)
            self.process_variant(variant, self.expEvidenceInfo)

    def process_variant(self, variant, info):
        for column in info['columns']:
            row = info['sheet'].find_first_empty_cell()
            columnId = info['columns'][column]
            sheet = info['sheet']
            if column in info['defaults']:
                sheet.alter(columnId, row, info['defaults'][column])
            else:
                values = [variant[attr] for attr in info['mapping'][column]]
                value = str(':'.join(values))
                sheet.alter(columnId, row, value)


    def configure_variant_sheet(self):
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
        {"id":"test","chromosome":"7","POS":26093141,"stop":26093141,"REF":"C","ALT":"A","gene":"HFE","cDNA":"c.845C>A","transcript":"y","protein":"x","type":"snp","location":"exonic","exon":"4","effect":"nonsynonymous","classification":"Pathogenic","comments":{"comments":"-"},"lab_upload_date":"2017-10-05 09:35:11","timestamp":"2017-06-15T10:37:55Z", 'omim':'123456'}
    ]
    ClinvarExportGenerator(testVariant, 'test')


if __name__ == '__main__':
    main()
