from dataciteschema import DataCiteSchemaGenerator
from sansschema import SANS1878SchemaGenerator

class SchemaFormatError(Exception):
    def __init__(self, *args, **kwargs):
        self.record_id = kwargs.pop('record_id','')

class SANSSchemaFormatError(SchemaFormatError):
    pass

class dataCiteSchemaFormatError(SchemaFormatError):
    pass

class Schema:
    def __init__(self,record_id):
        self.record_id = record_id