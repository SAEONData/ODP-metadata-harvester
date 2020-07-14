import metadataimporter
import builder
class MetadataHarvest:

    def __init__(self):
        pass

    def get_records(self):
        # Creates a list of JSON records in multiple metadata standards and file sources to the controller
        for imported_record in self.get_next_record():
            json_record = []
            builder = self.create_builder(imported_record['metadataStandardName'])
            json_record.append(self.build_json_record(builder, imported_record))
            print('lul')
            return json_record

    def create_builder(self, metadata_standard):
        #Intializes the builder based on the records standard
        if metadata_standard == 'DataCite':
            test = builder.DataCiteBuilder()
            return test
        if metadata_standard == 'SANS 1878':
            sansBuilder = builder.SANS1878Builder()
            return sansBuilder

    def build_json_record(self, builder, imported_record):
        #Inserts the contents of the imported record into the JSON format
        #builder.begin_record()
        builder.set_title(imported_record['title'])
        #builder.set_identifier(imported_record['fileIdentifier'])
        #builder.set_publisher(imported_record['responsibleParties.Publisher'])
        #builder.set_publication_year(imported_record['date'])
        #builder.add_creators(imported_record['responsibleParties']) #TODO creators excel structure needs to be mapped to JSON structure correctly
        #builder.add_subject(imported_record['keyword']) #TODO excel structure needs to be mapped to JSON structure correctly and deal with multiple keywords
        #builder.add_contributor(imported_record['responsibleParties.1']) #TODO the excel structure needs to be mapped to the JSON
        #builder.set_dates(imported_record['identifier']) #TODO Dates needs to be dealt with as an array
        #builder.set_language(imported_record['languages']) #TODO creators excel structure needs to be mapped to JSON structure correctly
        #builder.set_resourceType(imported_record['identifier']) #TODO resourceType needs to be sourced from spreadsheet
        #builder.add_alternateIdentifiers(imported_record['relatedIdentifiers']) #TODO the excel structure needs to be mapped to the JSON
        #builder.set_size(imported_record['identifier']) #TODO Size needs to be sourced from spreadsheet
        #builder.set_format(imported_record['formatName'])
        #builder.set_version(imported_record['metadataStandardVersion']) #TODO the excel structure needs to be mapped to the JSON
        #builder.set_rightsList(imported_record['rights'],imported_record'rightsURI') #TODO rightslist needs to accept two arguments
        builder.set_description(imported_record['abstract'])
        #builder.set_geolocations(imported_record['boundingBox']) #TODO the excel structure needs to be mapped to the JSON
        #builder.set_fundingReference(imported_record['identifier']) #TODO: funding reference needs to be sourced from spreadsheet
        #builder.set_immutableResource(imported_record['onlineResources']) #TODO: map the structure from excel to the JSON
        #builder.set_linkedResources(imported_record['relatedIdentifiers']) #TODO: map the structure from excel to the JSON
        return builder.end_record()

    def get_next_record(self):
        #Returns a list of JSON records from a file
        importer = metadataimporter.MetadataImport()
        imported_records = importer.create_importer(filename='excel_sheets/AMS_test_metadata.xlsx')
        return imported_records
        # implement in concrete importer class
        #raise NotImplementedError
