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


def check_exists_by_xpath(webdriver, timeout, xpath):
    try:
        #webdriver.find_element_by_xpath(xpath)
        #WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))) presence_of_element_located
        WebDriverWait(webdriver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath))) 
    except ElementNotVisibleException:
        print("Element NOT VISIBLE: " + str(xpath))
        return False
    except NoSuchElementException:
        print("No such element: " + str(xpath))
        return False
    except TimeoutException as ex:
        print("Element PRESENCE check TIMEOUT: " + str(ex))
        return False
    except:
        print("Unknown exception in EXISTENCE check: " + str(ex))
        return False
    return True

# finally:
#    print("Unknown Exception wheen trying to fing the: " + str(xpath))
#print("Element NOT VISIBLE: " + str(xpath))
def check_visibility_by_xpath(webdriver, xpath):
    try:
        WebDriverWait(webdriver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except ElementNotVisibleException:
        print("Element NOT VISIBLE: " + str(xpath))
        return False
    except TimeoutException as ex:
        print("Element VISIBILITY check TIMEOUT: " + str(ex))
        return False
    except:
        print("Unknown exception in VISIBILITY check: " + str(ex))
        return False
    return True
    
    
def agent_site_login(agent_browser, username, userpass, account_number):

    welcome_label = agent_browser.find_element(By.ID, 'welcomeLabel')
    welcome_label = agent_browser.find_element(By.XPATH, "//div[@id='welcomeLabel']")
    site_number = agent_browser.find_element(By.ID, 'siteNumber')
    user_id = agent_browser.find_element(By.ID, 'userName')
    password = agent_browser.find_element(By.ID, 'sitePass')
    submit_button = agent_browser.find_element(By.ID, 'submitButtonWrapper')

    site_number.send_keys(account_number)
    user_id.send_keys(username)
    password.send_keys(userpass)
    submit_button.click()



def agent_close_existing_conversations(agent_browser):
    
    while check_exists_by_xpath(agent_browser, "//div[contains(@class,'lpview_dropdown_menu_container lpview_dropdown_menu_button actions_menu')]"):
        agent_engagement_dropdown_menu = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'lpview_dropdown_menu_container lpview_dropdown_menu_button actions_menu')]")))
        agent_engagement_dropdown_menu.click()
        if check_exists_by_xpath(agent_browser, "//div[contains(text(),'End engagement')]"):
            agent_dropdown_menu_end_engagement = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'End engagement')]")))
            agent_dropdown_menu_end_engagement.click()
            #agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class(),'lpview_okButton button dark_bg grey operative')]")))
            #agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class(),'lpview_okButton')]")))
            if not check_exists_by_xpath(agent_browser, "//*[@id='LP_undefined_2']/div/div[2]/div[3]/div[2]/span"):
                print("End Engagement OK button not found")
            agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='LP_undefined_2']/div/div[2]/div[3]/div[2]/span")))
            #agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'End engagement')]")))
            agent_dropdown_menu_end_engagement_confirm_button.click()
        else:
            agent_dropdown_menu_end_engagement = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class(),'lpview_hideConversation_engagement_menu_item LP_header_floating_actions_menu_item hideConversation')]")))
            agent_dropdown_menu_end_engagement.click()
    else:
        print("Conversation control drop-down not found")


