# Hidden Friends Finder (HFF) for Facebook ![](http://i66.tinypic.com/15zgv4.png) 

HFF automates search for friends of targeted profile based on graph search method. It's designed as OSINT tool for online investigations (not stalking your ex :wink:). Depends on profile activity and privacy settings it can "extract" from 30% to 90% of private friends list.

### _Requirements_:
- Python 3 plus additional libraries: Click, tqdm, Requests. (check requirements.txt) 

- Chrome browser installed. Selenium headless webdriver is included for Windows and MacOS. HFF checks for OS type and choose correct driver.

- Target profile must have at least one post and one comment or reaction visible publicly.

- Only works with english version of Facebook so check your language settings.

- HFF works much better on accounts where "friends list" visibility is set to - "only friends" (most cases). Privacy setting "only me" works as well but returns fewer accounts. 

_____
### RUN:
`$ python HFF.py`
or
`$ python HFF.py -l [login email] -p [password to facebook] -t [target Facebook ID]`

After the launch program runs in 5 phases:


#### INPUT PHASE (if no options given with run command):
Facebook login: *[email you use to login to facebook]*

Facebook password: *[no need to explain]*

Target user ID: *[Facebook user ID in numerical format]*  (you can find one easily here: [Findmyfbid.in](https://findmyfbid.in/)) 


#### VERIFYING DATA:
The program automatically scrolls through a Facebook profile to reveal all posts and comments. 
At the same time, it tests the most critical elements of the Facebook code. The reason is, facebook changes classes and names of HTML elements quite frequently. In that case, program lets you know about changes and ask to edit values in file modules/elements.py.


#### GATHERING DATA:
HFF tries to gather as much data as possible. It collects all comments and reactions on a profile.


#### ANALYSING DATA:
HFF runs analysis based on graph search for every account gathered in the previous step. 


#### PRINTING DATA:
Results are save to two CSV files.

File Name  | Description
------------- | -------------
[target_username]-confirmed-friends.csv  | Profiles found and confirmed using graph search.
[target_username]-unconfirmed-friends.csv  | Profiles collected during data collecting phase, not confirmed by graph search.
