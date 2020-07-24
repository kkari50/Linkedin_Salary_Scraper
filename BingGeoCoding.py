from bingmaps.apiservices import LocationByAddress
from bingmaps.apiservices import LocationByQuery
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from database import *
from input_details import *
import time
import pandas




# 1.Fetch location data from database/excel file

def get_location_data_from_db(table_name):
    conn = get_data(db_instance_name, db_name)
    cursor = conn.cursor()
    q = f"select distinct (Location) from {table_name};"
    location_tuple_list = cursor.execute(q).fetchall()

    cursor.close()
    conn.close()

    return location_tuple_list


def get_location_data(location_name, api_key):
    data_dict = {'q': location_name, 'key': api_key}

    loc_by_query = LocationByQuery(data_dict)
    q_result_list = loc_by_query.get_address

    time.sleep(1)

    print(f'{location_name}: # of results:- {len(q_result_list)}')

    main_results_list = []
    for result in q_result_list:
        if 'countryRegionIso2' not in result.keys():
            result['countryRegionIso2'] = None
        if result['countryRegionIso2'] != 'US':
            continue
        else:
            result_index = q_result_list.index(result)
            q_f_address = result['formattedAddress']
            if 'locality' in result.keys():
                q_f_locality = result['locality']
            else:
                q_f_locality = None
            item_list = [result_index, data_2['q'], q_f_locality, q_f_address]
            main_results_list.append(item_list)
    #             print(item_list, result)

    pre_output_dict = {}
    for res_list in main_results_list:
        locality_TokenSetRatio = fuzz.token_set_ratio(res_list[1], res_list[2])
        f_address_TokenSetRatio = fuzz.token_set_ratio(res_list[1], res_list[3])
        pre_output_dict[res_list[0]] = [locality_TokenSetRatio, f_address_TokenSetRatio]

    # -------------------------------Filtering Based on Locality match score
    locality_score_list = []
    max_locality_score = 0
    max_locality_score_key = 0

    for key, val in pre_output_dict.items():
        locality_score = pre_output_dict[key][0]

        if locality_score > max_locality_score:
            max_locality_score = locality_score
            max_locality_score_key = key
        else:
            continue
    # -----------------------------Filtering original dict based on locality score
    filtered_pre_output_dict = {}
    for key, val in pre_output_dict.items():
        if pre_output_dict[key][0] == max_locality_score:
            filtered_pre_output_dict[key] = val
        else:
            continue
    #     print(filtered_pre_output_dict)

    # ------------------Get required index based on resulting f_address_score
    max_f_address_score = 0
    f_address_indices = []

    if max_locality_score == 0:
        used_output_dict = pre_output_dict
    else:
        used_output_dict = filtered_pre_output_dict

    for key, val in used_output_dict.items():
        f_address_score = used_output_dict[key][1]
        if f_address_score > max_f_address_score:
            max_f_address_score = f_address_score
            f_address_indices.append(key)
        else:
            continue

    min_index_for_max_f_address_score = f_address_indices[0]

    index_to_use = min_index_for_max_f_address_score
    required_data = q_result_list[index_to_use]
    print(f'{location_name} : {required_data}')
    print('------------------------------------------------------------')

    return required_data


def check_item_in_dict(item_name, search_dict):
    if item_name in search_dict.keys():
        return search_dict[item_name]
    else:
        return None


def convert_loc_results_to_DataFrame(final_output_dict):
    df_dict = {
        'location_name': [],
        'adminDistrict': [],
        'adminDistrict2': [],
        'countryRegion': [],
        'formattedAddress': [],
        'locality': [],
        'countryRegionIso2': []
    }

    for loc_q, res in final_output_dict.items():
        location_name = loc_q
        adminDistrict = check_item_in_dict('adminDistrict', res)
        adminDistrict2 = check_item_in_dict('adminDistrict2', res)
        countryRegion = check_item_in_dict('countryRegion', res)
        formattedAddress = check_item_in_dict('formattedAddress', res)
        locality = check_item_in_dict('locality', res)
        countryRegionIso2 = check_item_in_dict('countryRegionIso2', res)

        df_dict['location_name'].append(location_name)
        df_dict['adminDistrict'].append(adminDistrict)
        df_dict['adminDistrict2'].append(adminDistrict2)
        df_dict['countryRegion'].append(countryRegion)
        df_dict['formattedAddress'].append(formattedAddress)
        df_dict['locality'].append(locality)
        df_dict['countryRegionIso2'].append(countryRegionIso2)

        output_df = pd.DataFrame(df_dict)

        return output_df



















