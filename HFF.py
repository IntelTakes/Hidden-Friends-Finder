#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, click
from pprint import pprint

from modules import chrome
from modules import core
from modules import printer


@click.command()
@click.option('-l', '--login', prompt='\nFacebook login', help='Email you use to login to facebook.', required=True)
@click.option('-p', '--password', prompt='\nFacebook password', help="Password to facebook account.", required=True)
@click.option('-t', '--target', prompt='Target user ID (only numbers)', help="Facebook user ID - ex. 100003743435526", required=True, type=int)
def main(login, password, target):
    browser = chrome.setup()
    core.login(login,password,browser)

    printer.print_banner("Verifying data")
    errors = chrome.scroll_page(browser, target)
    profile_name = core.get_profile_name(browser)

    printer.print_banner("Gathering data")
    if "reactions" not in errors:
        reaction_accounts = core.get_reactions(browser)
    else:
        reaction_accounts = []
    if "comment" not in errors:
        comment_accounts = core.get_comments(browser)
    else:
        comment_accounts = []
    combined_accounts = list({x['FB User ID']:x for x in reaction_accounts + comment_accounts}.values())

    printer.print_banner("Analysing data")
    hidden_friends = core.find_mutual_friends(browser, target, combined_accounts)
    unconfirmed_friends = [x for x in combined_accounts if x not in hidden_friends]
    printer.print_good("Found {} accounts directly connected to {}: {} - confirmed friends, {} - probable friends ".format(len(hidden_friends+unconfirmed_friends), profile_name, len(hidden_friends), len(unconfirmed_friends)))

    printer.print_banner("Printing data")
    printer.save_friends(browser, target, hidden_friends, "confirmed")
    printer.save_friends(browser, target, unconfirmed_friends, "probable")

    browser.close()
    exit()

if __name__ == '__main__':
    printer.print_art()
    main()
