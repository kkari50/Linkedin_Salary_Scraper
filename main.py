from navigator import *
from database import *
import pandas as pd
from BingGeoCoding import *

logging.info(f'---------------Started Execution------------------')

driver = webdriver.Chrome(driver_path)
driver.get('https://www.linkedin.com/')

logging.info('Successfully loaded Linkedin Website.')

sign_in(driver, ln_username, ln_password)

time.sleep(random_time(3,5)) #waiting for few seconds to load the page
#open new window and navigate to Salary link

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(ln_salary_url)
time.sleep(random_time(3,5)) #waiting for few seconds to load the page
logging.info(f'Navigated to {ln_salary_url} webpage successfully.')

enter_salary_search_parameters(driver, search_title, search_location)
time.sleep(random_time(2,4)) #waiting for few seconds to load the page

logging.info('Web page successfully loaded')



try:
    see_results_by_company = driver.find_element_by_class_name('search-see-more-link')
    see_results_by_company.click()
    logging.info(f'Search Results by company selected')
    time.sleep(random_time(2,5)) #waiting for few seconds to load the page
except Exception as e:
    logging.info(f'Unable to click "See results by company element due to:": {e}')
    # driver.close()


# List of Company listing elements in the page


try:
    comp_obj_list = []
    page_count = 0
    while True:
        next_page_ele = driver.find_element_by_class_name('pagination__quick-link--next')
        comp_list = driver.find_elements_by_class_name('content-wrapper')
        counter = 1
        for comp in comp_list:
            comp_name = comp.find_element_by_class_name('title').text
            loc_name = comp.find_element_by_class_name('location').text
            compensation = comp.find_element_by_class_name('compensation').text
            salary_range = comp.find_element_by_class_name('range').text
            min_comp, max_comp = salary_range_parser(salary_range)
            comp_obj_list.append([comp_name, loc_name, compensation, min_comp, max_comp])
            counter = counter + 1

        print(f'Page {page_count} Completed. List Length: {len(comp_obj_list)}.')
        logging.info(f'Page {page_count} Completed. List Length: {len(comp_obj_list)}.')
        page_count += 1
        next_page_ele.click()
        time.sleep(random.randint(3, 5))



except NoSuchElementException:
    print("No clickable element found in Salary Scraping page. writing the details and exiting.")
#     print(salary_range)

logging.info(f'Total Scraped items: {len(comp_obj_list)}')

write_to_csv(comp_obj_list, output_file_path)

# driver.close()
logging.info(f'---------------Finished Execution------------------')

# print(comp_obj_list.head(5))
col_headers = ['Title', 'Location', 'Compensation', 'Min_Comp', 'Max_Comp']
df = pd.DataFrame(comp_obj_list)
df_2 = df.set_axis(col_headers, axis=1, inplace=False)
print(df_2.head(5))
print(df_2.columns)
database_handler(db_instance_name, db_name, db_scraped_data_table_name, df_2)



logging.info(f'Write to Database Successful.')

#--------------------------------Geo Coding for fetched area datapoints

location_tuple_list = get_location_data_from_db(db_scraped_data_table_name)

loc_list = [] #----location list used for actual geocodeing----
main_loc_dict = {}

for ele in location_tuple_list:
    loc_list.append(ele[0].replace("Greater", ""))
    main_loc_dict[ele[0]] = ele[0].replace("Greater", "")

final_output_dict={}
for src_loc,loc in main_loc_dict.items():
    output_data=get_location_data(loc,Bing_maps_API_key)
    final_output_dict[src_loc]=output_data

#--------------------------------Convert results into dataframe-----------

output_loc_df = convert_loc_results_to_DataFrame(final_output_dict)

#write to database:

database_handler(db_instance_name, db_name, db_location_data_table_name, output_loc_df)

print('location_data_write to database completed')

logging.info(f'Write to Database Location Data Successful.')