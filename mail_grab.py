from selenium import webdriver
from datetime import datetime

import re
import os
import sys
import progressbar


def search_engine(search_eng, dom):
    key = search_eng
    try:
        if key == 'g':
            url = 'https://google.com/?#q="' + str(dom) + '" email'
        if key == 'y':
            url = 'https://in.search.yahoo.com/search?p="' + str(dom) + '" email'
        if key == 'ddg':
            url = 'https://duckduckgo.com/?q="' + str(dom) + '" email'
    except Exception as e:
        return 'Error in search_engine(): %s' % str(e)
    else:
        return url


def google_search(dom, opt, key):
    global driver_path
    try:
        url = search_engine(key, dom)
        # print(url)
        if sys.platform == 'linux':
            driver_path = './webdriver/chromedriver_linux64'
        if sys.platform == 'win32':
            driver_path = './webdriver/chromedriver.exe'
        browser = webdriver.Chrome(executable_path=driver_path, options=opt)
        browser.get(url)

        # Getting the complete HTML content from a google search in a string format
        elements = browser.find_element_by_tag_name('html')
        content = str(elements.text).split()
        browser.close()     # Closing browser
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

    # Taking backup of old mails.csv if the file is non-empty
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

    domain: str
    ite = 0
    captcha_str = ''
    mail_ids = []
    ID = []

    # Looping all the domains
    for domain in progressbar.progressbar(domains):
        # Simple Progress
        # print('[' + str(domains.index(domain) + 1) + '/' + str(len(domains)) + ']  ' + str(domain))

        while not captcha_str:
            lines = google_search(domain, option, key='g')
            captcha_str = 'stop_loop'
            if 'unusual' in lines and 'traffic' in lines:
                captcha_str = 'unusual'
                if domain not in failed_domains:
                    failed_domains.append(domain)

        if os.path.isfile('mails.csv'):
            for m_ids in ID:
                if m_ids not in mail_ids:
                    mail_ids.append(m_ids)

        ID = []     # Resetting List ID

        # print(lines)

        # Collecting the domains which is blocked by google and searching by Yahoo
        # Recall the google search type url after a five unusual traffic
        if captcha_str == 'unusual':
            lines = google_search(domain, option, key='ddg')
            ite += 1
            if ite % 5 == 0:
                captcha_str = ''
        else:
            captcha_str = ''

        # Matching all the mailIDs from each line
        for line in lines:
            mailID = re.findall('[\w]+@[\w\W]+.com', line)      # Matching mail ID
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

        # Appending mails to a file
        with open('mails.csv', 'a') as f:
            if mails[domain]:
                for ids in mails[domain]:
                    # Filtering duplicate mailID
                    if ids not in mail_ids:
                        f.write(str(ids) + '\n')
        f.close()

    if failed_domains:
        with open('failed_domains', 'a') as f:
            for fdom in failed_domains:
                f.write(domain + '\n')
        f.close()
    # print(failed_domains)
