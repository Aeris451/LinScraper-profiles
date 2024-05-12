# LinScraper-profiles
### Tool that allow you to gather a list of users by name, surname, company, locations and titles. 

**This tool is for EDUCATIONAL purposes only.**

## Features
* Gather a list of users with their names, positions, companies, locations and a link to their profile.
* Save results to CSV

## Getting Started
1. `git clone https://github.com/Aeris451/LinScraper-profiles.git`
2. `cd LinScraper-profiles`
3. `pip install -r requirements.txt`
4. `set up config.json`
5. `python3 main.py or python main.py`


## Authorizing LinkedIn and parameters
In order to use LinkedIn search, you must authenticate with a credentials. 
* Put your credentials in config.json with search parameters.
* The program saves cookies after the first login, so you don't have to put them in a json file and enter them manually after the first run only once.

## Usage
* If login credentials and cookies were correct login should happen automatically, you may be asked to solve captcha or MFA(cookies saver prevents this, but they sill may ask you for password). After a successful login, confirm it with enter. 
* Now the program should find the id of the company based on its name and location, and then it will proceed to search for people based on the parameters given in config.json, at this point the program will stop so you can check and modify the entered data. If everything matches, you can press enter and let the program scrape the search results, if there are too many pages, just turn off the selenium window and the program will save only the data it has collected so far.

## Options 
* Skip the parameter validation. (“skip-checker”: false) 
* You can use headless mode but only if you are sure you won't have to do captcha, and you don't have MFA enabled. I don't reccomend using it when google-search is enabled, because of captcha. ("headless-mode": true)
* Disable cookie saving and log in with credentials every time. ("cookies-support": false)
* Experimental google search, if you leave it on, then any person who showed up without a name and link would be searched on google and compared to the results based on similarity. ("google-search:" true)

