import metadataimporter
from builder import builder
class MetadataHarvest:

    def __init__(self):
        pass

    def get_records(self):
        # Creates a list of JSON records in multiple metadata standards and file sources to the controller
        json_record = []
        for imported_record in self.get_next_record():
            json_builder = self.get_builder(imported_record)
            json_record.append(json_builder)
        return json_record

    def get_builder(self, imported_record):
        recordBuilder = builder()
        #Intializes the builder based on the records standard
        if imported_record['metadataStandardName'] == 'Datacite':
            dataciteBuilder = recordBuilder.build_datacite_json_record(imported_record)
            return dataciteBuilder
        if imported_record['metadataStandardName'] == 'SANS 1878':
            sansBuilder = recordBuilder.build_sans_json_record(imported_record)
            return sansBuilder



    def get_next_record(self):
        #Returns a list of JSON records from a file
        importer = metadataimporter.MetadataImport()
        imported_records = importer.create_importer(filename='excel_sheets/T_Lamont_PEI_Bulk_data_submission.xlsx')
        return imported_records
        # implement in concrete importer class
        #raise NotImplementedError
