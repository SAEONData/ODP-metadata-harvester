import metadataHarvestor
#import ODPClient
import pprint

class HarvestController:

    def harvest_records(self):
        #Harvest records from a file and push them to a an API
        harvestor = metadataHarvestor.MetadataHarvest()
        for record in harvestor.get_records():
            pprint.pprint(record)
            #self.odp_client.create_record(record)