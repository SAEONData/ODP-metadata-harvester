from datetime import datetime


class SANSSchemaFormatError(Exception):
    pass


class dataCiteSchemaFormatError(Exception):
    pass


class Schema:
    def __init__(self):
        pass


class DataCiteSchemaGenerator(Schema):
    # Create a DataCite JSON record

    def set_identifier(self, identifier):
        self.record["identifier"] = {
            "identifier": identifier,
            "identifierType": "DOI"
        }

    def set_title(self, title):
        self.record["titles"] = [
            {
                "title": title
            }]

    def set_publisher(self, publisher):
        for party in publisher:
            if party['role'] == 'publisher':
                self.record["publisher"] = party['organizationName']

    def set_publication_year(self, year):
        self.record["publicationYear"] = year

    def set_creators(self, creator):
        return {
            "name": creator['individualName'],
            "affiliations": [
                {
                    "affiliation": creator['organizationName']
                }
            ]
        }

    def set_subject(self, subject, subjectScheme):
        return {
            "subject": subject,
            "subjectScheme": subjectScheme
        }

    def set_contributor(self, contributors):
        return {
            "contributorType": contributors['role'],
            "name": contributors['individualName'],
            "affiliations": [
                {
                    "affiliation": contributors['organizationName']
                }
            ]
        }

    def set_only_start_date(self, start_date):
        timestamp_str = start_date.strftime("%Y-%m-%d")
        return {
                "date": timestamp_str + '/',
                "dateType": 'Valid'
            }

    def set_date(self,start_date,end_date):
        return {
                "date": start_date.strftime("%Y-%m-%d") + '/' + end_date.strftime("%Y-%m-%d"),
                "dateType": 'Valid'
            }

    def set_language(self):
        self.record["language"] = "en-US"

    def set_resource_type(self, type):
        self.record["resourceType"] = {
            "resourceTypeGeneral": 'TK'  # TODO: Enquire to mark about this field
            , "resourceType": type
        }

    def set_alternateIdentifiers(self, alternate):
        return {
            "alternateIdentifier": alternate['identifier'],
            "alternateIdentifierType": alternate['identifierType']
        }

    def set_relatedIdentifers(self,related):
        return {
            "relatedIdentifier": related['relatedIdentifier'],
            "relatedIdentifierType": related['relatedIdentifierType'],
            "relationType": related['relationType']
            }

    def set_relatedIdentifiers_metadata(self,related):
        return {
            "relatedIdentifier": related['relatedIdentifier'],
            "relatedIdentifierType": related['relatedIdentifierType'],
            "relationType": related['relationType'],
            "relatedMetadataScheme": related['metadataScheme'],
            "schemeURI": related['metadataSchemaURI']
            }

    def set_size(self, datasize):
        self.record["sizes"] = datasize  # TODO: Because this is a list, check if it's one value

    def set_format(self, dataformat):
        self.record["formats"] = dataformat

    def set_version(self,version):
        self.record["version"] = version

    def set_rightsList(self, rights, rightsURI):
        self.record["rightsList"] = [
            {
                "rights": rights,
                "rightsURI": rightsURI
            }
        ]

    def set_description(self, description):
        self.record["descriptions"] = [
            {
                "description": description,
                "descriptionType": "Abstract"
            }
        ]

    def set_geolocations(self, location):
        self.record["geoLocations"] = [
            {
                "geoLocationPlace": "Atlantic Ocean",
                "geoLocationPoint": {
                    "pointLongitude": "-67.302",
                    "pointLatitude": "31.233"
                },
                "geoLocationBox": {
                    "westBoundLongitude": "-71.032",
                    "eastBoundLongitude": "-68.211",
                    "southBoundLatitude": "41.090",
                    "northBoundLatitude": "42.893"
                },
                "geoLocationPolygons": [
                    {
                        "polygonPoints": [
                            {
                                "pointLatitude": "41.991",
                                "pointLongitude": "-71.032"
                            },
                            {
                                "pointLatitude": "42.893",
                                "pointLongitude": "-69.622"
                            },
                            {
                                "pointLatitude": "41.991",
                                "pointLongitude": "-68.211"
                            },
                            {
                                "pointLatitude": "41.090",
                                "pointLongitude": "-69.622"
                            },
                            {
                                "pointLatitude": "41.991",
                                "pointLongitude": "-71.032"
                            }
                        ]
                    }
                ]
            }
        ]
        # TODO: Chat with leo regarding the when to switch between the three

    def set_fundingReference(self, name):
        self.record["fundingReferences"] = {
                "funderName": name
            }

    def set_immutableResource(self, resource):
            self.record["immutableResource"] = {
                "resourceURL": resource['linkage'],
                "resourceName": resource['description'],
                "resourceDescription": resource['name']
            }

    def set_linkedResources(self, resource):
        return {
            "linkedResourceType": 'Information',
            "resourceURL": resource['linkage'],
            "resourceName": resource['description']
        }

    def set_geolocation_box(self,box):
        return {
            "westBoundLongitude": box['westBoundLongitude'],
            "eastBoundLongitude": box['eastBoundLongitude'],
            "southBoundLatitude": box['southBoundLatitude'],
            "northBoundLatitude": box['northBoundLatitude']
        }

    # def set_originalMetadata(self,):
    #     self.record"originalMetadata": "<?xml version=\"1.0\"?><resource>...the original metadata...</resource>"
    # TODO: check with mark about this field

    def get_filled_schema(self):
        return self.record

