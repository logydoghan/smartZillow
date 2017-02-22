import json
import operations
import os
import pyjsonrpc
import sys
import time

from bson.json_util import dumps

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import ml_prediction_client
import mongodb_client
import zillow_api_client
import zillow_web_scraper_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'
PROPERTY_TABLE_NAME = 'property'

"""Search a property with specific address and citystatezip"""
def searchByAddress(address, citystatezip):
    res = zillow_api_client.getSearchResults(address, citystatezip)
    print res
    return res

"""Search properties by zip code"""
def searchAreaByZip(zipcode):
    properties = findProperyByZipcode(zipcode)
    if len(properties) == 0:
        properties = zillow_web_scraper_client.search_zillow_by_zip(zipcode)
    print properties
    return properties

"""Search properties by city and state"""
def searchAreaByCityState(city, state):
    res = zillow_web_scraper_client.search_zillow_by_city_state(city, state)
    print res
    return res

"""Search properties in an area"""
def searchArea(text):
    zpids = []
    if text.isdigit():
        zpids = searchAreaByZip(text)
    else:
        city = text.split(',')[0].strip()
        state = text.split(', ')[1].strip()
        zpids = searchAreaByCityState(city, state)
    print zpids
    res = []
    update_list = []
    db = mongodb_client.getDB()
    for zpid in zpids:
        record = db[PROPERTY_TABLE_NAME].find_one({'zpid': zpid})
        if record != None:
            res.append(record)
        else:
            property_detail = getDetailsByZpid(zpid, False)
            res.append(property_detail)
            update_list.append(property_detail)

    storeUpdates(update_list)

    # Trick: use bson.dumps then re-construct json because of ObjectId.
    return json.loads(dumps(res))

"""
Retrieve details by zillow property ID (zpid)
If get_predction is True, get value prediction from ml_prediction_service
"""
def getDetailsByZpid(zpid, get_prediction=False):
    db = mongodb_client.getDB()
    prop = json.loads(dumps(db[PROPERTY_TABLE_NAME].find_one({'zpid': zpid})))
    if prop == None:
        prop = zillow_web_scraper_client.get_property_by_zpid(zpid)

    # Get prediction
    if get_prediction:
        predicted_value = ml_prediction_client.predict(
            prop['zipcode'],
            prop['property_type'],
            prop['bedroom'],
            prop['bathroom'],
            prop['size'])
        prop['predicted_value'] = int(predicted_value)
    return prop

"""Update doc in db"""
def storeUpdates(properties):
    db = mongodb_client.getDB()

    for property_detail in properties:
        print property_detail
        zpid = property_detail['zpid']
        property_detail['last_update'] = time.time()
        db[PROPERTY_TABLE_NAME].replace_one({'zpid': zpid}, property_detail, upsert=True)


"""Search property by zipcode"""
def findProperyByZipcode(zipcode):
    db = mongodb_client.getDB()
    properties = list(db[PROPERTY_TABLE_NAME].find({'zipcode': zipcode, 'is_for_sale': True}))
    return [x['zpid'] for x in properties]
