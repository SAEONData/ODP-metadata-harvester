from datetime import datetime
from schema import Schema
from schema import dataCiteSchemaFormatError

class DataCiteSchemaGenerator(Schema):
    # Create a DataCite JSON record
    def __init__(self,record_id):
        super().__init__(record_id)
        self.record = {}
        self.record['creators'] = []
        self.record['subjects'] = []
        self.record["dates"] = []
        self.record['alternateIdentifiers'] = []

    def set_identifier(self, identifier):
        self.record["identifier"] = {
            "identifier": identifier,
            "identifierType": "DOI"
        }

    def set_title(self, title):
        if not title:
            raise dataCiteSchemaFormatError('Title cannot be blank',record_id=self.record_id)

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


    def set_creators(self,creator):
        for person in creator:
            self.record['creators'].append(self.add_creators(person))

    def add_creators(self, creator):
        return {
            "name": creator['individualName'],
            "affiliations": [
                {
                    "affiliation": creator['organizationName']
                }
            ]
        }

    def set_subject(self,subjects):
        for word in subjects:
            self.record['subjects'].append(self.add_subject(word,'general'))

    def add_subject(self, subject, subjectScheme):
        return {
            "subject": subject,
            "subjectScheme": subjectScheme
        }

    def set_contributor(self,contributors):
        if contributors is not None:
            self.record['contributors'] = []
            for person in contributors:
                self.record['contributors'].append(self.add_contributor(person))

    def add_contributor(self, contributors):
        return {
            "contributorType": contributors['role'],
            "name": contributors['individualName'],
            "affiliations": [
                {
                    "affiliation": contributors['organizationName']
                }
            ]
        }

    def set_time(self,start_time, end_time):
        if not start_time and not end_time:
            pass
        elif isinstance(start_time,datetime) and isinstance(end_time,datetime):
            self.record['dates'] = []
            self.record['dates'].append(self.add_dates(start_time,end_time))
        elif isinstance(start_time,datetime) and not end_time:
            self.record['dates'] = []
            self.record['dates'].append(self.set_only_start_date(start_time))
        else:
            raise dataCiteSchemaFormatError()

    def add_only_start_date(self, start_date):
        timestamp_str = start_date.strftime("%Y-%m-%d")
        return {
                "date": timestamp_str + '/',
                "dateType": 'Valid'
            }

    def add_dates(self,start_date,end_date):
        return {
                "date": start_date.strftime("%Y-%m-%d") + '/' + end_date.strftime("%Y-%m-%d"),
                "dateType": 'Valid'
            }

    def set_language(self):
        self.record["language"] = "en-US"

    def set_resource_type(self, type):
        self.record["resourceType"] = {
            "resourceTypeGeneral": type
        }

    def set_alternative_identifiers(self,alternateIdentifiers):
        for identifier in alternateIdentifiers:
            self.record['alternateIdentifiers'].append(self.add_alternateIdentifiers(identifier))

    def add_alternateIdentifiers(self, alternate):
        return {
            "alternateIdentifier": alternate['identifier'],
            "alternateIdentifierType": alternate['identifierType']
        }

    def set_related_identifier(self,related):
        if related is None:
            pass
        else:
            self.record['relatedIdentifiers'] = []
            for related in related:
                if related['relationType'] == "IsMetadataFor" or related['relationType'] == "HasMetadata":
                    self.append(self.add_related_identifiers_metadata(related))
                else:
                    self.append(self.add_related_identifers(related))

    def add_related_identifers(self,related):
        return {
            "relatedIdentifier": related['relatedIdentifier'],
            "relatedIdentifierType": related['relatedIdentifierType'],
            "relationType": related['relationType']
            }

    def add_related_identifiers_metadata(self,related):
        return {
            "relatedIdentifier": related['relatedIdentifier'],
            "relatedIdentifierType": related['relatedIdentifierType'],
            "relationType": related['relationType'],
            "relatedMetadataScheme": related['metadataScheme'],
            "schemeURI": related['metadataSchemaURI']
            }

    def set_size(self, datasize):
        if datasize is None:
            pass
        else:
            self.record['size'] = []
            self.record['size'] = datasize

    def set_format(self, dataformat):
        if dataformat is None:
            pass
        else:
            self.record["formats"] = dataformat

    def set_version(self,version):
        if version is None:
            pass
        else:
            self.record["version"] = version

    def set_rights_list(self, rights, rightsURI):
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

    def set_funding_reference(self, reference):
        if reference is None:
            pass
        else:
            self.record["fundingReferences"] = []
            for funder in reference:
                self.record["fundingReferences"] = {
                    "funderName": funder['funder']
                }

    def set_online_resource(self,online_resources):
        if online_resources is None:
            pass
        else:
            for resource in online_resources:
                if resource['description'] == 'download':
                    self.set_immutableResource(resource)
                elif resource['description'] == 'information':
                    self.record['linkedResources'] = []
                    self.record['linkedResources'].append(self.set_linkedResources(resource))
                else:
                    pass

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

    def set_geolocation_box(self,bounding_box):
        if bounding_box is None:
            pass
        else:
            self.record['geoLocations'] = []
            self.record['geoLocations'].append(self.add_geolocation_box(bounding_box))

    def add_geolocation_box(self,box):
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