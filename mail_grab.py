from selenium import webdriver
from datetime import datetime

import re
import os
import sys
import time
import progressbar


def domain_exist():
    if not os.path.isfile('domains'):
        os.system('touch domains')
        return "Domains file created."


def get_domains():
    doms = []
    try:
        with open('domains', 'r') as f:
            lines = f.readlines()
            if not lines:
                return "File 'domains' is empty."
            for dom in lines:
                if dom not in doms:
                    dom = dom.rstrip()
                    if not str(dom).endswith('org'):
                        doms.append(dom)
            f.close()
    except Exception as e:
        return 'Error in get_domains(): %s' % str(e)
    else:
        return doms


def backup_mails(ts):
    global file_name
    time_stam = ts
    try:
        if time_stam:
            if os.path.isfile('mails.csv'):
                with open('mails.csv') as f:
                    isemp = f.readlines()
                f.close()
                if isemp:
                    file_name = 'mails_' + time_stam + '.csv'
                    os.rename('mails.csv', file_name)
                    return "Backup Done. File name %s" % file_name
    except Exception as e:
        return 'Error in backup_mails(): %s ' % str(e)


def search_engine(search_eng, dom, s_typ):
    global url
    key = search_eng
    try:
        if key == 'google':
            url = 'https://google.com/?#q="@' + str(dom) + '" ' + s_typ
        if key == 'yahoo':
            url = 'https://in.search.yahoo.com/search?p="' + str(dom) + '" ' + s_typ
        if key == 'ddg':
            url = 'https://duckduckgo.com/?q="' + str(dom) + '" ' + s_typ
        if key == 'ask':
            url = 'https://www.ask.com/web?q="' + str(dom) + '" ' + s_typ
    except Exception as e:
        return 'Error in search_engine(): %s' % str(e)
    else:
        return url


def google_search(dom, opt, s_type, key):
    global driver_path
    try:
        if sys.platform == 'linux':
            driver_path = './webdriver/chromedriver_linux64'
        if sys.platform == 'win32':
            driver_path = './webdriver/chromedriver.exe'

        s_url = search_engine(key, dom, s_type)
        # print(s_url)

        browser = webdriver.Chrome(executable_path=driver_path, options=opt)
        browser.get(s_url)

        # Getting the complete HTML content from a google search in a string format
        elements = browser.find_element_by_tag_name('html')
        content = str(elements.text).split()
        time.sleep(2)
        browser.close()  # Closing browser

    except Exception as e:
        return 'Error in google_search(): %s' % str(e)
    else:
        return content


if __name__ == '__main__':

    failed_domains = []
    mails = {}
    time_stamp = (datetime.date(datetime.now())).strftime('%d%m%y') + '_' + str(
        (datetime.time(datetime.now())).strftime('%H%M%S'))

    domain_exist()                              # Checking existence of domains file
    domains = get_domains()                     # Getting mail ids from a domains file
    if type(domains).__name__ == 'str':
        print(f"\n{str(domains)}")
        sys.exit(1)

    status = backup_mails(time_stamp)           # Taking backup of old mails.csv if the file is non-empty
    if status:
        print(status)

    # Browser Option for Chrome
    option = webdriver.ChromeOptions()
    # option.add_argument(" — incognito")

    domain: str
    ite = 0
    captcha_str = ''
    mail_ids = []
    ID = []
    search_types = ['email', 'info', 'sales']
    # Looping all the domains
    for domain in progressbar.progressbar(domains):
        # Simple Progress
        # print('[' + str(domains.index(domain) + 1) + '/' + str(len(domains)) + ']  ' + str(domain))

        if os.path.isfile('mails.csv'):
            for m_ids in ID:
                if m_ids not in mail_ids:
                    mail_ids.append(m_ids)

            ID = []     # Resetting List ID
        for search_type in search_types:
            while not captcha_str:
                lines = google_search(domain, option, search_type, key='google')
                captcha_str = 'stop_loop'
                if 'unusual' in lines and 'traffic' in lines:
                    captcha_str = 'unusual'
                    if domain not in failed_domains:
                        failed_domains.append(domain)

            # print(lines)

            # Recall the google search type url after a five unusual traffic
            if captcha_str == 'unusual':
                lines = google_search(domain, option, search_type, key='ask')
                ite += 1
                if ite % 5 == 0:
                    captcha_str = ''
            else:
                captcha_str = ''

            # Matching all the mailIDs from each line
            for line in lines:
                mailID = re.findall('[\w]+@[\w\W]+.com', line)  # Matching mail ID
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
