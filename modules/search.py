import difflib
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import time
import os


def google_search(company, headline, location, driver):
    search_query = f"{company} {headline} {location} site:linkedin.com"
    driver.execute_script(f"window.open('https://www.google.com/search?q={search_query}', 'new window')")
    driver.switch_to.window(driver.window_handles[1])
    if "google.com/sorry" in driver.current_url:
        print(input("Captcha detected, confirm solving with enter"))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = bs(driver.page_source, 'html.parser')
    h3_tags = soup.find_all('h3')
    max_similarity = 0
    best_name = ""
    best_link = ""

    for h3_tag in h3_tags:
        if "-" not in h3_tag.get_text() and " – " not in h3_tag.get_text():
            continue


        if "-" in h3_tag.get_text():
            name_parts = h3_tag.get_text().split("-", 1)
        else:
            name_parts = h3_tag.get_text().split("–", 1)

        if name_parts[0].count(" ") != 2:
            continue

        link = h3_tag.find_parent('a')['href']


        parent_div = h3_tag.find_parent('div')
        if parent_div:
            jump_div = parent_div.find_parent().find_parent().find_parent().find_parent()
            if jump_div:

                all_span_tags = jump_div.find_all('span')
                for span_tag in all_span_tags:
                    span_text = span_tag.get_text()
                    similarity = difflib.SequenceMatcher(None, location.lower(), span_text.lower()).ratio() * 100
                    if similarity >= 2:
                        if similarity > max_similarity:
                            max_similarity = similarity
                            best_name = name_parts[0]+"???"
                            best_link = link


    if max_similarity > 0:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return best_name, best_link
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return None, None




def search_profiles(driver, config):

    gsearch = config['options']['google-search']
    skip_check = config['options']['skip-checker']
    company = config['parameters']['company']
    company_location = config['parameters']['company-location']
    name = config['parameters']['name']
    surname = config['parameters']['surname']
    title = config['parameters']['title']
    if title != "":
        title = f"&titleFreeText={title}"

    location = config['parameters']['location']

    if company != "":
        driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={company}%20{company_location}&origin=GLOBAL_SEARCH_HEADER&sid=M%3Ay")
        source = driver.page_source
        page = bs(source, 'lxml')
        div = page.find('div', {'data-chameleon-result-urn': True})
        urn_value = div['data-chameleon-result-urn']
        company_id = urn_value.split(':')[-1]
        company_id = f"currentCompany=%5B%22{company_id}%22%5D&"
    else:
        company_id = ""

    driver.get(f"https://www.linkedin.com/search/results/people/?{company_id}%22%5D&keywords={name}%20{surname}%20{location}&origin=GLOBAL_SEARCH_HEADER&sid=pp3{title}")

    if(skip_check):
        print("skipping check")
    else:
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

            if name == "Name not found" and gsearch:
                name, profile_link = google_search(company, headline, location_text, driver)

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


    input("stop")
    # Printing collected data
    print("Number of collected profiles:", len(profile_data))
    for profile in profile_data:
        print(profile)

    # Creating DataFrame and saving to CSV
    data = pd.DataFrame(profile_data)
    current_directory = os.getcwd()
    data.to_csv(os.path.join(current_directory, 'output_profiles.csv'))
