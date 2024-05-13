import json
from selenium import webdriver
from modules.login import login
from modules.search import search_profiles, google_search

with open('config.json') as config_file:
    config = json.load(config_file)


options = webdriver.EdgeOptions()
if config['options']['headless-mode']:
    options.add_argument('--headless')


driver = webdriver.Edge(options=options)


username = config['user']['username']
password = config['user']['password']
cookies_support = config['options']['cookies-support']


company = config['parameters']['company']
title = config['parameters']['title']
location = config['parameters']['location']

skip_check = config['options']['skip-checker']
company_location = config['parameters']['company-location']
name = config['parameters']['name']
surname = config['parameters']['surname']




if name != "" and surname != "":
    login(driver, username, password, cookies_support)
    search_profiles(driver, company, company_location, name, surname, location, title, skip_check)
else:
    google_search(driver, company, title, location)


driver.quit()
