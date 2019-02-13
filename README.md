# Hidden-Friends-Finder
Hidden Friends Finder (HFF) for Facebook

Program automates search for friends of targed profile based on facebook graph search method.

After launch program runs in ... phases:

### INPUT PHASE
Facebook login: *[email you use to login to facebook]*

Facebook password: [no need to explain]

Target user ID: [Facebook user ID in numerical format]

### TESTING PHASE
Program will automaticly scroll trough facebook profile in order to reveal all posts and comments. 
At the same time it will test most important elements of facebook code. Reason is, facebook changes classes and names of html elements quite frequently. In that case program will let you know that code was chenged. You will have to add new values to file modules/elements.py.

### GATHERING DATA 
HFF will try to gather as much data as possible. It will collect all comments and reactions on profile.

### ANALYSING DATA
HFF will run analysis based on graph search for every account gathered in previus step. 
