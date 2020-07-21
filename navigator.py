import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from input_details import *
import time
import random
# import csv
import pandas as pd





# driver = webdriver.Chrome(driver_path)
# driver.get('https://www.linkedin.com/')

def random_time(start, end):
    return random.randint(start,end)

def sign_in(driver,username, password):
    delay=5
    try:
        driver.find_element_by_xpath('/html/body/nav/a[3]').click()
        time.sleep(random_time(3,5))

        username_ele = driver.find_element_by_id('username')
        pass_ele = driver.find_element_by_id('password')


        input_values(username_ele,username)
        logging.info('Login Username Entered.')
        input_values(pass_ele, password)
        logging.info('Login Password Entered.')

        submit_button = driver.find_element_by_class_name('login__form_action_container')
        submit_button.click()

        logging.info('Submitted Login information to Linkedin Server.')


        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        logging.info('Login Successful.')

    except Exception as e:
        logging.info(f'Login failed due to following exception: {e}')
        driver.close()



def input_values(ele, value):
    ele.click()
    ele.send_keys(Keys.CONTROL,'a')
    ele.send_keys(value)

def enter_salary_search_parameters(driver, title, location):
    try:
        logging.info(f'Started entering Search parameters for Salaries: {title,location}')
        search_by_title_ele = driver.find_element_by_class_name('typeahead-keyword')
        search_by_loc_ele = driver.find_element_by_class_name('typeahead-location')

        input_values(search_by_title_ele, title)
        logging.info(f'{title} entered')
        input_values(search_by_loc_ele, location)
        logging.info(f'{location} entered')

        search_by_loc_ele.send_keys(Keys.ENTER)
        time.sleep(random_time(2,5))
        search_by_loc_ele.send_keys(Keys.ENTER)


        submit_button_ele = driver.find_element_by_class_name('search-salary-button')
        submit_button_ele.click()

        logging.info('Submit button clicked.')

    except Exception as e:

        logging.info(f'Salary Search parameters Entering Failed due to: {e}')
        driver.close()

def salary_range_parser(range_str):
    l=range_str.replace('Range: $','').replace('$','').replace(' ','').replace(',','').partition('-')
    min_comp = l[0]
    max_comp = l[2]
    return (min_comp,max_comp)

def write_to_csv(job_list, file_name):
   # print(job_list)
   #  col_headers=['Title', 'Location', 'Compensation', 'Min_Comp', 'Max_Comp']
    df = pd.DataFrame(job_list)

    df.to_csv(file_name,index=False, mode='a', header=False)





# driver.close()
