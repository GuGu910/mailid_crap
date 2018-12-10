# mailid_grab
  The python script which is running on selenium will open the chrome browser and will 
search the content by the string `(Ex. "test.com" email)` and grab the whole `<html>`  content 
as string. Finally it will process the whole string content and matches only mail ID's.

#### Pre-requisites:
	    
1. [Python 3.7](https://www.python.org/downloads/) should be installed.
2. [Selenium](https://pypi.org/project/selenium/) should be installed. `pip install selenium`
3. [Progressbar](https://pypi.org/project/progressbar2/) should be installed. `pip install progressbar2`
	    
#### How to run:
	    
1. Download the `mailid_grab` code [here](https://github.com/GuGu910/mailid_grab/archive/master.zip) and extract into any directory/folder.
2. Put a punch of domains in a file [domains](domains).
3. Just run a [test_mail_grab.py](test_mail_grab.py) before running [mail_grab.py](mail_grab.py).
4. If all test status `PASS` then you can run [mail_grab.py](mail_grab.py).
4. Finally all mails will be saved and generated in a file `mails.csv`. 
	    
	    
#### Testing results:

PASS Scenario:
```	    
******* Testing mail_grab.py *******
domain_file_empty             : PASS           
domain_file_not_exist         : PASS           
mails_bkp                     : PASS 
```
FAILED Scenario:
```     
******* Testing mail.grab.py *******
domain_file_empty             : FAILED         
domain_file_not_exist         : FAILED         
mails_bkp                     : FAILED  
```