from datetime import datetime
class SANSSchemaFormatError(Exception):
    pass

class dataciteSchemaFormatError(Exception):
    pass

class Builder:
    def __init__(self):
        pass

# class DataCiteBuilder(Builder):
#     #Create a DataCite JSON record
#         def begin_record(self):
#             self.record = []
#
#         def set_identifier(self, identifier):
#             self.record["identifier"] = {
#                 "identifier": identifier,
#                 "identifierType": "DOI"
#             }
#
#         def set_title(self, title):
#             self.record["titles"] = [
#                 {
#                     "title": title
#                 }
#             ]
#             # TODO: Check if this is correct with mark
#
#         def set_publisher(self, publisher):
#             self.record["publisher"] = publisher
#
#         def set_publication_year(self, year):
#             self.record["publicationYear"] = year
#
#         def add_creators(self, name, surname, affiliation, ORCHIDID):
#             if type(name or surname or affiliation) != str:
#                 raise dataciteSchemaFormatError("Invalid file_identifier, must be a string")
#             self.record["creators"] = [
#                 {
#                     "name": "surname, name",
#                     "nameType": "Personal",
#                     "givenName": name,
#                     "familyName": surname,
#                     "nameIdentifiers": [
#                         {
#                             "nameIdentifier": ORCHIDID,
#                             "nameIdentifierScheme": "ORCID",
#                             "schemeURI": "http://orcid.org/"
#                         }
#                     ],
#                     "affiliations": [
#                         {
#                             "affiliation": affiliation
#                         }
#                     ]
#                 }
#             ]
#
#         def add_subject(self, subject, subjectScheme, SchemeURI):
#             self.record["subjects"] = [
#                 {
#                     "subject": subject,
#                     "subjectScheme": subjectScheme,
#                     "schemeURI": SchemeURI
#                 }
#             ]
#
#         def add_contributor(self, name, surname, affiliation, contributortype, ORCHID):
#             self.record["contributors"] = [
#                 {
#                     "contributorType": contributortype,
#                     "name": "{}, {}".format(surname, name),
#                     "givenName": name,
#                     "familyName": surname,
#                     "nameIdentifiers": [
#                         {
#                             "nameIdentifier": ORCHID,
#                             "nameIdentifierScheme": "ORCID",
#                             "schemeURI": "http://orcid.org/"
#                         }
#                     ],
#                     "affiliations": [
#                         {
#                             "affiliation": affiliation
#                         }
#                     ]
#                 }
#             ]
#
#         # def set_dates(self,date,datetype,dateinformation):
#         #     self.record["dates"] = [
#         #         {
#         #             "date": date,
#         #             "dateType": datetype,
#         #             "dateInformation": dateinformation
#         #         }]
#
#         def set_dates(self):
#             self.record["dates"] = [
#                 {
#                     "date": "2017-09-13",
#                     "dateType": "Updated",
#                     "dateInformation": "Updated with 4.2 properties"
#                 },
#                 {
#                     "date": "2018-09-21",
#                     "dateType": "Valid"
#                 }
#             ]  # TODO: Ask mark why this is an array vs not just one
#
#         def set_language(self):
#             self.record["language"] = "en-US"
#
#         def set_resourceType(self, description, type):
#             self.record["resourceType"] = {
#                 "resourceTypeGeneral": description,
#                 "resourceType": type
#             }
#
#         def add_alternateIdentifiers(self, description, type):
#             self.record["alternateIdentifiers"] = [
#                 {
#                     "alternateIdentifier": description,
#                     "alternateIdentifierType": type
#                 }
#             ]
#
#         # def add_relatedIdentifers(self,ID,relationType,relation):
#         #     if relationType == "IsMetadataFor" or relationType == "HasMetadata":
#         #         self.record["relatedIdentifiers"] = [
#         #             {
#         #                 "relatedIdentifier": "https://data.datacite.org/application/citeproc+json/10.5072/example-full",
#         #                 "relatedIdentifierType": "URL",
#         #                 "relationType": "HasMetadata",
#         #                 "relatedMetadataScheme": "citeproc+json",
#         #                 "schemeURI": "https://github.com/citation-style-language/schema/raw/master/csl-data.json"
#         #             }
#         #         ]
#         #     else:
#         #         self.record["relatedIdentifiers"] = [
#         #             {
#         #             "relatedIdentifier": "arXiv:0706.0001",
#         #             "relatedIdentifierType": "arXiv",
#         #             "relationType": "IsReviewedBy",
#         #             "resourceTypeGeneral": "Text"
#         #             }
#         #         ] #TODO: need to put the switch one level up so that inputs into the function are consistent across the cases
#
#         def set_size(self, datasize):
#             self.record["sizes"] = datasize
#
#         def set_format(self, dataformat):
#             self.record["formats"] = dataformat
#
#         def set_version(self):
#             self.record["version"] = "4.2"
#
#         def set_rightsList(self, rights, rightsURI, rightsIdentifier, rightsIdentifierScheme, schemeURI):
#             self.record["rightsList"] = [
#                 {
#                     "rights": rights,
#                     "rightsURI": rightsURI,
#                     "rightsIdentifier": rightsIdentifier,
#                     "rightsIdentifierScheme": rightsIdentifierScheme,
#                     "schemeURI": schemeURI
#                 }
#             ]
#
#         def set_description(self, description):
#             self.record["descriptions"] = [
#                 {
#                     "description": description,
#                     "descriptionType": "Abstract"
#                 }
#             ]
#
#         def set_geolocations(self, longitude, latitude):
#             self.record["geoLocations"] = [
#                 {
#                     "geoLocationPlace": "Atlantic Ocean",
#                     "geoLocationPoint": {
#                         "pointLongitude": "-67.302",
#                         "pointLatitude": "31.233"
#                     },
#                     "geoLocationBox": {
#                         "westBoundLongitude": "-71.032",
#                         "eastBoundLongitude": "-68.211",
#                         "southBoundLatitude": "41.090",
#                         "northBoundLatitude": "42.893"
#                     },
#                     "geoLocationPolygons": [
#                         {
#                             "polygonPoints": [
#                                 {
#                                     "pointLatitude": "41.991",
#                                     "pointLongitude": "-71.032"
#                                 },
#                                 {
#                                     "pointLatitude": "42.893",
#                                     "pointLongitude": "-69.622"
#                                 },
#                                 {
#                                     "pointLatitude": "41.991",
#                                     "pointLongitude": "-68.211"
#                                 },
#                                 {
#                                     "pointLatitude": "41.090",
#                                     "pointLongitude": "-69.622"
#                                 },
#                                 {
#                                     "pointLatitude": "41.991",
#                                     "pointLongitude": "-71.032"
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             ]
#             # TODO: Chat with leo regarding the when to switch between the three
#
#         def set_fundingReference(self, name, identifier, funderidentifor, awardnumber, awardTitle):
#             self.record["fundingReferences"] = [
#                 {
#                     "funderName": name,
#                     "funderIdentifier": identifier,
#                     "funderIdentifierType": funderidentifor,
#                     "awardNumber": awardnumber,
#                     "awardTitle": awardTitle
#                 }
#             ]
#
#         def set_immutableResource(self, URL, checksum, algorithm, name, description):
#             self.record["immutableResource"] = {
#                 "resourceURL": URL,
#                 "resourceChecksum": checksum,
#                 "checksumAlgorithm": algorithm,
#                 "resourceName": name,
#                 "resourceDescription": description
#             }
#
#         def set_linkedResources(self, resourcetype, resourceURL, resourceName, resourceDescription):
#             self.record["linkedResources"] = [
#                 {
#                     "linkedResourceType": resourcetype,
#                     "resourceURL": resourceURL,
#                     "resourceName": resourceName,
#                     "resourceDescription": resourceDescription
#                 }
#             ]
#         # def set_originalMetadata(self,):
#         #     self.record"originalMetadata": "<?xml version=\"1.0\"?><resource>...the original metadata...</resource>"
#         # TODO: check with mark about this field
#
#         def end_record(self):
#             built_record = self.record
#             return built_record

    # datacite=dataciteSchemaGenerator()
    # datacite.add_contributor("kyle","Cooper","SAEON","publisher","0000-0002-7285-027X")
    # pprint(datacite.record)

