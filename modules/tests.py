from . import printer


def test_elements(browser, *elements):
    errors = []
    for element in elements:
        if len(browser.find_elements_by_xpath("//{}[@{}='{}']".format(element['html'], element['attribute'], element['value']))) > 0:
            printer.print_good("{} test - ok".format(element['verbose']))
        else:
            if element['verbose'] == "post":
                printer.print_bad('Critical error. No posts were found. Reasons: no posts in profile or post value "{}" was changed in page code'.format(element['value']))
                printer.print_bad('Terminating program...')
                browser.close()
                exit()
            else:
                printer.print_bad('Error. No {} found. Reasons: no {} in profile or {} value "{}" was changed in page code'.format(element['verbose'], element['plural'], element['plural'], element['value']))
                errors.append(element['verbose'])
                test_failed_prompt(browser)
    return errors

def test_failed_prompt(browser):
    answer = None
    while answer not in ("y", "n"):
        answer = input("Would you like to continue? [y/n] ")
        if answer == "y":
            pass
        elif answer == "n":
            browser.close()
            exit()
        else:
            print("Please press 'y' or 'n'.")
            
def profile_prompt(browser, profile_name, target):
    answer = None
    while answer not in ("y", "n"):
        answer = input("User ID: {} is connected to profile name: {} - is this a right profile? [y/n] ".format(target, profile_name))
        if answer == "y":
            pass
        elif answer == "n":
            browser.close()
            exit()
        else:
            print("Please press 'y' or 'n'.")
