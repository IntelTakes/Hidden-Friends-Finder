# Hidden-Friends-Finder
Hidden Friends Finder (HFF) for Facebook

The program automates the search of friends of targeted profile based on facebook graph search method.

## Run:
`$ python HFF.py`

`$ python HFF.py -l [login email] -p [password to facebook] -t [target Facebook ID]`

After the launch program runs in 5 phases:

### INPUT PHASE (if no options in run command)
Facebook login: *[email you use to login to facebook]*

Facebook password: [no need to explain]

Target user ID: [Facebook user ID in numerical format]

### TESTING PHASE
The program automatically scrolls through a Facebook profile to reveal all posts and comments. 
At the same time, it tests the most critical elements of the Facebook code. The reason is, facebook changes classes and names of HTML elements quite frequently. In that case, the program lets you know about changes. You have to add new values to file modules/elements.py.

### GATHERING DATA 
HFF tries to gather as much data as possible. It collects all comments and reactions on a profile.

### ANALYSING DATA
HFF runs analysis based on graph search for every account gathered in the previous step. 

### PRINTING DATA
Results are save to two CSV files.

File Name  | Description
------------- | -------------
[target_username]-confirmed-friends.csv  | Profiles found using graph search.
[target_username]-unconfirmed-friends.csv  | Profiles collected during data collecting phase, not confirmed by graph search.