class SANS1878Builder(Builder):
    #Create a SANS1878 JSON record
    def __init__(self):
        pass

    def begin_record(self):
        #Create an empty SANS1878 record
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


    def set_responsible_party(self, responsible_parties_array):
        pass
        # for rparty in responsible_parties_array:
        #     contactInfo = "%r" % rparty['contactInfo']
        #     # contactInfo = rparty['contactInfo']
        #     if contactInfo == "''":
        #         contactInfo = ''
        #         # print("Invalid contact info {} {}".format(rparty, record['fileIdentifier']))
        #         # continue
        #     if len(rparty['email']) > 0:
        #         contactInfo = contactInfo + "," + rparty['email']
        #
        #     role_fixes = {'': '', 'resourceprovider': 'resourceProvider', 'custodian': 'custodian', 'owner': 'owner',
        #                   'user': 'user', 'distributor': 'distributor', 'originator': 'originator',
        #                   'pointofcontact': 'pointOfContact', 'principleinvestigator': 'principalInvestigator',
        #                   'principalinvestigator': 'principalInvestigator', 'processor': 'processor',
        #                   'publisher': 'publisher'}
        #
        #     def add responsible_party(self, name='', organization='', contact_info='', role='', position_name='',
        #                           online_resource=None):
        #
        #
        #
        #     schema_generator.add_responsible_party("%r" % rparty['individualName'], rparty['organizationName'],
        #                                            contactInfo, role_fixes[rparty['role'].lower()],
        #                                            rparty['positionName'])  # , online_resource)
        # responsible_party = {
        #     "individualName": name,
        #     "organizationName": organization,
        #     "contactInfo": contact_info,
        #     'positionName': position_name,
        #     'role': role,
        # }
        #
        # if online_resource:
        #     link = {"linkage": online_resource}
        #     responsible_party['onlineResource'] = link
        #
        # self.record["responsibleParties"].append(responsible_party)

    def set_geographic_identifier(self, identifier):
        if str(identifier) == 'nan':
            self.record["extent"]["geographicElements"][0]["geographicIdentifier"] = ''
        else:
            self.record["extent"]["geographicElements"][0]["geographicIdentifier"] = identifier

    def set_bounding_box_extent(self, bounding_box):
        bounding_box_template = {
            "westBoundLongitude": None,
            "eastBoundLongitude": None,
            "southBoundLatitude": None,
            "northBoundLatitude": None
        }

        self.record["extent"]["geographicElements"][0]["boundingBox"] = bounding_box

    def add_bounding_polygon(self,polygon):
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

    def set_vertical_extent(self, minimum_value, maximum_value, unit_of_measure, vertical_datum):
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
        if type(represenation) != list:
            raise SANSSchemaFormatError("Invalid spatial representation type, must be a list")
        self.record["spatialRepresentationTypes"] = represenation

    def set_reference_system_name(self, codespace, version):
        self.record["referenceSystemName"] = {"codeSpace": codespace, "version": version}

    def set_lineage_statement(self, lineage):
        self.record["lineageStatement"] = lineage

    def add_online_resources(self, name='', description='', link=''):
        online_resource = {
            "name": name.replace(" ", ""),
            "description": description.replace(" ", ""),
            "linkage": link.replace(" ", "")
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

    def add_descriptive_key_words(self, keyword_type, keyword):
        self.record["descriptiveKeywords"].append({
            "keywordType": keyword_type,
            "keyword": keyword
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

    def set_related_identifiers(self, identifier, id_type, relation_type):
        self.record["relatedIdentifiers"] = [{
            "relatedIdentifier": identifier,
            "relatedIdentifierType": id_type,
            "relationType": relation_type
        }]

    # def set_sort_hierarchy(self, hierarchy):
    #     self.record["hierarchy"] = hierarchy

    def convert_date(self,date_input):
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
