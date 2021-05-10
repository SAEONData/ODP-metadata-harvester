import metadataHarvestor
from odp.client import ODPClient
from odp.exceptions import ODPException
from dotenv import load_dotenv
import os
import pprint
from setup_logger import logger


class HarvestController:

    def harvest_records(self):
        # Harvest records from a file and push them to a an API
        harvester = metadataHarvestor.MetadataHarvest()
        load_dotenv(f'{os.getcwd()}/.env')
        logger.debug('Loaded enviromental variables')
        client = ODPClient(timeout=30)
        records = harvester.get_records()
        imported_rec = records[1]
        json_rec = records[0]
        for i in range(len(json_rec)):
            try:
                process_rec = imported_rec[i]
                post_rec = json_rec[i]
                # print(post_rec)
                if 'doi' in post_rec and len(post_rec['doi']) > 0:
                    curr_doi = str(post_rec['doi'].strip())
                else:
                    curr_doi = None
                curr_sid = str(post_rec['fileIdentifier'].strip())

                """
                role_check_list = ['pointOfContact', 'originator', 'publisher']
                for role in role_check_list:
                    missing_role = True
                    #print(type(post_rec['responsibleParties']))
                    for party in post_rec['responsibleParties']:
                        #print("{}\n".format(party))
                        if role == party['role']:
                            missing_role = False
                    if missing_role:
                        print("{} role is missing".format(role))
                #print("{}\n".format(post_rec['responsibleParties']))
                continue
                """

                logger.info("Attempting to add record DOI - {} ; SID - {}".format(curr_doi, curr_sid))
                upload_result = None
                if process_rec['metadataStandardName'] == 'Datacite':
                    upload_result = client.create_or_update_metadata_record('chief-directorate-oceans-and-coastal-research',
                                                                     'marine-information-management-system-collection',
                                                                     'saeon-datacite-4-3',
                                                                     post_rec,
                                                                     doi=str(post_rec['doi'].strip()))
                elif process_rec['metadataStandardName'] == 'ISO19115':
                    if curr_doi:
                        upload_result = client.create_or_update_metadata_record('chief-directorate-oceans-and-coastal-research',
                                                                         'marine-information-management-system-collection',
                                                                         'iso19115-saeon-profile',
                                                                         post_rec,
                                                                         doi=curr_doi,
                                                                         sid=post_rec['fileIdentifier'].strip())
                    else:
                        upload_result = client.create_or_update_metadata_record('chief-directorate-oceans-and-coastal-research',
                                                                         'marine-information-management-system-collection',
                                                                         'iso19115-saeon-profile',
                                                                         post_rec,
                                                                         sid=post_rec['fileIdentifier'].strip())

                if not upload_result or 'id' not in upload_result:
                    raise Exception("Could not add record {} {}".format(curr_doi, curr_sid))

                if len(upload_result['errors']) > 0:
                    logger.error("Errors when trying to add record {} {}".format(curr_sid, upload_result['errors']))

                if not upload_result['validated']:
                    raise Exception("Record was not validated, unable to proceed with workflow update.")

                logger.info("Added record {} with id: {} to ODP, attempting workflow update ...".format(curr_doi, upload_result['id']))

                workflow_result = client.change_state_of_metadata_record(
                        institution_key='chief-directorate-oceans-and-coastal-research',
                        record_id=upload_result['id'],
                        state='published')
                if workflow_result['success']:
                    logger.info("Successfully updated state to published for record with ID {}".format(upload_result['id']))
                elif len(workflow_result['errors']) > 0:
                    workflow_errors = workflow_result['errors']
                    raise Exception("Errors when setting state for {} {} workflow errors {} validation errors {}".format(curr_sid, upload_result['id'], workflow_result['errors'], upload_result['errors']))
                else:
                    raise Exception("{}".format(workflow_result['errors']))

            except ODPException as e:
                logger.exception(f"{e}: {e.error_detail}")
                print(f"{e}: {e.error_detail}")
            except Exception as e:
                logger.exception(f"{e}")
                print(f"{e}")