def agent_invite_visitor(agent_browser):
    print("Searching for 'Connecting to visitor' string")
    WebDriverWait(agent_browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
    if check_exists_by_xpath(agent_browser, 10, "//div[@id='pre-call']//h1[contains(text(),'Connecting')]"):
        print("'Connecting to visitor' FOUND")
    else:
        print("'Connecting to visitor' NOT FOUND")
    agent_browser.switch_to.default_content()
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()
        
    print("Searching for 'Detecting video capability' string")
    WebDriverWait(agent_browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
    if check_exists_by_xpath(agent_browser, 10, "//div[@id='pre-call']//h1[contains(text(),'Detecting')]"):
        print("'Detecting video capability' FOUND")
    else:
        print("'Detecting video capability' NOT FOUND")
    agent_browser.switch_to.default_content()
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

    print("Searching for 'Click invite to initialize a video call' string")
    WebDriverWait(agent_browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
    if check_exists_by_xpath(agent_browser, 30, "//div[@id='pre-call']//h1[contains(text(),'Click invite to initialize a video call')]"):
        print("'Click invite to initialize a video call' FOUND")
    else:
        print("'Click invite to initialize a video call' NOT FOUND")
    agent_browser.switch_to.default_content()
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

    agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
    # Unable to establish connection. Please check your network. [CRLF] Refresh this widget to attempt to continue.



def agent_open_LPVE_widget(agent_browser):
    #agent_browser.switch_to.default_content()
    print("Checking existense LPVE widges button")
    #agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")
    
    #WebDriverWait(agent_browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='LP_MainWidgetsManagerViewController_1']//div[contains(@class,'custom_widget_icon')]")))
    while not check_exists_by_xpath(agent_browser, 5, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon_pilot disabled selected')]"):
        try: 
            WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]")))
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()
        except StaleElementReferenceException:
            print("StaleElementReferenceException exception: " + str(ex))
            #agent_browser.execute_script("$('.custom_widget_icon').click()")
            print("Trying one more time....")
            WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]")))
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()
    print("Clicked the LPVE widges button")
    #agent_custom_vi_widget.click()



def agent_wait_page_load_finished(agent_browser):
    agent_upper_menu = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@class='top-level-menu-switch']")))


def agent_pickup_call(agent_browser):
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_QueueOrbView_1']//div[contains(text(), 'Accept')]"))).click()


def agent_close_advertisement_panel(agent_browser):
    if check_exists_by_xpath(agent_browser, 10, "//div[contains(@class, 'connection-profile-close-arrow')]"):
        print("Closing the Advertizement panel")
        WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'connection-profile-close-arrow')]"))).click()

def agent_end_call(agent_browser):
    agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")
    print("Clicked on Agent END CALL button")


def agent_mute_own_in_call_camera(agent_browser):
    print("Muting the Agent CAMERA")
    agent_browser.execute_script("$('.iframeElement').contents().find('#video-btn').click()")
    print("Agent CAMERA muted")
    time.sleep(1)


def agent_unmute_own_in_call_camera(agent_browser):
    print("Muting the Agent CAMERA")
    agent_browser.execute_script("$('.iframeElement').contents().find('#video-btn').click()")
    print("Agent CAMERA muted")
    time.sleep(1)

def agent_mute_own_in_call_microphone(agent_browser):
    print("Muting the Agent MICROPHONE")
    agent_browser.execute_script("$('.iframeElement').contents().find('#mic-btn').click()")
    print("Agent MICROPHONE muted")
    time.sleep(1)

def agent_unmute_own_in_call_microphone(agent_browser):
    print("Muting the Agent MICROPHONE")
    agent_browser.execute_script("$('.iframeElement').contents().find('#mic-btn').click()")
    print("Agent MICROPHONE muted")
    time.sleep(1)


def visitor_open_chat(visitor_browser):
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class,'LPMimage')]"))).click()
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_top-text')]")))


def visitor_mute_own_in_call_microphone(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    print("Checking that the Visitor MICROPHONE EXISTS and NOT MUTED")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"):
        try:
            print("Trying to MUTE the Visitor MICROPHONE")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"))).click()
            
        except:
            print("Exception: UNMUTED Visitor MICROPHONE NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
            print("Visitor MICROPHONE is already MUTED")
        else:
            print("Visitor MICROPHONE control NOT FOUND")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
        print("Visitor MICROPHONE is MUTED")
    else:
        print("Visitor MICROPHONE is NOT MUTED")
        print("Trying to find the MUTED Visitor MICROPHONE for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]")))
        except:
            print("Visitor MICROPHONE control NOT FOUND in MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")       
    visitor_browser.switch_to_default_content()


