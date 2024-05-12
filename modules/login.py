import os
import pickle
from selenium.webdriver.common.by import By
import time




def login(driver, username, password, cookies_support):

    driver.get('https://www.linkedin.com/uas/login')


    cookies_file = 'cookies.pkl'
    try:
        if cookies_support and os.path.exists(cookies_file):
            print("Cookies file found. Logging in using cookies...")
            with open(cookies_file, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
        else:
            raise FileNotFoundError
    except (FileNotFoundError, Exception):
        print("Cookies file not found or invalid. Logging in using username and password...")


        uname = driver.find_element(By.ID, "username")
        uname.send_keys(username)
        pword = driver.find_element(By.ID, 'password')
        pword.send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def check_page():
        return "https://www.linkedin.com/feed/" in driver.current_url

    while not check_page():
        time.sleep(5)

    if cookies_support and not os.path.exists(cookies_file):
        cookies = driver.get_cookies()
        with open(cookies_file, 'wb') as file:
            pickle.dump(cookies, file)