import os.path
import os

import excel
class MetadataImport:
    def __init__(self):
        pass

    #import filename or directory
    #determine the file type
    #create harvestor for that file type
    def create_importer(self, filename):
        #Creates an importer based on the file type
        fileExtension = os.path.splitext(filename)[1]
        if fileExtension == '.xlsx':
            sheet = os.environ['SHEET_NAME']
            excel_importer = excel.ExcelImporter()
            records = excel_importer.read_excel_to_json(filename,sheet)
            return records
        else:
            raise Exception('No importer created, no filename provided')


