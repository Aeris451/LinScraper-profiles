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
cookies_support = config['options']['cookies-support']
gsearch = config['options']['google-search']

if gsearch:
    driver.get('https://www.google.com/search?q=test')
    if "google.com/sorry" in driver.current_url:
        print(input("Captcha detected, confirm solving with enter"))

login(driver, username, password, cookies_support)
search_profiles(driver, config)



driver.quit()
