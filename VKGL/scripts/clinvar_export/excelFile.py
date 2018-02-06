__author__ = 'mslofstra'
from openpyxl import load_workbook
from excelSheet import ExcelSheet

class ExcelFile:
    """Class EmxFile
    contains all the operations that an emx file can do (and are needed in this application)
    with the openpyxl library
    """
    def __init__(self, filename, sheets):
        self.filename = filename
        self.workbook = load_workbook(self.filename)
        self.sheets = {}
        for sheet in sheets:
            self.sheets[sheet]= (ExcelSheet(self.workbook[sheet]))

    def save_overwrite_file_changes(self):
        """function save_file_changes
        saves the emx file with the original file name
        """
        self.workbook.save(self.filename)

    def save_to_new_file(self, filename):
        """function save_file_changes
        saves the emx file with the original file name
        """
        self.workbook.save(filename)

    def get_workbook(self):
        """function get_workbook
        returns the workbook to work with
        """
        return self.workbook



