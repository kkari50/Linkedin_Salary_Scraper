import os
import logging

#--------------------------------------------Linkedin Credentials-------------------------------------------------------
ln_username=''
ln_password = ''
ln_salary_url='https://www.linkedin.com/salary/'
search_title='Business Intelligence Analyst'
search_location = 'San Francisco Bay Area'
#---------------------------------------------Database Credentials------------------------------------------------------

db_instance_name='KRISHDELL'
# db_name = 'Linkedin_Salaries'
db_name = 'Linkedin_Salaries'

db_table_name='scraped_data'
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

