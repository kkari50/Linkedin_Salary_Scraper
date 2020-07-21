from bingmaps.apiservices import LocationByAddress
from bingmaps.apiservices import LocationByQuery
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

key='ApfYnUrz5tx7XvHh4CLjKlMp0oPtkXHvWiQ-pGOb2BuJyMN9qQzjZbtyymRrCPQ2'

data = {'adminDistrict': 'Greater Seattle Area' ,
        'key': key}

loc_by_address = LocationByAddress(data)
# print(loc_by_address.response)

output=[{'addressLine': 'Seattle St',
         'adminDistrict': 'MA',
         'adminDistrict2': 'Suffolk County',
         'countryRegion': 'United States',
         'formattedAddress': 'Seattle St, Boston, MA 02134',
         'locality': 'Boston',
         'postalCode': '02134',
         'countryRegionIso2': 'US'}]

#
# data_2={'q': 'San Francisco Bay Area', 'key': key}
# data_2={'q': 'Greater Seattle Area', 'key': key}
data_2={'q': 'Nashville Metropolitan Area', 'key': key}
#
loc_by_query = LocationByQuery(data_2)
#
print(loc_by_query.get_address)

# response = loc_by_query.response
# print(response)
#
# for key, value in response.items():
#     print(key, value)

response = loc_by_query.get_address
print('-----------------------------------------------')
strOptions_formatted_address=[]
strOptions_locality=[]
for r in response:

    if r['countryRegion']=='United States':
        print(r)
        # str2Match=data_2['q']
        # strOptions=r['locality']
        # Ratios = process.extract(str2Match, strOptions)
        # print(Ratios)
        strOptions_formatted_address.append(r['formattedAddress'])
        if 'locality' in r.keys():
            strOptions_locality.append(r['locality'])




str2Match=data_2['q']
# strOptions=['Atlanta metropolitan area','Seattle']
Ratios = process.extract(str2Match, strOptions_formatted_address)
# print(Ratios)
for _ in strOptions_locality:
    locality_TokenSetRatio = fuzz.token_set_ratio(str2Match,_)
    print(f'{_}: {locality_TokenSetRatio}')

for val in strOptions_formatted_address:
    Token_Set_Ratio = fuzz.token_set_ratio(str2Match,val)
    print(f'{val}: {Token_Set_Ratio}')

# def dict_parser(d):
# {'adminDistrict': 'WA', 'adminDistrict2': 'King County', 'countryRegion': 'United States', 'formattedAddress': 'Seattle, WA', 'locality': 'Seattle', 'countryRegionIso2': 'US'}
# {'adminDistrict': 'GA', 'adminDistrict2': 'Fulton County', 'countryRegion': 'United States', 'formattedAddress': 'Atlanta metropolitan area, GA', 'locality': 'Atlanta metropolitan area', 'countryRegionIso2': 'US'}