def visitor_unmute_own_in_call_microphone(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    print("Checking that the Visitor MICROPHONE EXISTS and  MUTED")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
        try:
            print("Trying to UN-MUTE the Visitor MICROPHONE")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"))).click()
            
        except:
            print("Exception: MUTED Visitor MICROPHONE NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"):
            print("Visitor MICROPHONE is already UN-MUTED")
        else:
            print("Visitor MICROPHONE control NOT FOUND")
    # Checking that MIC has changed its state to UN-MUTED
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"):
        print("Visitor MICROPHONE is UNMUTED")
    else:
        print("Visitor MICROPHONE is STILL MUTED")
        print("Trying to find the UNMUTED Visitor MICROPHONE for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]")))
        except:
            print("Visitor MICROPHONE control NOT FOUND in UN-MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")       
    visitor_browser.switch_to_default_content()

# Page Object ==========================================================================================================
# <div id="VyIRojPtYS2w_renderer_vidyoRemoteName0" class="guest">demoUser_97567</div> # Counterparty name on the screen
# <button id="joinLeaveButton" class="toolbarButton callStart" title="Join Conference"/> # Join Button 
# <button id="cameraButton" class="toolbarButton cameraOn" title="Camera Privacy"/> # Camera button
# <button id="microphoneButton" class="toolbarButton microphoneOn" title="Microphone Privacy"/> # Microphone button
# <select id="cameras"> # Camera selection drop-down
# <select id="microphones"> # Microphone selection drop-down
# <select id="speakers"> # Speakers
#     <option value="0">None</option>
#     <option value="ZGVmYXVsdA==">Default</option>
# <input id="host" value="prod.vidyo.io" type="text"/> # Host
# <input id="token" placeholder="ACCESS-TOKEN" value="" type="text"/> # Token
# <input id="displayName" placeholder="Display Name" value="Guest" type="text"/> # Display name
# <input id="resourceId" placeholder="Conference Reference" value="demoRoom" type="text"/> # Resource ID (room)
# //*[@id="notifier"]
# class="notifier-sub-container"
# sub //*[@id="notifier"]/div/div[1] - div class="notifierTitle" text = Process failed
# sub - class="notifierMessage" text Please try again.


#driver = webdriver.Chrome(chrome_options=options)

#CONFIG

