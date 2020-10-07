import metadataHarvestor
from odp.client import ODPClient
from odp.exceptions import ODPException
from dotenv import load_dotenv
import os
import pprint

class HarvestController:

    def harvest_records(self):
        #Harvest records from a file and push them to a an API
        harvester = metadataHarvestor.MetadataHarvest()
        load_dotenv(f'{os.getcwd()}/.env')
        client = ODPClient()
        records = harvester.get_records()
        imported_rec = records[1]
        json_rec = records[0]
        for i in range(len(json_rec)):
            try:
                process_rec = imported_rec[i]
                post_rec = json_rec[i]
                if process_rec['metadataStandardName'] == 'Datacite':
                    result = client.create_or_update_metadata_record('chief-directorate-oceans-and-coastal-research',
                                                                     'marine-information-management-system-collection',
                                                                     'saeon-odp-4-2',
                                                                     post_rec, capture_method='harvester',
                                                                     data_agreement_url='https://www.environment.gov.za/branches/oceans_coast')
                    pprint.pprint(result['errors'],indent=4)
                elif process_rec['metadataStandardName'] == 'SANS 1878':
                    result = client.create_or_update_metadata_record('chief-directorate-oceans-and-coastal-research',
                                                                     'marine-information-management-system-collection',
                                                                     'sans-1878-mims-historical-1',
                                                                     post_rec, capture_method='harvester',
                                                                     data_agreement_url='https://www.environment.gov.za/branches/oceans_coast')
                    pprint.pprint(result['errors'],indent=4)
            except ODPException as e:
                print(f"{e}: {e.error_detail}")