from datetime import datetime
from schema import dataCiteSchemaFormatError
from schema import Schema
import warnings

class DataCiteSchemaGenerator(Schema):
    # Create a DataCite JSON record
    def __init__(self,record_id):
        super().__init__(record_id)
        self.record = {}
        self.record['creators'] = []
        self.record['subjects'] = []
        self.record["dates"] = []

    def set_DOI(self,DOI):
        if not DOI:
            raise dataCiteSchemaFormatError('DOI is empty, record NOT posted',record_id=self.record_id)
        self.record['doi'] = DOI.strip()

    def set_identifier(self, identifiers):
        if not identifiers:
            warnings.warn(f'Record:{self.record_id}: identifiers is empty')
            return
        self.record['identifiers'] = []
        for identifier in identifiers:
            self.record['identifiers'].append(self.add_identifers(identifier))

    def add_identifers(self,identifier):
        return {
            "identifier": identifier['alternativeIdentifier'].strip(),
            "identifierType": identifier['alternativeIdentifierType'].strip()
        }

    def set_title(self, title):
        if not title:
            warnings.warn(f'Record:{self.record_id}: Mandatory Title field is empty')
            return

        self.record["titles"] = [
            {
                "title": title.strip()
            }]

    def set_publisher(self, publisher):
        if not publisher:
            warnings.warn(f'Record:{self.record_id}: Mandatory Publisher field is empty')
            return
        for party in publisher:
            if party['role'] == 'publisher':
                self.record["publisher"] = party['organizationName'].strip()

    def set_publication_year(self, year):
        if not year:
            warnings.warn(f'Record:{self.record_id}: Mandatory Publication year field is empty')
        self.record["publicationYear"] = int(year.strftime("%Y"))


    def set_creators(self,creator):
        if not creator:
            warnings.warn(f'Record:{self.record_id}: Mandatory Creator field is empty')
            return
        for person in creator:
            self.record['creators'].append(self.add_creators(person))

    def add_creators(self, creator):
        return {
            "name": creator['individualName'].strip(),
            "affiliation": [
                {
                    "affiliation": creator['organizationName'].strip()
                }
            ]
        }

    def set_subject(self,subjects):
        if not subjects:
            warnings.warn(f'Record:{self.record_id}: Mandatory subjects field is empty')
            return
        for word in subjects:
            self.record['subjects'].append(self.add_subject(word,'general'))

    def add_subject(self, subject, subjectScheme):
        return {
            "subject": subject.strip(),
            "subjectScheme": subjectScheme.strip()
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
            "affiliation": [
                {
                    "affiliation": contributors['organizationName'].strip()
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
            warnings.warn(f'Record:{self.record_id}: Mandatory Dates field is empty')
            return

    def set_only_start_date(self, start_date):
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
            warnings.warn(f'Record:{self.record_id}: Mandatory types field is empty')
            return
        self.record["types"] = {
            "resourceType": type.strip(),
            "resourceTypeGeneral": type.strip()
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
            "relatedIdentifier": related['relatedIdentifier'].strip(),
            "relatedIdentifierType": related['relatedIdentifierType'].strip(),
            "relationType": related['relationType'].strip()
            }

    def add_related_identifiers_metadata(self,related):
        return {
            "relatedIdentifier": related['relatedIdentifier'].strip(),
            "relatedIdentifierType": related['relatedIdentifierType'].strip(),
            "relationType": related['relationType'].strip(),
            "relatedMetadataScheme": related['metadataScheme'].strip(),
            "schemeURI": related['metadataSchemaURI'].strip()
            }

    def set_size(self, datasize):
        if not datasize:
            warnings.warn(f'Record:{self.record_id}: Data Size is empty, continuing with record')
            return
        self.record['sizes'] = []
        self.record['sizes'] = datasize.strip()

    def set_format(self, dataformat):
        if not dataformat:
            warnings.warn(f'Record:{self.record_id}: Data format is empty, continuing with record')
            return
        self.record["formats"] = [dataformat.strip()]

    def set_version(self,version):
        if not version:
            warnings.warn(f'Record:{self.record_id}: Version (dataset) is empty, continuing with record')
            return
        self.record["version"] = str(version)

    def set_rights_list(self, rights, rightsURI):
        if not rights:
            warnings.warn(f'Record:{self.record_id}: Mandatory Rights or Rights URI field is empty')
            return
        self.record["rightsList"] = [
            {
                "rights": rights.strip(),
                "rightsURI": rightsURI.strip()
            }
        ]

    def set_description(self, description):
        if not description:
            warnings.warn(f'Record:{self.record_id}: Mandatory description field is empty')
            return
        self.record["descriptions"] = [
            {
                "description": description.strip(),
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
                "funderName": funder['funder'].strip()
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
                "resourceDownload": {
                    "downloadURL" : resource['linkage']},
                "resourceName": resource['description'],
                "resourceDescription": resource['name']
            }

    def add_linkedResources(self, resource):
        return {
            "linkedResourceType": 'Information',
            "resourceURL": resource['linkage'].strip(),
            "resourceName": resource['description'].strip()
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
            "westBoundLongitude": float(box['westBoundLongitude']),
            "eastBoundLongitude": float(box['eastBoundLongitude']),
            "southBoundLatitude": float(box['southBoundLatitude']),
            "northBoundLatitude": float(box['northBoundLatitude'])
        }}
    def set_schema_version(self):
        self.record['schemaVersion'] = "http://datacite.org/schema/kernel-4"

    def get_filled_schema(self):
        return self.record