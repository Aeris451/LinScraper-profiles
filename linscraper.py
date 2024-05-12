import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

import json

with open('config.json') as config_file:
    config = json.load(config_file)

with open(r'C:\Users\aeris\PycharmProjects\mail-lookup\output\config.json') as config_file:
    configLookup = json.load(config_file)

username = config['user']['username']
password = config['user']['password']

company = config['parameters']['company']
companyLocation = config['parameters']['companyLocation']
name = configLookup['parameters']['name']
surname = configLookup['parameters']['surname']
title = config['parameters']['title']
if title != "":
    title = f"&titleFreeText={title}"

location = config['parameters']['location']

options = webdriver.EdgeOptions()
#options.add_argument('--headless')
driver = webdriver.Edge()

driver.get('https://www.linkedin.com/uas/login')
uname = driver.find_element(By.ID, "username")
uname.send_keys(username)
pword = driver.find_element(By.ID, 'password')
pword.send_keys(password)


#driver.find_element(By.XPATH, "//button[@type='submit']").click()


input("Press enter after you log in")



if company != "":
    driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={company}%20{companyLocation}&origin=GLOBAL_SEARCH_HEADER&sid=M%3Ay")
    source = driver.page_source
    page = bs(source, 'lxml')
    div = page.find('div', {'data-chameleon-result-urn': True})
    urn_value = div['data-chameleon-result-urn']
    companyId = urn_value.split(':')[-1]
    companyId = f"currentCompany=%5B%22{companyId}%22%5D&"
else:
    companyId = ""





driver.get(f"https://www.linkedin.com/search/results/people/?{companyId}%22%5D&keywords={name}%20{surname}%20{location}&origin=GLOBAL_SEARCH_HEADER&sid=pp3{title}")


input("Check if the parameters are correct and press enter")

source = driver.page_source
page = bs(source, 'lxml')

profile_data = []

def collection(page):
    profiles = page.find_all('li', class_='reusable-search__result-container')
    for profile in profiles:
        name_tag = profile.find('span', class_='entity-result__title-text').find('span', {'aria-hidden': 'true'})
        if name_tag:
            name = name_tag.get_text().strip()
            profile_link = profile.find('a', class_='app-aware-link scale-down').get('href')
        else:
            name = "Name not found"
            profile_link = ""

        subtitle = profile.find('div', class_='entity-result__primary-subtitle')
        if subtitle:
            headline = subtitle.get_text().strip()
        else:
            headline = "Headline not found"

        location = profile.find('div', class_='entity-result__secondary-subtitle')
        if location:
            location_text = location.get_text().strip()
        else:
            location_text = "Location not found"



        profile_data.append({'Name': name, 'Headline': headline, 'Location': location_text, 'Link': profile_link})



collection(page)

while True:
    try:
        next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
        if next_button.is_enabled():
            next_button.click()
            time.sleep(5)
            source = driver.page_source
            page = bs(source, 'lxml')
            collection(page)
        else:
            print("Next button is disabled. Exiting loop.")
            break
    except:
        break

# Printing collected data
print("Number of collected profiles:", len(profile_data))
for profile in profile_data:
    print(profile)

# Creating DataFrame and saving to CSV
data = pd.DataFrame(profile_data)
current_directory = os.getcwd()
data.to_csv(os.path.join(current_directory, 'output_profiles.csv'))
