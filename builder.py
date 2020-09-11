from schema import SANS1878SchemaGenerator
from schema import DataCiteSchemaGenerator
class builder:
    def __init__(self):
        pass

    def build_sans_json_record(self,imported_record):
        #Inserts the contents of the imported SANS record into the JSON format
        sansJSONrecord = SANS1878SchemaGenerator()
        sansJSONrecord.begin_record()
        sansJSONrecord.set_title(imported_record['title'])
        sansJSONrecord.set_date(imported_record['date'])
        sansJSONrecord.set_file_identifier(str(imported_record['fileIdentifier']))
        sansJSONrecord.set_responsible_party(imported_record['responsibleParties'])
        sansJSONrecord.set_geographic_identifier(str(imported_record['geographicIdentifier']))
        sansJSONrecord.set_bounding_box_extent(imported_record['boundingBox'])
        sansJSONrecord.set_vertical_extent(imported_record['verticalElement'])
        sansJSONrecord.set_temporal_extent(imported_record['startTime'],imported_record['endTime'])
        sansJSONrecord.set_languages(imported_record['languages'])
        sansJSONrecord.set_characterset('utf8')
        sansJSONrecord.set_topic_categories(imported_record['topicCategories'])
        sansJSONrecord.set_spatial_resolution(imported_record['spatialResolution'])
        sansJSONrecord.set_abstract(imported_record['abstract'])
        sansJSONrecord.add_distribution_format(imported_record['formatName'])
        sansJSONrecord.set_spatial_representation_type(imported_record['spatialRepresentationType'])
        sansJSONrecord.set_reference_system_name(imported_record['referenceSystemName'])
        sansJSONrecord.set_lineage_statement(imported_record['lineageStatement'])
        sansJSONrecord.add_online_resources(imported_record['onlineResources'])
        sansJSONrecord.set_metadata_standard_name(imported_record['metadataStandardName'])
        sansJSONrecord.set_metadata_standard_version(imported_record['metadataStandardVersion'])
        sansJSONrecord.set_metadata_language(imported_record['languages'])
        sansJSONrecord.set_metadata_characterset('utf8')
        sansJSONrecord.set_metadata_time_stamp(imported_record['metadataTimestamp'])
        sansJSONrecord.set_purpose("")
        sansJSONrecord.set_scope(imported_record['scope'])
        sansJSONrecord.set_status([imported_record['status']])
        sansJSONrecord.add_descriptiveKeywords(imported_record['descriptiveKeywords'])
        sansJSONrecord.add_keywords(imported_record['keyword'])
        sansJSONrecord.set_constraints(imported_record['rights'],imported_record['rightsURI'],imported_record['accessConstraints'])
        sansJSONrecord.set_related_identifiers(imported_record['relatedIdentifiers'])
        sansJSONrecord.set_abstract(imported_record['abstract'])
        return sansJSONrecord.record

    def build_datacite_json_record(self,imported_record):
        dataciteJSONrecord = DataCiteSchemaGenerator()
        dataciteJSONrecord.begin_record()
        #dataciteJSONrecord.set_identifier(imported_record['DOI'])
        #dataciteJSONrecord.set_title(title='This is the main title',subtitle='This is the subtitle') #TODO: Function before schema
        dataciteJSONrecord.set_publisher(imported_record['responsibleParties'])
        dataciteJSONrecord.set_publication_year(imported_record['date'])
        #dataciteJSONrecord.set_subject() #TODO: Function before schema
        #dataciteJSONrecord.set_contributor(imported_record['responsibleParties.1']) #TODO: Function before schema
        #dataciteJSONrecord.add_creators(imported_record['responsibleParties']) #TODO: Function before schema
        #dataciteJSONrecord.set_date(imported_record['date']) #TODO: Check with mark
        dataciteJSONrecord.set_language()
        dataciteJSONrecord.set_resource_type(imported_record['scope'])
        #dataciteJSONrecord.add_alternateIdentifiers(imported_record['relatedIdentifiers']) #TODO: Function before schema
        #dataciteJSONrecord.set_size('') #TODO: No input field
        dataciteJSONrecord.set_format(imported_record['formatName'])
        dataciteJSONrecord.set_version() #TODO: check what version this is refering to
        #dataciteJSONrecord.set_rightsList(imported_record['rights'],imported_record['rightsURI']) #TODO: Check with Mark
        dataciteJSONrecord.set_description(imported_record['abstract'])
        #dataciteJSONrecord.set_geolocations(imported_record['boundingBox'],imported_record['placeKeywords (CV)'],imported_record['geographicIdentifier']) #TODO: Function before schema
        #dataciteJSONrecord.set_fundingReference('') #TODO: No input field
        #dataciteJSONrecord.set_immutableResource(imported_record['onlineResources']) #TODO: Check if this is the download link
        #dataciteJSONrecord.set_linkedResources(imported_record['onlineResources']) #TODO: Check if this is supplementary info
        return dataciteJSONrecord.record

