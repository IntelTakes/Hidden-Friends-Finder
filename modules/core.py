import time, json, operator, re
from progress.bar import IncrementalBar, Bar


from . import printer
from . import chrome
from . import elements

from selenium.webdriver.common.keys import Keys


# Login to facebook
def login(login,password,browser):

    printer.print_info("Logging in to facebook account...")
    try:
        browser.get("https://www.facebook.com/")
        elem = browser.find_element_by_id('email')
        elem.send_keys(login)
        elem = browser.find_element_by_id('pass')
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

    except:
        printer.print_bad("Something went seriously wrong during login - check internet connection and python configuration")
        browser.close()
        exit()

    try:
        login_test = get_elements(browser, **elements.recover)
        if len(login_test) == 0:
            printer.print_good("Login to facebook account ({}) successful".format(login))
        else:
            printer.print_bad("Login unsuccessful - check login and/or password")
            browser.close()
            exit()
    except Exception as e:
        printer.print_bad("Login test error: {}".format(e))

    return

def get_elements(browser, **kwargs):
        elements = browser.find_elements_by_xpath("//{}[@{}='{}']".format(kwargs['html'], kwargs['attribute'], kwargs['value']))
        return elements


def get_profile_name(browser):
    profile_name_elements = get_elements(browser, **elements.profile_name)
    name = profile_name_elements[0].text
    return name

def get_reactions(browser):
    # printer.print_info("Processing reactions")
    reaction_accounts = []
    reactions_links = get_elements(browser, **elements.reactions_link)

    bar = IncrementalBar('\033[1;37mProcessing reactions', fill='#', max=len(reactions_links), suffix='%(percent)d%%')
    for reaction_link in reactions_links:
        try:
            while reaction_link.is_displayed() == False:
                chrome.scroll_into_view(reaction_link, browser)
            browser.execute_script("arguments[0].click();", reaction_link)
            time.sleep(2)

            see_more = get_elements(browser, **elements.see_more)

            if len(see_more) > 0:
                chrome.scroll_into_view(browser, see_more[0])
                time.sleep(1)
                browser.execute_script("arguments[0].click();", see_more[0])
                time.sleep(1)

            reaction_profiles = get_elements(browser, **elements.reaction_profile)
            if len(reaction_profiles) == 0:
                time.sleep(5) #additional verification. Just in case code in pop-up window didn't load quickly enough.
                reaction_profiles = get_elements(browser, **elements.reaction_profile)

        except Exception as e:
                    printer.print_bad("Error while trying to collect reactions")
                    print(e)
                    pass

        try:
            for profile in reaction_profiles:
                if profile.text:
                    link = profile.find_element_by_tag_name("a")
                    user_data_json = link.get_attribute("data-gt")
                    user_data_dict = json.loads(user_data_json)
                    user_id = user_data_dict['engagement']['eng_tid']

                    account                = {}
                    account['Name']        = profile.text
                    account['Profile URL'] = "https://www.facebook.com/"+user_id
                    account['FB User ID']  = user_id

                    if account not in reaction_accounts:
                        reaction_accounts.append(account)

        except Exception as e:
                    print(e)
                    pass


        close_btn = get_elements(browser, **elements.close_button)
        while len(close_btn) == 0:
            time.sleep(1)
            close_btn = get_elements(browser, **elements.close_button)

        time.sleep(1)
        chrome.click_it(close_btn[0])
        bar.next()

    bar.finish()
    printer.print_good("Found {} unique profiles in reactions".format(len(reaction_accounts)))
    return reaction_accounts


def get_comments(browser):
    # printer.print_info("Collecting comments")
    comment_accounts = []
    comments_links = get_elements(browser, **elements.comments_link)

    bar = IncrementalBar('Processing comments', fill='#', max=len(comments_links), suffix='%(percent)d%%')
    # for i in range(len(comments_links)):
    for comment_link in comments_links:
        try:
            chrome.scroll_into_view(browser, comment_link)
            browser.execute_script("arguments[0].click();", comment_link)
            time.sleep(2)
            comment_profiles = get_elements(browser, **elements.comment)
        except Exception as e:
            print(e)
            pass
        bar.next()

    for profile in comment_profiles:
        try:
            regex = re.compile("id=[0-9]*")
            hovercard = profile.get_attribute("data-hovercard")
            r = regex.findall(hovercard)
            user_id = r[0][3:]
            account                = {}
            account['Name']        = profile.text
            account['Profile URL'] = "https://www.facebook.com/"+user_id
            account['FB User ID']  = user_id
            if account not in comment_accounts:
                comment_accounts.append(account)

        except Exception as e:
            print(e)
            pass


    bar.finish()
    printer.print_good("Found {} unique profiles in comments".format(len(comment_accounts)))
    return comment_accounts


def find_mutual_friends(browser, target, accounts):
    hidden_friends = []

    bar = IncrementalBar('\033[1;37mProcessing connections', fill='#', max=len(accounts), suffix='%(percent)d%%')

    for account in accounts:
        try:
            browser.get("https://www.facebook.com/browse/mutual_friends/?uid={}&node={}".format(target, account['FB User ID']))
            mutual_friends = get_elements(browser, **elements.mutual_friend)

            for bff in mutual_friends:
                link = bff.find_element_by_tag_name('a')
                user_data_json = link.get_attribute("data-gt")
                user_data_dict = json.loads(user_data_json)
                user_id        = user_data_dict['engagement']['eng_tid']

                friend                = {}
                friend['Name']        = link.text
                friend['Profile URL'] = "https://www.facebook.com/"+user_id
                friend['FB User ID']  = user_id

                if account not in hidden_friends:
                    hidden_friends.append(account)
        except Exception as e:
            print(e)

        bar.next()

    bar.finish()
    hidden_friends.sort(key=operator.itemgetter('Name'))
    printer.print_good("Found {} hidden friends".format(len(hidden_friends)))
    return hidden_friends
