import requests

from json import dumps
from json import loads
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

ZILLOW_ENDPOINT = 'http://www.zillow.com/webservice'

GET_SEARCH_RESULTS_API_NAME = 'GetSearchResults.htm'
GET_UPDATED_PROPERTY_DETAILS_API_NAME = 'GetUpdatedPropertyDetails.htm'
GET_COMPS_API_NAME = 'GetComps.htm'

### REPLACE ZWS_ID WITH YOUR OWN ###
ZWS_ID = ''

def build_url(api_name):
    return '%s/%s' % (ZILLOW_ENDPOINT.strip('/'), api_name.strip('/'))

""" Doc: http://www.zillow.com/howto/api/GetSearchResults.htm """
def getSearchResults(address, citystatezip, rentzestimate=False):
    payload = {'zws-id': ZWS_ID, 
               'address': address,
               'citystatezip': citystatezip,
               'rentzestimate': rentzestimate}
    response = requests.get(build_url(GET_SEARCH_RESULTS_API_NAME), params=payload)
    res_json = loads(dumps(bf.data(fromstring(response.text))))

    # Extract info from response.
    for key in res_json:
        if (res_json[key] is not None and
            res_json[key]['response'] is not None and
            res_json[key]['response']['results'] is not None):
            return res_json[key]['response']['results']['result']
    else:
        return {}

"""
    WARN: a lot of updated details are not accessable through this API.
    Doc: http://www.zillow.com/howto/api/GetUpdatedPropertyDetails.htm
"""
def getUpdatedPropertyDetails(zpid):
    payload = {'zws-id': ZWS_ID, 
               'zpid': zpid}
    response = requests.get(build_url(GET_UPDATED_PROPERTY_DETAILS_API_NAME), params=payload)
    res_json = loads(dumps(bf.data(fromstring(response.text))))

    # TODO: extract ino from response
    return res_json

""" Doc: http://www.zillow.com/howto/api/GetComps.htm """
def getComps(zpid, count=25, rentzestimat=False):
    payload = {'zws-id': ZWS_ID,
               'zpid': zpid,
               'count': count,
               'rentzestimat': rentzestimat}
    response = requests.get(build_url(GET_COMPS_API_NAME), params=payload)
    res_json = loads(dumps(bf.data(fromstring(response.text))))

    return res_json

"""
    Extract zpids from getComps result.
    Doc: http://www.zillow.com/howto/api/GetComps.htm
"""
def getCompsZpids(zpid, count=25, rentzestimat=False):
    payload = {'zws-id': ZWS_ID,
               'zpid': zpid,
               'count': count,
               'rentzestimat': rentzestimat}
    response = requests.get(build_url(GET_COMPS_API_NAME), params=payload)
    res_json = loads(dumps(bf.data(fromstring(response.text))))
    comp_zpids = [x['$'] for x in list(gen_dict_extract('zpid', res_json))]
    return comp_zpids

""" Helper method to extract all values from a nested json. """
def gen_dict_extract(key, var):
    if hasattr(var,'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result