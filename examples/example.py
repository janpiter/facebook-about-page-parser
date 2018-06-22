from __future__ import print_function
import re
import json
import argparse
import mechanicalsoup
from getpass import getpass
import __init__
from src.parser import ExtractFacebookProfile


def get_about():
    try:
        browser = mechanicalsoup.StatefulBrowser(
            user_agent='Mozilla/5.0 (Windows NT 6.1) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/41.0.2228.0 Safari/537.36',
        )

        browser.open("https://mbasic.facebook.com/login")
        browser.select_form('#login_form')
        browser["email"] = args.username
        browser["pass"] = args.password
        browser.submit_selected()

        browser.open("https://mbasic.facebook.com/jpnkls/about")
        html_page = browser.get_current_page()

        if html_page.find("a", href=re.compile(r"logout")):
            efp = ExtractFacebookProfile()
            result = efp.get(html_page)
            if result:
                print(json.dumps(result, indent=4))

    except BaseException as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Login to Facebook.")
    parser.add_argument("username")
    args = parser.parse_args()
    args.password = getpass("Please enter your Facebook password: ")
    get_about()
