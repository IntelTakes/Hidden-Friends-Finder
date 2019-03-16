import platform, os, time, sys
from tqdm import tqdm

from . import printer
from . import core
from . import tests
from . import elements

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def setup():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    options.add_argument("--log-level=3")

    current_path = os.path.dirname(os.path.realpath(__file__))

    os_check = platform.system()
    if "Darwin" in os_check:
        chromedrive_check = os.path.isfile(current_path + "/chromedriver")
        if not chromedrive_check:
            printer.print_bad("Missing Mac OS chromedriver or damaged file.")
            exit()
        os.chmod(current_path + "/chromedriver", 0o775)
        chromedriver = current_path + '/chromedriver'

    elif "Win" in os_check:
        chromedrive_check = os.path.isfile(current_path + "/chromedriver.exe")
        if not chromedrive_check:
            printer.print_bad("Missing Windows chromedriver or damaged file.")
            exit()
        chromedriver = current_path + '/chromedriver.exe'
    else:
        printer.print_bad("Driver for your system is not included. Add driver manualy and modify code in chrome.py file")
        exit()

    browser = webdriver.Chrome(executable_path=chromedriver, options=options)
    return browser


def scroll_page(browser, target):

    url = "https://www.facebook.com/{}".format(target)
    errors = []
    browser.get(url)
    time.sleep(5)

    try:
        profile_name = core.get_profile_name(browser)
        tests.profile_prompt(browser, profile_name, target)
        printer.print_info("Data verification in progress. It might take a while... ".format(profile_name))
    except Exception as e:
        printer.print_bad("Cannot open profile page. Error message: {}. Are you sure user ID is correct? Please check and start again.".format(e))
        browser.close()
        exit()

    tests.test_elements(browser, elements.post)

    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(2)

    posts_after_scrolling = len(core.get_elements(browser, **elements.post))

    t = tqdm(ncols=0)
    while True:
        posts_before_scrolling = posts_after_scrolling
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(4)
        posts_after_scrolling = len(core.get_elements(browser, **elements.post))
        browser.execute_script("window.scrollTo(0,0);")
        t.update()

        if posts_after_scrolling <= posts_before_scrolling:
            if len(core.get_elements(browser, **elements.spinner)) > 0:
                spinners = core.get_elements(browser, **elements.spinner)
                for spinner in spinners:
                    scroll_into_view(browser, spinner)
                    time.sleep(3)
            else:
                errors = tests.test_elements(browser, elements.reactions_link, elements.comment)
                break
    t.close()
    printer.print_info("Completed. Verified {} posts with {} errors.".format(posts_after_scrolling, len(errors)))
    return errors


def scroll_into_view(browser, element):
    scroll = ActionChains(browser).move_to_element(element)
    scroll.perform()
    return

def click_it(element):
    n = 1
    while n < 5:
        try:
            time.sleep(1)
            element.click()
            time.sleep(1)
            break
        except Exception as e:
            printer.print_bad("Error when clicking {}".format(element.text))
            time.sleep(5)
            n += 1
            continue
