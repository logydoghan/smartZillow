import zillow_api_client as client

print client.getSearchResults('65 Norfolk St UNIT 4', 'San Francisco, CA')

print client.getUpdatedPropertyDetails("15622377")

print client.getComps('15622377', 2)

print client.getCompsZpids('15622377')