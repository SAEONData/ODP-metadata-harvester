from datetime import datetime
from schema import Schema
from schema import dataCiteSchemaFormatError
import warnings

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
        if not identifier:
            raise dataCiteSchemaFormatError('Identifier is empty, record not posted',record_id=self.record_id)
        self.record["identifier"] = {
            "identifier": identifier,
            "identifierType": "DOI"
        }

    def set_title(self, title):
        if not title:
            raise dataCiteSchemaFormatError('Title is empty, record not posted',record_id=self.record_id)

        self.record["titles"] = [
            {
                "title": title
            }]

    def set_publisher(self, publisher):
        if not publisher:
            raise dataCiteSchemaFormatError('Publisher is empty, record not posted',record_id=self.record_id)
        for party in publisher:
            if party['role'] == 'publisher':
                self.record["publisher"] = party['organizationName']

    def set_publication_year(self, year):
        if not year:
            raise dataCiteSchemaFormatError('Publication year is empty, record not posted',record_id=self.record_id)
        self.record["publicationYear"] = year.strftime("%Y")


    def set_creators(self,creator):
        if not creator:
            raise dataCiteSchemaFormatError('Creator is empty, record not posted',record_id=self.record_id)
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
        if not subjects:
            raise dataCiteSchemaFormatError('Subjects is empty, record not posted',record_id=self.record_id)
        for word in subjects:
            self.record['subjects'].append(self.add_subject(word,'general'))

    def add_subject(self, subject, subjectScheme):
        return {
            "subject": subject,
            "subjectScheme": subjectScheme
        }

    def set_contributor(self,contributors):
        if not contributors:
            warnings.warn(f'Record:{self.record_id}: Contributors is empty, continuing with record')
            return
        for person in contributors:
            self.record['contributors'] = []
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
            raise dataCiteSchemaFormatError('dates is empty, record not posted',record_id=self.record_id)

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
        if not type:
            raise dataCiteSchemaFormatError('Resource Type is empty, record not posted',record_id=self.record_id)
        self.record["resourceType"] = {
            "resourceType": type,
            "resourceTypeGeneral": type
        }

    def set_alternative_identifiers(self,alternateIdentifiers):
        if not alternateIdentifiers:
            raise dataCiteSchemaFormatError('Alternate Identifiers is empty, record not posted',record_id=self.record_id)
        for identifier in alternateIdentifiers:
            self.record['alternateIdentifiers'].append(self.add_alternateIdentifiers(identifier))

    def add_alternateIdentifiers(self, alternate):
        return {
            "alternateIdentifier": alternate['identifier'],
            "alternateIdentifierType": alternate['identifierType']
        }

    def set_related_identifier(self,related):
        if not related:
            warnings.warn(f'Record:{self.record_id}: Related Identifiers is empty, continuing with record')
            return
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
        if not datasize:
            warnings.warn(f'Record:{self.record_id}: Data Size is empty, continuing with record')
            return
        self.record['sizes'] = []
        self.record['sizes'] = datasize

    def set_format(self, dataformat):
        if not dataformat:
            warnings.warn(f'Record:{self.record_id}: Data format is empty, continuing with record')
            return
        self.record["formats"] = [dataformat]

    def set_version(self,version):
        if not version:
            warnings.warn(f'Record:{self.record_id}: Version (dataset) is empty, continuing with record')
            return
        self.record["version"] = str(version)

    def set_rights_list(self, rights, rightsURI):
        if not rights:
            raise dataCiteSchemaFormatError('Rights or Rights URI is empty, record not posted',record_id=self.record_id)
        self.record["rightsList"] = [
            {
                "rights": rights,
                "rightsURI": rightsURI
            }
        ]

    def set_description(self, description):
        if not description:
            raise dataCiteSchemaFormatError('Description is empty, record not posted',record_id=self.record_id)
        self.record["descriptions"] = [
            {
                "description": description.decode(),
                "descriptionType": "Abstract"
            }
        ]

    def set_funding_reference(self, reference):
        if not reference:
            warnings.warn(f'Record:{self.record_id}: Funding reference is empty, continuing with record')
            return
        self.record["fundingReferences"] = []
        for funder in reference:
            self.record["fundingReferences"].append({
                "funderName": funder['funder']
            })

    def set_online_resource(self,online_resources):
        if not online_resources:
            warnings.warn(f'Record:{self.record_id}: Online Resources is empty, continuing with record')
            return
        for resource in online_resources:
            if resource['description'] == 'download':
                self.add_immutableResource(resource)
            elif resource['description'] == 'information':
                self.record['linkedResources'] = []
                self.record['linkedResources'].append(self.add_linkedResources(resource))
            else:
                pass

    def add_immutableResource(self, resource):
            self.record["immutableResource"] = {
                "resourceURL": resource['linkage'],
                "resourceName": resource['description'],
                "resourceDescription": resource['name']
            }

    def add_linkedResources(self, resource):
        return {
            "linkedResourceType": 'Information',
            "resourceURL": resource['linkage'],
            "resourceName": resource['description']
        }

    def set_geolocation_box(self,bounding_box):
        if not bounding_box:
            warnings.warn(f'Record:{self.record_id}: Geolocation box is empty, continuing with record')
            return
        self.record['geoLocations'] = []
        self.record['geoLocations'].append(self.add_geolocation_box(bounding_box))

    def add_geolocation_box(self,box):
        return {"geoLocationBox":
            {
            "westBoundLongitude": box['westBoundLongitude'],
            "eastBoundLongitude": box['eastBoundLongitude'],
            "southBoundLatitude": box['southBoundLatitude'],
            "northBoundLatitude": box['northBoundLatitude']
        }}

    def get_filled_schema(self):
        return self.record