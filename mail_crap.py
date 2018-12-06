from selenium import webdriver
from datetime import datetime

import re
import os
import sys


def google_search(dom, opt, url):
    global driver_path
    # print(url)
    try:
        if url == 'g':
            url = 'https://google.com/?#q="' + str(dom) + '" email'
        if url == 'y':
            url = 'https://in.search.yahoo.com/search?p="' + str(dom) + '" email'
        if sys.platform == 'linux':
            driver_path = './webdriver/chromedriver_linux64'
        if sys.platform == 'nt':
            driver_path = './webdriver/chromedriver.exe'
        browser = webdriver.Chrome(executable_path=driver_path, options=opt)
        browser.get(url)

        # Getting the complete HTML content from a google search in a string format
        elements = browser.find_element_by_tag_name('html')
        content = str(elements.text).split()

        # Closing the browser if it is a last domain
        # if len(domains) == domains.index(dom) + 1:
        browser.close()
    except Exception as e:
        return 'Error in google_search(): %s' % str(e)
    else:
        return content


if __name__ == '__main__':
    # Checking existence of domains file
    if not os.path.isfile('domains'):
        print("\nFile 'domains' doesn't exist.")
        sys.exit(1)

    domains = []
    failed_domains = []
    # Getting the Domains from the file
    with open('domains', 'r') as f:
        lines = f.readlines()
        if not lines:
            print("\nFile 'domains' is empty.")
            sys.exit(1)
        for domain in lines:
            if domain not in domains:
                domain = domain.rstrip()
                domains.append(domain)
        f.close()
    # print(domains)

    mails = {}
    time_stamp = (datetime.date(datetime.now())).strftime('%d%m%y') + '_' + str(
        (datetime.time(datetime.now())).strftime('%H%M%S'))

    # Taking backup of old mails.csv if the file is empty
    if os.path.isfile('mails.csv'):
        with open('mails.csv') as f:
            lines = f.readlines()
            if lines:
                file_name = 'mails_' + time_stamp + '.csv'
                os.rename('mails.csv', file_name)
            f.close()

    # Browser Option for Chrome
    option = webdriver.ChromeOptions()
    # option.add_argument(" — incognito")

    # Looping all the domains
    domain: str
    for domain in domains:
        lines = google_search(domain, option, url='g')

        ID = []
        ms = []

        # print(lines)

        # Collecting the domains which is blocked by google
        if 'unusual' in lines:
            print(lines)
            lines = google_search(domain, option, url='y')
            failed_domains.append(domain)
            print(failed_domains)

        # Matching all the mailIDs from each line
        for line in lines:
            mailID = re.findall('[\w]+@[\w\W]+.com', line)
            # print(mailID)
            if mailID:
                for mail in mailID:
                    '''
                    # Filtering the mailID by domain
                    if domain in mail:
                        # Removing the extra char in end of mail
                        match = len(domain) + str(mail).index('@')
                        mail = mail[:match + 1]
                    '''

                    # Filtering redundant mailID and .org mails
                    if not str(mail).endswith('.org'):
                        if str(mail).lower() not in ID:
                            ID.append(str(mail).lower())

        mails[domain] = ID
        print(ID)

        # Getting mails from mails.csv file
        if os.path.isfile('mails.csv'):
            with open('mails.csv', 'r') as f:
                ms = f.readlines()
                # Removing \n from mailID
                for item in range(len(ms)):
                    ms[item] = ms[item].rstrip()
            f.close()

        if not ms:
            ms = ['']

        with open('mails.csv', 'a') as f:
            if mails[domain]:
                for ids in mails[domain]:
                    # Filtering duplicate mailID
                    if ids not in ms:
                        f.write(str(ids) + '\n')
            f.close()

    if failed_domains:
        with open('failed_domains', 'a') as f:
            for fdom in failed_domains:
                f.write(domain + '\n')
        f.close()
