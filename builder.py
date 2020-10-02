import datetime
from sansschema import SANS1878SchemaGenerator
from dataciteschema import DataCiteSchemaGenerator

class builder:
    def __init__(self):
        pass

    def build_sans_json_record(self,imported_record):
        #Inserts the contents of the imported SANS record into the JSON format
        sansJSONrecord = SANS1878SchemaGenerator(imported_record['DOI'])
        sansJSONrecord.set_title(imported_record['title'])
        sansJSONrecord.set_date(imported_record['date'])
        sansJSONrecord.set_file_identifier(str(imported_record['fileIdentifier']))
        sansJSONrecord.set_responsible_party(imported_record['responsibleParties'])
        sansJSONrecord.set_responsible_party(imported_record['responsibleParties.1'])
        sansJSONrecord.set_responsible_party(imported_record['responsibleParties.Publisher'])
        sansJSONrecord.set_geographic_identifier(str(imported_record['geographicIdentifier']))
        sansJSONrecord.set_bounding_box_extent(imported_record['boundingBox'])
        sansJSONrecord.set_vertical_extent(imported_record['verticalElement'])
        sansJSONrecord.set_temporal_extent(imported_record['startTime'],imported_record['endTime'])
        sansJSONrecord.set_languages(imported_record['languages'])
        sansJSONrecord.set_characterset('utf8')
        sansJSONrecord.set_topic_categories(imported_record['topicCategories'])
        sansJSONrecord.set_spatial_resolution(imported_record['spatialResolution'])
        sansJSONrecord.set_abstract(imported_record['abstract'])
        sansJSONrecord.set_distribution_format(imported_record['formatName'])
        sansJSONrecord.set_spatial_representation_type(imported_record['spatialRepresentationType'])
        sansJSONrecord.set_reference_system_name(imported_record['referenceSystemName'])
        sansJSONrecord.set_lineage_statement(imported_record['lineageStatement'])
        sansJSONrecord.add_online_resources(imported_record['onlineResources'])
        sansJSONrecord.set_metadata_standard_name(imported_record['metadataStandardName'])
        sansJSONrecord.set_metadata_standard_version(imported_record['metadataStandardVersion'])
        sansJSONrecord.set_metadata_language(imported_record['languages'])
        sansJSONrecord.set_metadata_characterset('utf8')
        sansJSONrecord.set_metadata_time_stamp(imported_record['metadataTimestamp'])
        sansJSONrecord.set_purpose('')
        sansJSONrecord.set_scope(imported_record['scope'])
        sansJSONrecord.set_status([imported_record['status']])
        sansJSONrecord.set_descriptive_keywords(imported_record['descriptiveKeywords'])
        sansJSONrecord.set_keywords(imported_record['keyword'])
        sansJSONrecord.set_constraints(imported_record['rights'],imported_record['rightsURI'],imported_record['accessConstraints'])
        sansJSONrecord.set_related_identifiers(imported_record['relatedIdentifiers'])
        return sansJSONrecord.record

    def build_datacite_json_record(self,imported_record):
        # Inserts the contents of the imported record into the datacite JSON format
        dataciteJSONrecord = DataCiteSchemaGenerator(imported_record['DOI'])

        #required fields
        dataciteJSONrecord.set_title(imported_record['title'])
        dataciteJSONrecord.set_publisher(imported_record['responsibleParties.Publisher'])
        dataciteJSONrecord.set_publication_year(imported_record['date'])
        dataciteJSONrecord.set_creators(imported_record['responsibleParties'])
        dataciteJSONrecord.set_subject(imported_record['keyword'])
        dataciteJSONrecord.set_resource_type(imported_record['scope'])
        dataciteJSONrecord.set_rights_list(imported_record['rights'],imported_record['rightsURI'])
        dataciteJSONrecord.set_description(imported_record['abstract'])
        dataciteJSONrecord.set_alternative_identifiers(imported_record['alternateIdentifiers'])
        #optional fields
        dataciteJSONrecord.set_identifier(imported_record['DOI'])
        dataciteJSONrecord.set_language()
        dataciteJSONrecord.set_contributor(imported_record['responsibleParties.1'])
        dataciteJSONrecord.set_time(imported_record['startTime'],imported_record['endTime'])
        dataciteJSONrecord.set_funding_reference(imported_record['fundingReferences'])
        dataciteJSONrecord.set_size(imported_record['size'])
        dataciteJSONrecord.set_format(imported_record['formatName'])
        dataciteJSONrecord.set_version(imported_record['datasetVersion'])
        dataciteJSONrecord.set_online_resource(imported_record['onlineResources'])
        dataciteJSONrecord.set_related_identifier(imported_record['relatedIdentifiers'])
        dataciteJSONrecord.set_geolocation_box(imported_record['boundingBox'])
        return dataciteJSONrecord.record