class SANS1878SchemaGenerator(Schema):
    # Create a SANS1878 JSON record
    def __init__(self):
        pass

    def begin_record(self):
        # Create an empty SANS1878 record
        self.record = {}
        self.record["responsibleParties"] = []
        self.record["extent"] = {
            "geographicElements": [{"geographicIdentifier": None,
                                    "boundingBox": None,
                                    "boundingPolygon": []}],
            "verticalElement": {},
            "temporalElement": {}
        }
        self.record["distributionFormats"] = []
        self.record["descriptiveKeywords"] = []
        self.record["onlineResources"] = []
        return self.record

    def set_title(self, title):
        self.record["title"] = title

    def set_date(self, date):
        if type(date) != datetime:
            converted_date = self.convert_date(str(date))
            self.record["date"] = converted_date.strftime("%Y-%2m-%2d")
        else:
            self.record["date"] = date.strftime("%Y-%2m-%2d")

    def add_responsible_party(self, name='', organization='', contact_info='', role='', position_name='',
                              online_resource=None):
        responsibleParties = {
            "individualName": name,
            "organizationName": organization,
            "contactInfo": contact_info,
            'positionName': position_name,
            'role': role,
        }

        return self.record['responsibleParties'].append(responsibleParties)

    def set_responsible_party(self, responsible_parties_array):
        role_fixes = {'': '', 'resourceprovider': 'resourceProvider', 'custodian': 'custodian', 'owner': 'owner',
                      'user': 'user', 'distributor': 'distributor', 'originator': 'originator',
                      'pointofcontact': 'pointOfContact', 'principleinvestigator': 'principalInvestigator',
                      'principalinvestigator': 'principalInvestigator', 'processor': 'processor',
                      'publisher': 'publisher'}
        for rparty in responsible_parties_array:
            contactInfo = "%r" % rparty['contactInfo']
            # contactInfo = rparty['contactInfo']
            if contactInfo == "''":
                contactInfo = ''
                # print("Invalid contact info {} {}".format(rparty, record['fileIdentifier']))
                # continue
            if len(rparty['email']) > 0:
                contactInfo = contactInfo + "," + rparty['email']
            self.add_responsible_party("%r" % rparty['individualName'], rparty['organizationName'],
                                       contactInfo, role_fixes[rparty['role'].lower()],
                                       rparty['positionName'])  # , online_resource)

    def set_geographic_identifier(self, identifier):
        if str(identifier) == 'nan':
            self.record["extent"]["geographicElements"][0]["geographicIdentifier"] = ''
        else:
            self.record["extent"]["geographicElements"][0]["geographicIdentifier"] = identifier

    def set_bounding_box_extent(self, bounding_box):
        box = {
            "westBoundLongitude": float(bounding_box['westBoundLongitude']),
            "eastBoundLongitude": float(bounding_box['eastBoundLongitude']),
            "southBoundLatitude": float(bounding_box['southBoundLatitude']),
            "northBoundLatitude": float(bounding_box['northBoundLatitude'])
        }
        self.record["extent"]["geographicElements"][0]["boundingBox"] = box

    def add_bounding_polygon(self, polygon):
        if type(polygon) != list or len(polygon) < 5:
            raise SANSSchemaFormatError("Invalid polygon type, must be a list with 5 elements")

        valid_keys = ['longitude', 'latitude']
        for point in polygon:
            if type(point) != dict:
                raise SANSSchemaFormatError("Invalid polygon element, must be a dict")
            for k in point.keys():
                if k not in valid_keys:
                    raise SANSSchemaFormatError("Invalid polygon key name, must be 'longitude' or 'latitude'")

        self.record["extent"]["geographicElements"][0]["boundingPolygon"].append(polygon)

    def set_vertical_extent(self, vertical_elements):

        minimum_value = vertical_elements['minimumValue']
        maximum_value = vertical_elements['maximumValue']
        unit_of_measure = vertical_elements['unitOfMeasure']
        vertical_datum = vertical_elements['verticalDatum']
        vertical_extent = {
            "minimumValue": minimum_value,
            "maximumValue": maximum_value,
            "unitOfMeasure": unit_of_measure,
            "verticalDatum": vertical_datum
        }
        self.record["extent"]["verticalElement"] = vertical_extent

    def set_temporal_extent(self, start_time, end_time):
        start_time_str = self.convert_date(start_time)
        end_time_str = self.convert_date(end_time)
        if type(start_time_str) != datetime or type(end_time_str) != datetime:
            raise SANSSchemaFormatError("Invalid start/end time type, must be a datetime")
        format = "%Y-%2m-%2dT%H:%M:%S"
        start_time_str = start_time_str.strftime(format) + "+02:00"
        end_time_str = end_time_str.strftime(format) + "+02:00"
        temporal_extent = {
            "startTime": start_time_str,
            "endTime": end_time_str
        }
        self.record["extent"]["temporalElement"] = temporal_extent

    def set_languages(self, language):
        self.record["languages"] = [language]

    def set_characterset(self, characterset):
        self.record["characterSet"] = characterset

    def set_topic_categories(self, categories):
        if type(categories) != list:
            raise SANSSchemaFormatError("Invalid categories type, must be a list")
        self.record["topicCategories"] = categories

    def set_spatial_resolution(self, resolution):
        self.record["spatialResolution"] = resolution

    def set_abstract(self, abstract):
        self.record["abstract"] = abstract

    def add_distribution_format(self, format_name, format_version=None):
        format = {"formatName": format_name}
        # if format_version != list:
        #     raise SANSSchemaFormatError("Invalid distribution format type, must be a list")
        # format["formatVersion"] = format_version
        self.record["distributionFormats"].append(format)

    def set_spatial_representation_type(self, represenation):
        if str(represenation) == 'nan':
            self.record["spatialRepresentationTypes"] = ''
        else:
            rep_type_fixes = {'': '', 'vector': 'vector', 'grid': 'grid', \
                              'texttable': 'textTable', 'tin': 'tin', 'stereomodel': 'stereoModel', \
                              'video': 'video', 'image': 'image'}
            self.record["spatialRepresentationTypes"] = [rep_type_fixes[represenation.lower()]]

    def set_reference_system_name(self, reference):
        self.record["referenceSystemName"] = {"codeSpace": reference['codeSpace'], "version": reference['version']}

    def set_lineage_statement(self, lineage):
        self.record["lineageStatement"] = lineage

    def add_online_resources(self, onlineResources):
        for resource in onlineResources:
            if str(resource) == 'nan':
                self.record["onlineResources"] = ''
            else:
                online_resource = {
                    "name": resource['name'],
                    "description": resource['description'],
                    "linkage": resource['linkage']
                }
                self.record["onlineResources"].append(online_resource)

    def set_file_identifier(self, file_identifier):
        if type(file_identifier) != str:
            raise SANSSchemaFormatError("Invalid file_identifier, must be a string")
        self.record["fileIdentifier"] = file_identifier

    def set_metadata_standard_name(self, metadata_standard):
        self.record["metadataStandardName"] = metadata_standard

    def set_metadata_standard_version(self, standard_version):
        self.record["metadataStandardVersion"] = standard_version

    def set_metadata_language(self, language):
        self.record["metadataLanguage"] = language

    def set_metadata_characterset(self, characterset):
        self.record["metadataCharacterSet"] = characterset

    def set_metadata_time_stamp(self, timestamp):
        timestamp = self.convert_date(timestamp)
        if type(timestamp) != datetime:
            raise SANSSchemaFormatError("Invalid metadata timestamp, must be datetime")
        format = "%Y-%m-%dT%H:%M:%S"
        # format="%Y-%m-%d %H:%M:%S"
        timestamp_str = timestamp.strftime(format) + "+02:00"
        self.record["metadataTimestamp"] = timestamp_str

    def set_purpose(self, purpose):
        self.record["purpose"] = purpose

    def set_scope(self, scope):
        self.record["scope"] = scope

    def set_status(self, status):
        if type(status) != list:
            raise SANSSchemaFormatError("Invalid status type, must be a list")
        self.record["status"] = status

    def add_keywords(self, keywords):
        for word in keywords:
            self.record["descriptiveKeywords"].append({
                "keywordType": 'general',
                "keyword": word
            })

    def add_descriptiveKeywords(self, keywordArray):
        if str(keywordArray) == 'nan':
            return
        else:
            for word in keywordArray:
                self.record["descriptiveKeywords"].append({
                    "keywordType": word['keywordType'].replace(' ', ''),
                    "keyword": word['keyword']
                })

    def set_constraints(self, rights, rights_uri, access_constraints, use_constraints='', classification='',
                        use_limitations=''):
        if use_constraints != '' and type(use_constraints) != list:
            raise SANSSchemaFormatError("Invalid use_constraints type, must be a list")
        self.record["constraints"] = [{
            "rights": rights,
            "rightsURI": rights_uri,
            "useLimitations": [use_limitations],
            "accessConstraints": [access_constraints],
            "useConstraints": use_constraints,
            "classification": classification}]

    def set_related_identifiers(self, related_identifiers_array):
        self.record["relatedIdentifiers"] = {
            "relatedIdentifier": related_identifiers_array['relatedIdentifier'],
            "relatedIdentifierType": related_identifiers_array['relatedIdentifierType'],
            "relationType": related_identifiers_array['relationType']
        }

    def convert_date(self, date_input):
        supported_formats = ["%Y-%m-%d", "%d-%m-%Y", '%Y', "%Y/%m/%d %H:%M",
                             "%Y-%m-%d %H:%M:%S"]  # 2015/03/12 12:00
        for fmt in supported_formats:
            try:
                return datetime.strptime(str(date_input), fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found record')

    def get_filled_schema(self):
        return self.record
