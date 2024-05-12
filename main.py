import json
from selenium import webdriver
from modules.login import login
from modules.search import search_profiles

with open('config.json') as config_file:
    config = json.load(config_file)


options = webdriver.EdgeOptions()
if config['options']['headless-mode']:
    options.add_argument('--headless')


driver = webdriver.Edge(options=options)

username = config['user']['username']
password = config['user']['password']
cookiesSupport = config['options']['cookies-support']

login(driver, username, password, cookiesSupport)
search_profiles(driver, config)






driver.quit()
