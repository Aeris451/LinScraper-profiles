# LinScraper-profiles
### Tool that allows you to gather a list of users from LinkedIn

**This tool is for EDUCATIONAL purposes only.**

#Requires Edge

## Features
* Gather a list of users with their names, positions, companies, locations and a link to their profile.
* Save results to CSV
* The program itself chooses between the Google and LinkedIn search engines. If the name or surname is provided, the program will search on Linkedin, and if there is only the company name, it will search on Google. This was done to avoid hiding usernames on LinkedIn. However, a Google search provides less information than a LinkedIn search.

## Getting Started
1. `git clone https://github.com/Aeris451/LinScraper-profiles.git`
2. `cd LinScraper-profiles`
3. `pip install -r requirements.txt`
4. `set up config.json`
5. `python3 main.py or python main.py`


## Authorizing LinkedIn and parameters
To use LinkedIn search, you must authenticate with a credentials. 
* Put your credentials in config.json with search parameters.
* The program saves cookies after the first login, so you don't have to put them in a json file and enter them manually after the first run only once.

## Usage (LinkedIn search case, if you provided name or surname)
* If login credentials and cookies were correct login should happen automatically, you may be asked to solve captcha or MFA (cookie saver prevents this, but they still may ask you for password). After a successful login, confirm it with enter. 
* Now the program should find the id of the company based on its name and location. Then it will proceed to search for people based on the parameters given in config.json, at this point the program will stop, so you can check and modify the entered data. If everything matches, you can press enter and let the program scrape the search results, if there are too many pages, turn off the selenium window and the program will save only the data it has collected so far.

## Usage (Google search case, if you are not provided name or surname)
* A Google search only retrieves the company name, location and job title. The program will scroll down, and you need to press the more results button. If you have collected enough data, click enter in the console to save it.
* Google may require the captcha to be solved, in which case it should be solved and confirmed with enter in the console, after which the program will return to operation.
  
## Options 
* Skip the parameter validation. (“skip-checker”: false) 
* You can use headless mode but only if you are sure you won't have to do captcha, and you don't have MFA enabled. I don't recommend using it when google-search is enabled, because of captcha. ("headless-mode": true)
* Disable cookie saving and log in with credentials every time. ("cookies-support": false)
