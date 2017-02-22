import zillow_web_scraper_client as client

print client.search_zillow_by_zip("94015")

print client.search_zillow_by_city_state("San Francisco", "CA")

print client.get_property_by_zpid(83154148)

print client.get_properties_by_zip(94080)

print client.get_properties_by_city_state('San Bruno', 'CA')

print client.get_similar_homes_for_sale_by_id(2096630311)
