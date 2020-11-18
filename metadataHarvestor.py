import metadataimporter
from schema import SchemaFormatError
from builder import builder
from builder import builderError
import os

class MetadataHarvest:

    def __init__(self):
        pass

    def get_records(self):
        # Creates a list of JSON records in multiple metadata standards and file sources to the controller
        json_records = []
        imported_records = []
        for imported_record in self.get_next_record():
            try:
                json_builder = self.get_builder(imported_record)
                json_records.append(json_builder)
                imported_records.append(imported_record)
            except SchemaFormatError as e:
                print(f'!Schema ERROR!: record ID {e.record_id}:{e}')
        return json_records,imported_records;

    def get_builder(self, imported_record):
        recordBuilder = builder()
        #Intializes the builder based on the records standard
        if imported_record['metadataStandardName'] == 'Datacite':
            dataciteBuilder = recordBuilder.build_datacite_json_record(imported_record)
            return dataciteBuilder
        elif imported_record['metadataStandardName'] == 'ISO19115':
            sansBuilder = recordBuilder.build_sans_json_record(imported_record)
            return sansBuilder
        else:
            raise builderError('Builder not available')

    def get_next_record(self):
        #Returns a list of JSON records from a file
        importer = metadataimporter.MetadataImport()
        imported_records = importer.create_importer(filename=os.environ['FILE_NAME'])
        return imported_records
        # implement in concrete importer class
        #raise NotImplementedError
