import os
import logging

#--------------------------------------------Linkedin Credentials-------------------------------------------------------
ln_username=''
ln_password = ''
ln_salary_url='https://www.linkedin.com/salary/'
search_title=['Data Analyst','Data Scientist','Data Engineer','Business Analyst']
    #
search_location = ['New York Area','Houston, Texas Area','San Francisco Bay Area']
Bing_maps_API_key=''
#---------------------------------------------Database Credentials------------------------------------------------------

db_instance_name='KRISHDELL'
# db_name = 'Linkedin_Salaries'
db_name = 'Linkedin_Salaries'

db_scraped_data_table_name='scraped_data'
db_location_data_table_name='location_data'

db_uid ='KRISHDELL\krish'
db_password=''
db_AuthenticationMethod='Windows'

#---------------------------------------------Excel File Path-----------------------------------------------------------
dirname = os.path.dirname(__file__)
output_file_path = os.path.join(dirname,'Output.csv')

#---------------------------------------------Others----------------------------------------

driver_path=os.path.join(dirname,'chromedriver.exe')
ops_log_file_path = os.path.join(dirname,'operations.log')

logging.basicConfig(filename=ops_log_file_path,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

