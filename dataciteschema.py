from datetime import datetime
from schema import Schema
from schema import dataCiteSchemaFormatError

class DataCiteSchemaGenerator(Schema):
    # Create a DataCite JSON record
    def __init__(self):
        self.record = {}
        self.record['creators'] = []

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


    def set_creators(self,*args):
        for person in args:
            self.record['creators'].append(self.set_creators(person))

    def add_creators(self, creator):
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
            "resourceTypeGeneral": type
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
        self.record["sizes"] = datasize

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