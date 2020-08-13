import metadataimporter
import builder
class MetadataHarvest:

    def __init__(self):
        pass

    def get_records(self):
        # Creates a list of JSON records in multiple metadata standards and file sources to the controller
        json_record = []
        for imported_record in self.get_next_record():
            builder = self.create_builder(imported_record['metadataStandardName'])
            json_record.append(self.build_json_record(builder, imported_record))
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
        builder.begin_record()
        builder.set_title(imported_record['title'])
        builder.set_date(imported_record['date'])
        builder.set_file_identifier(str(imported_record['fileIdentifier']))
        #builder.set_responsible_party(imported_record['responsibleParties'])
        #builder.add_responsible_party(imported_record['responsibleParties.1'])
        #builder.add_responsible_party(imported_record['responsibleParties.Publisher'])
        #builder.set_geographic_identifier(str(imported_record['geographicIdentifier']))
        #builder.set_bounding_box_extent(imported_record['boundingBox'])
        #builder.set_vertical_extent(imported_record['verticalElement'])
        # builder.set_temporal_extent(imported_record['startTime'],imported_record['endTime'])
        # builder.set_languages(imported_record['languages'])
        # builder.set_characterset('utf8')
        # builder.set_topic_categories(imported_record['topicCategories'])
        # builder.set_spatial_resolution(imported_record['spatialResolution'])
        # builder.set_abstract(imported_record['abstract'])
        # builder.add_distribution_format(imported_record['formatName'])
        # builder.set_spatial_representation_type(imported_record['spatialRepresentationType'])
        # builder.set_reference_system_name(imported_record['referenceSystemName'])
        # builder.set_lineage_statement(imported_record['lineageStatement'])
        # builder.add_online_resources(imported_record['onlineResources'])
        # builder.set_metadata_standard_name(imported_record['metadataStandardName'])
        # builder.set_metadata_standard_version(imported_record['metadataStandardVersion'])
        # builder.set_metadata_language(imported_record['languages'])
        # builder.set_metadata_characterset('utf8')
        # builder.set_metadata_time_stamp(imported_record['metadataTimestamp'])
        # builder.set_purpose("")
        # builder.set_scope(imported_record['scope'])
        # builder.set_status(imported_record['status'])
        # builder.add_keywords(imported_record['descriptiveKeywords'],imported_record['placeKeywords (CV)'],imported_record['keyword'])
        # builder.set_constraints(imported_record['rights'],imported_record['rightsURI'],imported_record['accessConstraints'])
        # builder.set_related_identifiers(imported_record['relatedIdentifiers'])
        # builder.set_abstract(imported_record['abstract'])
        return builder.record

    def get_next_record(self):
        #Returns a list of JSON records from a file
        importer = metadataimporter.MetadataImport()
        imported_records = importer.create_importer(filename='excel_sheets/T_Lamont_PEI_Bulk_data_submission.xlsx')
        return imported_records
        # implement in concrete importer class
        #raise NotImplementedError
