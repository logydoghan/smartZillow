import json
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import zillow_web_scraper_client

from cloudAMQP_client import CloudAMQPClient

# RabbitMQ config
### REPLACE CLOUD_AMQP_URL WITH YOUR OWN ###
CLOUD_AMQP_URL = ''''''
DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'

# mongodb config
PROPERTY_TABLE_NAME = 'property'

FETCH_SIMILAR_PROPERTIES = True

SECONDS_IN_ONE_DAY = 3600 * 24
SECONDS_IN_ONE_WEEK = SECONDS_IN_ONE_DAY * 7

WAITING_TIME = 3

cloudAMQP_client = CloudAMQPClient(CLOUD_AMQP_URL, DATA_FETCHER_QUEUE_NAME)

def handle_message(msg):
    task = json.loads(msg)

    if (not isinstance(task, dict) or
        not 'zpid' in task or
        task['zpid'] is None):
        return

    zpid = task['zpid']

    # Scrape the zillow for details
    property_detail = zillow_web_scraper_client.get_property_by_zpid(zpid)
    # Add timestamp
    property_detail['last_update'] = time.time()

    # update doc in db
    db = mongodb_client.getDB()
    db[PROPERTY_TABLE_NAME].replace_one({'zpid': zpid}, property_detail, upsert=True)

    if FETCH_SIMILAR_PROPERTIES:
        # get its similar propertie's zpid
        similar_zpids = zillow_web_scraper_client.get_similar_homes_for_sale_by_id(zpid)

        # generate taslks for similar zpids
        for zpid in similar_zpids:
            old = db[PROPERTY_TABLE_NAME].find_one({'zpid': zpid})
            # Don't send task if the record is recent
            if (old is not None and
                'last_update' in old and
                time.time() - old['last_update'] < SECONDS_IN_ONE_WEEK):
                    continue
            cloudAMQP_client.sendDataFetcherTask({'zpid': zpid})


# Main thread
while True:
    # fetch a message
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getDataFetcherTask()
        if msg is not None:
            handle_message(msg)
        time.sleep(WAITING_TIME)
