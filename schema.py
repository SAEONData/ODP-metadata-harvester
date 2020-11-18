class SchemaFormatError(Exception):
    def __init__(self, *args, **kwargs):
        self.record_id = kwargs.pop('record_id','')

class ISOSchemaFormatError(SchemaFormatError):
    pass

class dataCiteSchemaFormatError(SchemaFormatError):
    pass

class Schema:
    def __init__(self,record_id):
        self.record_id = record_id