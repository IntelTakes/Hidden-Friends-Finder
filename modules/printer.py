import codecs, csv
from . import core

author = 'Musafir.py'
version = '1.0'

# Console colors
W = '\033[1;0m'   # white
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G,R,B,P,C,O,GR]

info = '{0}[*]{1} '.format(B,GR)
ques =  '{0}[?]{1} '.format(C,GR)
bad = '{0}[-]{1} '.format(R,GR)
good = '{0}[+]{1} '.format(G,GR)


def print_art():

    print("""
    {}¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
    ¶¶¶¶¶¶¶{}____{}¶¶¶¶
    ¶¶¶¶¶¶{}___{}¶¶¶¶¶¶
    ¶¶¶¶{}_______{}¶¶¶¶
    ¶¶¶¶¶¶{}___{}¶¶¶¶¶¶
    ¶¶¶¶¶¶{}___{}¶¶¶¶¶¶ {}HIDDEN{}
    ¶¶¶¶¶¶{}___{}¶¶¶¶¶¶ {}FRIENDS{}
    ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ {}FINDER {}
    by {}{}
    """.format(B,W,B,W,B,W,B,W,B,W,
               B,W,B,W,B,W,B,W,version,author,GR))


def print_banner(text):
    print('{1}[ {2}{0}{1} ]'.format(text, G, C))

def print_info(text):
    print(info + text)

def print_ques(text):
    print(ques + text)

def print_good(text):
    print(good + text)

def print_bad(text):
    print(bad + text)


def save_friends(browser, name, friends_list, category):
    try:
        print_info("Writing to file {}-{}-friends.csv".format(name, category))

        headers = ["Name","FB User ID","Profile URL",]
        with open("{}-{}-friends.csv".format(name, category),"w") as fd:
            spreadsheet = csv.DictWriter(fd,fieldnames=headers)
            spreadsheet.writeheader()
            for friend in friends_list:
                spreadsheet.writerow(friend)
    except Exception as e:
        print_bad("Error when writing to file: {}".format(e))
        pass
    print_good("Task completed! {} {} friends found and saved".format(len(friends_list), category))

    return
