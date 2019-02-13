import platform, os, zipfile, time, sys

from . import printer
from . import core
from . import tests
from . import elements

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Check if webdriver is installed and if not install it.
def install_webdriver():
    current_path = os.path.dirname(os.path.realpath(__file__))
    chromedrive_check = os.path.isfile(current_path + "/chromedriver")

    if chromedrive_check:
        os.chmod(current_path + "/chromedriver", 0o775)
        printer.print_good("Webdriver already installed")
        return

    printer.print_info("Downloading chrome headless...")
    url = "https://chromedriver.storage.googleapis.com/2.45/"

    os_check = platform.platform()
    if 'Darwin' in os_check:
        url += "chromedriver_mac64.zip"
    elif 'Win' in os_check:
        url += "chromedriver_win32.zip"
    elif 'Linux' in os_check:
        url += "chromedriver_linux64.zip"
    else:
        url += "chromedriver_linux64.zip"

    r = requests.get(url, allow_redirects=True)
    open(current_path + "/chromedriver.zip", 'wb').write(r.content)

    with open(current_path + '/chromedriver.zip', 'rb') as f:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            z.extract(name, current_path)

    os.chmod(current_path + "/chromedriver", 0o775)

# Setup browser
def setup():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-notifications")

    current_path = os.path.dirname(os.path.realpath(__file__))
    chromedrive_check = os.path.isfile(current_path + "/chromedriver")
    if not chromedrive_check:
        raise ValueError("Something wrong with chromedriver path")

    chromedriver = current_path + '/chromedriver'
    browser = webdriver.Chrome(executable_path=chromedriver, options=options)

    return browser

#Scroll down to open full facebook wall page
def scroll_page(browser, target):

    url = "https://www.facebook.com/{}".format(target)
    errors = []
    browser.get(url)
    time.sleep(5)

    try:
        profile_name = core.get_profile_name(browser)
        printer.print_info("Scrolling trough the profile page of {}. It might take a while...".format(profile_name))
    except:
        printer.print_info("Scrolling trough the profile page of {}. It might take a while...".format(target))

    tests.test_elements(browser, elements.post)

    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);") 
    time.sleep(2)

    posts_after_scrolling = len(core.get_elements(browser, **elements.post))
    while True:
        posts_before_scrolling = posts_after_scrolling
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(4)
        posts_after_scrolling = len(core.get_elements(browser, **elements.post))
        browser.execute_script("window.scrollTo(0,0);")

        if posts_after_scrolling <= posts_before_scrolling:
            if len(core.get_elements(browser, **elements.spinner)) > 0:
                spinners = core.get_elements(browser, **elements.spinner)
                for spinner in spinners:
                    scroll_into_view(browser, spinner)
                    time.sleep(3)
            else:
                errors = tests.test_elements(browser, elements.reactions_link, elements.comment)

                printer.print_info("Scrolling completed. Found {} posts and {} errors.".format(posts_after_scrolling, len(errors)))
                break
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
