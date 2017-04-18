'''
Created on 6 апр. 2017 г.

@author: pavlo.ivanov


if __name__ == '__main__':
    pass
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import ElementNotVisibleException  
from selenium.common.exceptions import TimeoutException  
from selenium.common.exceptions import StaleElementReferenceException  

from selenium.webdriver.common.keys import Keys
import time
import lxml.etree
from io import StringIO

import smtplib
import datetime


#CONFIG

timeout = 30
counter = 1

email_fromaddr = 'selenium.probe@vidyo.io.test'
email_toaddrs  = 'pavlo.ivanov@globallogic.com'
email_msg = 'There was a terrible error that occured and I wanted you to know!'
email_username = 'vidyo.automation'
email_password = 'v1dy0123'
velp_server = "ve4lp.vidyocloudstaging.com"

agent_site = "https://authentication.liveperson.net/"
agent_acc_number = "79228492"
agent_login = "Probe"
agent_password = "Probe123"

visitor_site = "https://amitsarm85.github.io/"

while counter == 1:
    print("Run " + str(counter) + " started")
    try:
	    #raise
        email_msg = "Subject: Call successful on " + str(velp_server)
        raise TimeoutException("Time out!")

    except StaleElementReferenceException as ex:
        print("StaleElementReferenceException exception: " + str(ex))
        email_msg = "Subject: Call exception on " + str(velp_server) + "\n\n" + str(ex)
        pass
    except TimeoutException as ex:
        print("TimeOut exception in MAIN FLOW: " + str(ex))
        email_msg = "Subject: Call exception on " + str(velp_server) + "\n\n" + str(ex)
        pass
    except:
        email_msg = "Subject: Call exception on " + str(velp_server) + ". Unknown exception"
        pass    
    finally:
        #time.sleep(10)
        #agent_browser.quit()
        #print(agent_browser)
        #visitor_browser.quit()
        #print(visitor_browser)
        #time.sleep(10)
        print(email_msg)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(email_username,email_password)
        server.sendmail(email_fromaddr, email_toaddrs, email_msg)
        server.quit()
        print("Email sent")

        print("Run " + str(counter) + " finished")
        counter = counter + 1
