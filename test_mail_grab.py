from Mail_Scrap import mail_grab
from datetime import datetime

import os


def domains_file_test():
    if os.path.isfile('domains') or not os.path.isfile('domains'):
        with open('domains', "w") as f:
            f.write('')
        f.close()
        if mail_grab.get_domains() == "File 'domains' is empty.":
            Test_Results['domain_file_empty'] = 'PASS'
        os.remove('domains')
        if mail_grab.domain_exist() == "File 'domains' doesn't exist.":
            Test_Results['domain_file_not_exist'] = 'PASS'
    return Test_Results


def mails_bkp_test():
    time_stamp = (datetime.date(datetime.now())).strftime('%d%m%y') + '_' + str(
        (datetime.time(datetime.now())).strftime('%H%M%S'))
    if os.path.isfile('mails.csv') or not os.path.isfile('mails.csv'):
        with open('mails.csv', "w") as f:
            f.write('user0@test.com')
        f.close()
        status = mail_grab.backup_mails(time_stamp)
        if 'Backup Done.' in status:
            Test_Results['mails_bkp'] = 'PASS'
        else:
            Test_Results['mails_bkp'] = 'FAILED'
    return Test_Results


if __name__ == '__main__':

    Test_Results = {}

    print("\n******* Testing mail.grab.py *******")
    domains_file_test()
    results = mails_bkp_test()
    for result in results:
        print("{:<30}: {:<15}".format(result, results[result]))



