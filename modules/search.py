import threading
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import os


def google_search(driver, company, title, location):

    search_query = f"{company} {title} {location} site:linkedin.com/in/"
    driver.get(f'https://www.google.com/search?q={search_query}')
    if "google.com/sorry" in driver.current_url:
        print(input("Captcha detected, confirm solving with enter"))

    def scroll(driver):
        while not stop_event.is_set():
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def wait_for_enter():
        global stop_event
        stop_event = threading.Event()
        scroll_thread = threading.Thread(target=scroll, args=(driver,))
        scroll_thread.start()
        input("Press Enter to stop scrolling: ")
        stop_event.set()
        scroll_thread.join()

    wait_for_enter()

    soup = bs(driver.page_source, 'html.parser')
    h3_tags = soup.find_all('h3')
    profile_data = []
    for h3_tag in h3_tags:
        if "-" not in h3_tag.get_text() and " – " not in h3_tag.get_text():
            continue

        if "-" in h3_tag.get_text():
            name_parts = h3_tag.get_text().split("-", 1)
        else:
            name_parts = h3_tag.get_text().split("–", 1)

        if name_parts[0].count(" ") != 2:
            continue

        # To correct
        parent_div = h3_tag.find_parent('div')
        link = parent_div.find('a').get('href')
        if parent_div:
            jump_div = parent_div.find_parent().find_parent().find_parent().find_parent().find_parent()
            if jump_div:
                second_divs = jump_div.find_all('div')
                span_tag = second_divs[25].find('span')
                if span_tag:
                    location_text = span_tag.get_text().strip()
                    profile_data.append({'Name': name_parts[0], 'Info': location_text, 'Link': link})

    print("Number of collected profiles:", len(profile_data))
    for profile in profile_data:
        print(profile)

    # Creating DataFrame and saving to CSV
    data = pd.DataFrame(profile_data)
    current_directory = os.getcwd()
    data.to_csv(os.path.join(current_directory, 'output_profiles.csv'))








def search_profiles(driver, company, company_location, name, surname, location, title, skip_check):



    if title != "":
        title = f"&titleFreeText={title}"



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


            profile_data.append({'Name': name, 'Headline': headline, 'Location': location_text, 'Link': profile_link})

    collection(page)

    while True:
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
            if next_button.is_enabled():
                next_button.click()
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