timeout = 30
counter = 1
while counter == 1:
    print("Run " + str(counter) + " started")
    try:
        options = webdriver.ChromeOptions()
        #print(options)
        #options.addArguments("start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-web-security")
        options.add_argument("--use-fake-ui-for-media-stream")
        
        #print(options.to_capabilities()) --disable-web-security
        #agent_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        agent_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=options.to_capabilities())
        #agent_browser = webdriver.Chrome(chrome_options=options)
        
        agent_browser.get('https://va-a.authentication.liveperson.net/')
        agent_browser.maximize_window()
        #agent_browser.implicitly_wait(30)
        agent_site_login(agent_browser, 'Agent1', 'Agent123', '54424706') #VEL-QA
        #agent_site_login(agent_browser, 'Bohdan', 'Bohdan123', '57877913') # VEL
        
        """
        visitor_options = webdriver.ChromeOptions()
        #print(options)
        #options.addArguments("start-maximized")
        visitor_options.add_argument("--disable-notifications")
        visitor_options.add_argument("--disable-web-security")
        visitor_options.add_argument("--use-fake-ui-for-media-stream")
        """

        #visitor_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        visitor_browser = webdriver.Chrome(chrome_options=options)
        
        visitor_browser.get('https://pavelivanov1.github.io/LPVE/')  #VEL-QA
        #visitor_browser.get('https://ishapiro11.github.io/liveperson-visitor/ilanaaws.htm') # VEL
        #time.sleep(5)
        
        agent_wait_page_load_finished(agent_browser)
        
        """
        visitor_LE_chat_tab = WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class,'LPMimage')]")))
        visitor_LE_chat_tab.click()
        """

        #visitor_browser.refresh()
        
        
        #visitor_chat_caption = WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_top-text')]")))
        visitor_open_chat(visitor_browser)
        
        #agent_incoming_call = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_QueueOrbView_1']//div[contains(text(), 'Accept')]")))
        #agent_pickup_call = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_QueueOrbView_1']//div[contains(text(), 'Accept')]"))).click()
        agent_pickup_call(agent_browser)

        #agent_open_LPVE_widget(agent_browser)
        """
        alpve = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_MainWidgetsManagerViewController_1']//div[contains(@class,'custom_widget_icon')]")))
        alpve = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]")))
        alpve.click()
        """
        agent_open_LPVE_widget(agent_browser)
        
        agent_close_advertisement_panel(agent_browser)
        
        agent_invite_visitor(agent_browser)
        
        # Mute camera id="video-toggle-button"
        # Agent, Before call
        agent_browser.execute_script("$('.iframeElement').contents().find('#video-toggle-button').click()")
        agent_browser.execute_script("$('.iframeElement').contents().find('#video-toggle-button').click()")
        # Mute mic id="microphone-toggle-button"
        agent_browser.execute_script("$('.iframeElement').contents().find('#microphone-toggle-button').click()")
        agent_browser.execute_script("$('.iframeElement').contents().find('#microphone-toggle-button').click()")

      
        # Sending the invitation message on the Agent side
        WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
        
        
        
        
        # Waiting for the invitation indicator on the Visitor side
        visitor_chat_vidyo_invitation_indicator = WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_notification_text')]")))
        
        # Visitor opens the widget after an invite
        WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'lp_slider')]"))).click()
            
        
        
        
        '''
        agent_invite_button = WebDriverWait(agent_browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'invite-btn')]")))
        agent_invite_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'invite-btn')]")))
        print(agent_invite_button)
        agent_invite_button.click()
        '''
        
        
        
        # id LPFRM_eb3f01-4a22-9d2e
        visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
        WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'join-button')]"))).click()
        visitor_browser.switch_to_default_content()
        time.sleep(5)

        visitor_mute_own_in_call_microphone(visitor_browser)

        # Mute the camera on Agent side
        """
        print("Muting the Agent CAMERA")
        agent_browser.execute_script("$('.iframeElement').contents().find('#video-btn').click()")
        print("Agent CAMERA muted")
        time.sleep(1)
        """

        agent_mute_own_in_call_microphone(agent_browser)

        agent_mute_own_in_call_camera(agent_browser)
        agent_unmute_own_in_call_camera(agent_browser)
        
        agent_unmute_own_in_call_microphone(agent_browser)

        visitor_unmute_own_in_call_microphone(visitor_browser)

        """
        # Un-mute the camera on Agent side
        print("Un-muting the Agent CAMERA")
        agent_browser.execute_script("$('.iframeElement').contents().find('#video-btn').click()")
        print("Agent CAMERA un-muted")
        time.sleep(1)

        # Mute the mic on Agent side
        print("Muting the Agent MICROPHONE")
        agent_browser.execute_script("$('.iframeElement').contents().find('#mic-btn').click()")
        print("Agent MICROPHONE muted")
        time.sleep(1)
        # Un-mute the mic on Agent side
        print("Un-muting the Agent MICROPHONE")
        agent_browser.execute_script("$('.iframeElement').contents().find('#mic-btn').click()")
        print("Agent MICROPHONE un-muted")
        time.sleep(1)
        """



        # End the call at the Agent side
        agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")
        print("Clicked on Agent END CALL button")
        time.sleep(5)
        #WebDriverWait(agent_browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))



    except StaleElementReferenceException:
        print("StaleElementReferenceException exception: " + str(ex))
        pass
    except TimeoutException as ex:
        print("TimeOut exception in MAIN FLOW: " + str(ex))
        pass
    except:
        pass    
    finally:
        #time.sleep(10)
        agent_browser.quit()
        #print(agent_browser)
        visitor_browser.quit()
        #print(visitor_browser)
        #time.sleep(10)
        print("Run " + str(counter) + " finished")
        counter = counter + 1
