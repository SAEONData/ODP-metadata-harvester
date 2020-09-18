import sys
import traceback
from datetime import datetime
import pandas

class RecordParseError(Exception):
    pass

class ExcelImporter:
    _required_columns = \
        ['fileIdentifier', 'DOI', 'date', 'metadataStandardName', 'metadataStandardVersion',
         'metadataTimestamp', 'accessConstraints', 'descriptiveKeywords', 'title', 'responsibleParties',
         'responsibleParties.1','responsibleParties.Publisher','keyword','instrumentKeywords (CV)','status','topicCategories', 'abstract',
         'languages', 'formatName', 'spatialRepresentationType', 'spatialResolution', 'referenceSystemName', 'scope',
         'geographicIdentifier','placeKeywords (CV)', 'boundingBox', 'verticalElement', 'startTime', 'endTime', 'rights',
         'rightsURI', 'lineageStatement', 'onlineResources', 'relatedIdentifiers','size','fundingReferences','datasetVersion',
         'alternateIdentifiers']

    def __init__(self):
        pass


    def read_excel_to_json(self, spreadsheet_file, sheet):
        raw_record = None
        try:
            df = pandas.read_excel(spreadsheet_file,sheet,dtype=object)
            raw_records = []
            for index, row in df.iterrows():
                try:
                    raw_record = {}
                    col_titles = row.keys()
                    for title in col_titles:
                        raw_record[title] = row[title]
                    self.parse_raw_record(raw_record)
                    raw_records.append(raw_record)
                except RecordParseError as e:
                    print("{}    Record id: {}".format(e, raw_record['fileIdentifier']))
        except Exception as e:
            print("Error while reading excel speadsheet. {}".format(e))
            #traceback.print_exc(file=sys.stdout)
        return raw_records

    def parse_raw_record(self, record):
        # parse where necessary
        self.parse_file_identifier(record)
        self.parse_responsible_parties(record, 'responsibleParties')
        self.parse_responsible_parties(record, 'responsibleParties.1')
        self.parse_responsible_parties(record, 'responsibleParties.Publisher')

        self.parse_column_list(record, 'keyword')
        self.parse_column_list(record, 'topicCategories')
        self.parse_field_to_dict(record,'relatedIdentifiers',
                                       ['relatedIdentifier', 'relatedIdentifierType', 'relationType'])
        self.parse_listed_dict(record, 'onlineResources')
        self.parse_field_to_dict(record,'referenceSystemName',
                                       ['codeSpace', 'version'])
        self.parse_place_keywords(record, 'descriptiveKeywords', False)
        self.parse_place_keywords(record, 'placeKeywords (CV)', True)
        self.parse_place_keywords(record, 'instrumentKeywords (CV)', True)
        self.parse_field_to_dict(record,'boundingBox',
                                       ['northBoundLatitude', 'southBoundLatitude',
                                       'eastBoundLongitude', 'westBoundLongitude'],True)
        self.parse_field_to_dict(record,'verticalElement',['minimumValue','maximumValue','unitOfMeasure', 'verticalDatum'],True)
        self.parse_column_list(record,'size')
        self.parse_column_list(record,'fundingReferences')
        self.parse_listed_dict(record,'alternateIdentifiers')
        self.parse_time_field(record,'startTime')
        self.parse_time_field(record,'endTime')

        for col in record.keys():
            if str(record[col]) == 'nan' or record[col] is None:
                record[col] = None


    def parse_file_identifier(self, record):
        if type(record['fileIdentifier']) == float:
            record['fileIdentifier'] = str(int(record['fileIdentifier'].strip()))

    def parse_responsible_parties(self, record, field):
        valid_keys = ['individualName','organizationName','positionName','contactInfo','role','email']
        responsible_parties = []
        try:
            raw_str = record[field]
            for detail_str in raw_str.split("\n"):
                if len(detail_str.replace(" ","")) > 0:
                    detail = {'individualName':'','organizationName':'','positionName':'',
                              'contactInfo':'','role':'','email':''}
                    for item in detail_str.split("|"):
                        if 'email' in item and 'contactInfo' in item:
                            #print(item)
                            parts = item.split(',')
                            email_str = parts[-1]
                            email_k, email_v = email_str.split(":")
                            addr_str = ','.join(parts[0:len(parts) - 1])
                            addr_k, addr_v = addr_str.split(":")
                            email_k = email_k.replace(" ","")
                            addr_k = addr_k.replace(" ","")
                            if email_k not in valid_keys or addr_k not in valid_keys:
                                #print(k)
                                raise RecordParseError("bad field: %r" % item)
                            detail[email_k] = email_v
                            detail[addr_k] = addr_v
                        else:
                            parts = item.split(":",1)
                            if len(parts) != 2:
                                raise RecordParseError("bad field: %r" % item)
                            k,v = item.split(":",1)
                            k = k.replace(" ","")
                            if k not in valid_keys:
                                #print(k)
                                raise RecordParseError("bad field: {}".format(item))
                            if k == 'role':
                                v = v.replace(' ','')
                            detail[k] = v.replace(";","")
                    responsible_parties.append(detail)
        except RecordParseError as e:
            raise RecordParseError("Invalid responible party - {}".format(e))
        except Exception as e:
            raise RecordParseError("Invalid responible party - {}".format(item))
        record[field] = responsible_parties

    def parse_listed_dict(self, record, field):
        if str(record[field]) == 'nan':
            record[field] = ''
        else:
            resource = []
            raw_str = record[field]
            for detail_str in raw_str.split(";"):
                if len(detail_str.replace(" ", "")) > 0:
                    detail = {}
                    for item in detail_str.split("|"):
                       k, v = item.split(":",1)
                       k = k.replace(" ", "")
                       detail[k] = v.replace(";","")
                    resource.append(detail)
            record[field] = resource

    def parse_column_list(self, record, column):
        if ',' in record[column]:
            keywords = record[column].split(',')
            record[column] = keywords
        else:
            record[column] = [record[column]]

    def parse_bounding_box(self, record):
        parsed_box = {'North':'','South':'','East':'','West':''}
        box_parts = []
        box_str = record['Bounding Box']
        sep = None
        if ";" in box_str:
            sep = ";"
        elif ',' in box_str:
            sep = ','
        if sep:
            try:
                box_parts = box_str.split(sep)
                for part in box_parts:
                    #print(part)
                    if len(part.replace(" ","")) == 0:
                        continue
                    k,v = part.split(":")
                    k = k.replace(' ','')
                    if k not in parsed_box:
                        raise Exception()
                record['Bounding Box'] = parsed_box
            except:
                traceback.print_exc(file=sys.stdout)
                raise RecordParseError("Invalid bounding box: {}".format(box_str))

    def parse_place_keywords(self, record, field_name, append_mode=False):
        descriptive_keywords = []
        if str(field_name) == "descriptiveKeywords":
            if str(record[field_name]) == 'nan':
                return
            else:
                detail={'keywordType':'theme','keyword':''}
                raw_str = record[field_name]
                for item in raw_str.split("|"):
                    k, v = item.split(":",1)
                    k = k.replace(" ", "")
                    detail[k] = v.replace(";", "")
                descriptive_keywords.append(detail)
                if not append_mode:
                    record['descriptiveKeywords'] = descriptive_keywords
                else:
                    record['descriptiveKeywords'] = record['descriptiveKeywords'] + descriptive_keywords

        elif str(field_name) == "instrumentKeywords (CV)":
            if str(record[field_name]) == 'nan':
                return
            else:
                raw_str = record[field_name]
                for item in raw_str.split(","):
                    detail = {'keywordType': 'stratum', 'keyword': ''}
                    detail['keyword'] = item
                descriptive_keywords.append(detail)
                if not append_mode:
                    record['descriptiveKeywords'] = descriptive_keywords
                else:
                    record['descriptiveKeywords'] = record['descriptiveKeywords'] + descriptive_keywords

        elif str(field_name) == "placeKeywords (CV)":
            if str(record[field_name]) == 'nan':
                return
            else:
                raw_str = record[field_name]
                detail = {'keywordType': 'place', 'keyword': ''}
                for item in raw_str.split("|"):
                    k, v = item.split(":", 1)
                    k = k.replace(" ", "")
                    detail[k] = v.replace(";", "")
                descriptive_keywords.append(detail)

                if not append_mode:
                    record['descriptiveKeywords'] = descriptive_keywords
                else:
                    record['descriptiveKeywords'] = record['descriptiveKeywords'] + descriptive_keywords

        else:
            print("Invalid Keywords field")

    def parse_field_to_dict(self, record, field_name, valid_fields,all_fields=False):
        related_ids_str = record[field_name]
        if str(related_ids_str) == "nan":
            record[field_name] = None
            return
        related_ids = {}
        #print(related_ids_str)
        for item in related_ids_str.split("|"):
            parts = item.split(":")
            k = parts[0]
            v = ":".join(parts[1:len(parts)])

            k = k.replace(" ","")
            if len(k) == 0:
                continue
            if k not in valid_fields:
                #print(item)
                raise RecordParseError("Invalid %s field: %r" % (field_name,item))
            related_ids[k] = v
        record[field_name] = related_ids

        if all_fields:
            for field in valid_fields:
                if field not in record[field_name]:
                    raise RecordParseError("Invalid %r format: %r" % (field_name,str(record[field_name])))

    def parse_time_field(self,record,field_name):
        imported_time = record[field_name]
        if str(imported_time) == "nan":
            record[field_name] = None
            return
        converted_time = self.convert_date(imported_time)
        record[field_name] = converted_time

    def convert_date(self, date_input):
        supported_formats = ["%Y-%m-%d", "%d-%m-%Y", '%Y', "%Y/%m/%d %H:%M",
                             "%Y-%m-%d %H:%M:%S"]
        for fmt in supported_formats:
            try:
                return datetime.strptime(str(date_input), fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found record')