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
        for record in harvester.get_records():
            try:
                result = client.create_or_update_metadata_record('chief-directorate-oceans-and-coastal-research',
                                                                 'marine-information-management-system-collection',
                                                                 'saeon-odp-4-2',
                                                                 record, capture_method='harvester',
                                                                 data_agreement_url='https://www.environment.gov.za/branches/oceans_coast')
                print(result)
            except ODPException as e:
                print(f"{e}: {e.error_detail}")