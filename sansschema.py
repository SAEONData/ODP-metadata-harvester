from datetime import datetime
import warnings
from schema import Schema
from schema import SANSSchemaFormatError

class SANS1878SchemaGenerator(Schema):
    # Create a SANS1878 JSON record
    def __init__(self,record_id):
        super().__init__(record_id)
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
        self.record["relatedIdentifiers"] = []

    def set_title(self, title):
        if not title:
            raise SANSSchemaFormatError('Title is empty, record not posted',record_id=self.record_id)
        self.record["title"] = title

    def set_date(self, date):
        if not date:
            raise SANSSchemaFormatError('date is empty, record not posted',record_id=self.record_id)
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
        if not responsible_parties_array:
            raise SANSSchemaFormatError('Responsible parties is empty, record not posted',record_id=self.record_id)
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
        if not identifier:
            raise SANSSchemaFormatError('Geographic Identifier is empty, record not posted',record_id=self.record_id)
        else:
            self.record["extent"]["geographicElements"][0]["geographicIdentifier"] = identifier

    def set_bounding_box_extent(self, bounding_box):
        if not bounding_box:
            raise SANSSchemaFormatError('Bounding Box is empty, record not posted', record_id=self.record_id)
        box = {
            "westBoundLongitude": float(bounding_box['westBoundLongitude']),
            "eastBoundLongitude": float(bounding_box['eastBoundLongitude']),
            "southBoundLatitude": float(bounding_box['southBoundLatitude']),
            "northBoundLatitude": float(bounding_box['northBoundLatitude'])
        }
        self.record["extent"]["geographicElements"][0]["boundingBox"] = box

    def add_bounding_polygon(self, polygon):
        if not polygon:
            warnings.warn(f'{self.record_id}: Bounding polygon is empty, continuing with record')
            return
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
        if not vertical_elements:
            warnings.warn(f'{self.record_id}: Vertical elements is empty, continuing with record')
            return
        vertical_extent = {
            "minimumValue": float(vertical_elements['minimumValue']),
            "maximumValue": float(vertical_elements['maximumValue']),
            "unitOfMeasure": vertical_elements['unitOfMeasure'],
            "verticalDatum": vertical_elements['verticalDatum']
        }
        self.record["extent"]["verticalElement"] = vertical_extent

    def set_temporal_extent(self, start_time, end_time):
        if not start_time or not end_time:
            raise SANSSchemaFormatError('Topic categories is empty, record not posted',record_id=self.record_id)
        if type(start_time) != datetime or type(end_time) != datetime:
            raise SANSSchemaFormatError("Invalid start/end time type, must be a datetime")
        format = "%Y-%2m-%2dT%H:%M:%S"
        start_time_str = start_time.strftime(format) + "+02:00"
        end_time_str = end_time.strftime(format) + "+02:00"
        temporal_extent = {
            "startTime": start_time_str,
            "endTime": end_time_str
        }
        self.record["extent"]["temporalElement"] = temporal_extent

    def set_languages(self, language):
        if not language:
            raise SANSSchemaFormatError('Language is empty, record not posted',record_id=self.record_id)
        self.record["languages"] = [language]

    def set_characterset(self, characterset):
        if not characterset:
            raise SANSSchemaFormatError('characterSet is empty, record not posted',record_id=self.record_id)
        self.record["characterSet"] = characterset

    def set_topic_categories(self, categories):
        if not categories:
            raise SANSSchemaFormatError('Topic categories is empty, record not posted',record_id=self.record_id)
        self.record["topicCategories"] = categories

    def set_spatial_resolution(self, resolution):
        if not resolution:
            self.record["spatialResolution"] = ''
            warnings.warn(f'Record:{self.record_id}: Spatial Resolution is empty, continuing with record')
            return
        self.record["spatialResolution"] = resolution

    def set_abstract(self, abstract):
        if not abstract:
            raise SANSSchemaFormatError('Abstract is empty, record not posted',record_id=self.record_id)
        self.record["abstract"] = abstract.decode()

    def set_distribution_format(self, format_name, format_version=None):
        if not format_name:
            raise SANSSchemaFormatError('Distribution format is empty, record not posted',record_id=self.record_id)
        format = {"formatName": format_name}
        # if format_version != list:
        #     raise SANSSchemaFormatError("Invalid distribution format type, must be a list")
        # format["formatVersion"] = format_version
        self.record["distributionFormats"].append(format)

    def set_spatial_representation_type(self, represenation):
        if not represenation:
            raise SANSSchemaFormatError('spatialRepresentationType cannot be blank', record_id=self.record_id)
        return
        rep_type_fixes = {'': '', 'vector': 'vector', 'grid': 'grid', \
                          'texttable': 'textTable', 'tin': 'tin', 'stereomodel': 'stereoModel', \
                          'video': 'video', 'image': 'image'}
        self.record["spatialRepresentationTypes"] = [rep_type_fixes[represenation.lower()]]

    def set_reference_system_name(self, reference):
        if not reference:
            raise SANSSchemaFormatError('referenceSystemName is empty, record not posted',record_id=self.record_id)
        self.record["referenceSystemName"] = {"codeSpace": reference['codeSpace'], "version": reference['version']}

    def set_lineage_statement(self, lineage):
        if not lineage:
            raise SANSSchemaFormatError('lineageStatement is empty, record not posted',record_id=self.record_id)
        self.record["lineageStatement"] = lineage.decode()

    def add_online_resources(self, onlineResources):
        if not onlineResources:
            raise SANSSchemaFormatError('onlineResource is empty, record not posted',record_id=self.record_id)
        for resource in onlineResources:
            if str(resource) == 'nan':
                self.record["onlineResources"] = ''
            else:
                online_resource = {
                    "name": resource['name'].strip(),
                    "description": resource['description'].strip(),
                    "linkage": resource['linkage'].strip()
                }
                self.record["onlineResources"].append(online_resource)

    def set_file_identifier(self, file_identifier):
        if not file_identifier:
            raise SANSSchemaFormatError('File Identifier is empty, record not posted',record_id=self.record_id)
        self.record["fileIdentifier"] = file_identifier

    def set_metadata_standard_name(self, metadata_standard):
        if not metadata_standard:
            raise SANSSchemaFormatError('metadataStandardName is empty, record not posted',record_id=self.record_id)
        self.record["metadataStandardName"] = metadata_standard

    def set_metadata_standard_version(self, standard_version):
        if not standard_version:
            raise SANSSchemaFormatError('metadataStandardVersion is empty, record not posted',record_id=self.record_id)
        self.record["metadataStandardVersion"] = str(standard_version)

    def set_metadata_language(self, language):
        if not language:
            raise SANSSchemaFormatError('metadataLanguage is empty, record not posted',record_id=self.record_id)
        self.record["metadataLanguage"] = language

    def set_metadata_characterset(self, characterset):
        if not characterset:
            raise SANSSchemaFormatError('metadataCharacterSet is empty, record not posted',record_id=self.record_id)
        self.record["metadataCharacterSet"] = characterset

    def set_metadata_time_stamp(self, timestamp):
        if not timestamp:
            raise SANSSchemaFormatError('metadataTimestamp cannot be blank',record_id=self.record_id)
        timestamp = self.convert_date(timestamp) #TODO check if this is coming through as datetime
        if type(timestamp) != datetime:
            raise SANSSchemaFormatError("Invalid metadata timestamp, must be datetime")
        format = "%Y-%m-%dT%H:%M:%S"
        # format="%Y-%m-%d %H:%M:%S"
        timestamp_str = timestamp.strftime(format) + "+02:00"
        self.record["metadataTimestamp"] = timestamp_str

    def set_purpose(self, purpose):
        if not purpose:
            self.record["purpose"] = ''
            warnings.warn(f'{self.record_id}: Purpose is empty, continuing with record')
            return
        self.record["purpose"] = purpose

    def set_scope(self, scope):
        if not scope:
            raise SANSSchemaFormatError('scope is empty, record not posted',record_id=self.record_id)
        self.record["scope"] = scope

    def set_status(self, status):
        if not status:
            raise SANSSchemaFormatError('status is empty, record not posted',record_id=self.record_id)
        if type(status) != list:
            raise SANSSchemaFormatError("Invalid status type, must be a list")
        self.record["status"] = status

    def set_keywords(self, keywords):
        if not keywords:
            warnings.warn(f'{self.record_id}: Keywords is empty, continuing with record')
            return
        for word in keywords:
            self.record["descriptiveKeywords"].append({
                "keywordType": 'general',
                "keyword": word
            })

    def set_descriptive_keywords(self, keywordArray):
        if not keywordArray:
            warnings.warn(f'{self.record_id}: Descriptive Keywords is empty, continuing with record')
            return
        else:
            for word in keywordArray:
                self.record["descriptiveKeywords"].append({
                    "keywordType": word['keywordType'].replace(' ', ''),
                    "keyword": word['keyword']
                })

    def set_constraints(self, rights, rights_uri, access_constraints, use_constraints='', classification='',
                        use_limitations=''):
        if not rights:
            raise SANSSchemaFormatError('Constraints is empty, record not posted',record_id=self.record_id)
        self.record["constraints"] = [{
            "rights": rights,
            "rightsURI": rights_uri,
            "useLimitations": [use_limitations],
            "accessConstraints": [access_constraints],
            "useConstraints": use_constraints,
            "classification": classification}]

    def set_related_identifiers(self, related_identifiers_array):
        if not related_identifiers_array:
            warnings.warn(f'{self.record_id}: Related Identifiers is empty, continuing with record')
            return
        for related in related_identifiers_array:
             related_identifiers = {
                "relatedIdentifier": related['relatedIdentifier'].strip(),
                "relatedIdentifierType": related['relatedIdentifierType'].strip(),
                "relationType": related['relationType'].strip()
             }
             self.record["relatedIdentifiers"].append(related_identifiers)

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
