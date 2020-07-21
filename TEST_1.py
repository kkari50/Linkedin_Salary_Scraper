import requests
from UserAgents import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver_path = "C:\\Users\\krish\\Desktop\\PythonProjects\\Linkedin_Salaries\\chromedriver.exe"

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get('https://www.linkedin.com')

