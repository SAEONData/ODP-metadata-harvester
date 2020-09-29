import datetime
from schema import SANS1878SchemaGenerator
from schema import DataCiteSchemaGenerator

class builder:
    def __init__(self):
        pass

    def build_sans_json_record(self,imported_record):
        #Inserts the contents of the imported SANS record into the JSON format
        sansJSONrecord = SANS1878SchemaGenerator(imported_record['DOI']) #TODO: handle None type sent from records
        sansJSONrecord.begin_record()
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
        # Inserts the contents of the imported record into the datacite JSON format
        dataciteJSONrecord = DataCiteSchemaGenerator(imported_record['DOI'])

        #required fields
        dataciteJSONrecord.set_title(imported_record['title'])
        dataciteJSONrecord.set_publisher(imported_record['responsibleParties.Publisher'])
        dataciteJSONrecord.set_publication_year(imported_record['date'])
        dataciteJSONrecord.set_creators(imported_record['responsibleParties'])


        dataciteJSONrecord.record['subjects'] = []
        for word in imported_record['keyword']:
            dataciteJSONrecord.record['subjects'].append(dataciteJSONrecord.set_subject(word,'general'))
        dataciteJSONrecord.set_resource_type(imported_record['scope'])
        dataciteJSONrecord.set_rightsList(imported_record['rights'],imported_record['rightsURI'])
        dataciteJSONrecord.set_description(imported_record['abstract'])
        dataciteJSONrecord.record["dates"] = []
        dataciteJSONrecord.record['alternateIdentifiers'] = []
        for identifier in imported_record['alternateIdentifiers']:
            dataciteJSONrecord.record['alternateIdentifiers'].append(dataciteJSONrecord.set_alternateIdentifiers(identifier))

        #optional fields
        dataciteJSONrecord.set_identifier(imported_record['DOI'])
        dataciteJSONrecord.set_language()

        if imported_record['responsibleParties.1'] is not None:
            dataciteJSONrecord.record['contributors'] = []
            for person in imported_record['responsibleParties.1']:
                dataciteJSONrecord.record['contributors'].append(dataciteJSONrecord.set_contributor(person))

        if not imported_record['startTime'] and not imported_record['endTime']:
            pass
        elif isinstance(imported_record['startTime'],datetime.date) and isinstance(imported_record['endTime'],datetime.date):
            dataciteJSONrecord.record['dates'] = []
            dataciteJSONrecord.record['dates'].append(dataciteJSONrecord.set_date(imported_record['startTime'],imported_record['endTime']))
        elif isinstance(imported_record['startTime'],datetime.date) and not imported_record['endTime']:
            dataciteJSONrecord.record['dates'] = []
            dataciteJSONrecord.record['dates'].append(dataciteJSONrecord.set_only_start_date(imported_record['startTime']))
        else:
            print('error')

        if imported_record['fundingReferences'] is None:
            pass
        else:
            dataciteJSONrecord.record["fundingReferences"] = []
            dataciteJSONrecord.set_fundingReference(imported_record['fundingReferences'])

        if imported_record['size'] is None:
            pass
        else:
            dataciteJSONrecord.record['size'] = []
            dataciteJSONrecord.record['size'].append(dataciteJSONrecord.set_size(imported_record['size']))

        if imported_record['formatName'] is None:
            pass
        else:
            dataciteJSONrecord.set_format(imported_record['formatName'])

        if imported_record['datasetVersion'] is None:
            pass
        else:
            dataciteJSONrecord.set_version(imported_record['datasetVersion'])

        if imported_record['onlineResources'] is None:
            pass
        else:
            for resource in imported_record['onlineResources']:
                if resource['description'] == 'download':
                    dataciteJSONrecord.set_immutableResource(resource)
                elif resource['description'] == 'information':
                    dataciteJSONrecord.record['linkedResources'] = []
                    dataciteJSONrecord.record['linkedResources'].append(dataciteJSONrecord.set_linkedResources(resource))
                else:
                    pass

        if imported_record['relatedIdentifiers'] is None:
            pass
        else:
            dataciteJSONrecord.record['relatedIdentifiers'] = []
            for related in imported_record['relatedIdentifiers']:
                if related['relationType'] == "IsMetadataFor" or related['relationType'] == "HasMetadata":
                    imported_record['relatedIdentifiers'].append(dataciteJSONrecord.set_relatedIdentifiers_metadata(related))
                else:
                    imported_record['relatedIdentifiers'].append(dataciteJSONrecord.set_relatedIdentifers(related))

        if imported_record['boundingBox'] is None:
            pass
        else:
            dataciteJSONrecord.record['geoLocations'] = []
            dataciteJSONrecord.record['geoLocations'].append(dataciteJSONrecord.set_geolocation_box(imported_record['boundingBox']))

        return dataciteJSONrecord.record

