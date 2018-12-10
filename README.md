# mailid_grab

	    The python script which is running on selenium will open the chrome browser (both google and yahoo) 
	    and will search the content by the string `(Ex. "domain" email)` and grab the whole <html>  content 
	    as string. Finally it will process the whole string content and matches only mail ID's.

	    
	    ## Pre-requesites:
	    
	    1. Python 3.7 or higher than this version should be installed.
	       `https://www.python.org/downloads/`
	    2. Selenium should be installed.
	       `pip install selenium`
	    
	    
	    ## How to run:
	    
	    1. Clone the code by `git clone https://github.com/GuGu910/mailid_grab.git`
	    2. Put a punch of domains in a file `domains`.
	    3. Just run a `mail_grab.py`.
	    4. Finally all mails will be saved in a file mails.csv
	    
	    
	    ## Testing output
	    
	    ******* Testing mail_grab.py *******
        domain_file_empty             : PASS           
        domain_file_not_exist         : PASS           
        mails_bkp                     : PASS 
        
        ******* Testing mail.grab.py *******
        domain_file_empty             : FAILED         
        domain_file_not_exist         : FAILED         
        mails_bkp                     : FAILED  