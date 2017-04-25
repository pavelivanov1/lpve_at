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

    velp_server = 've4lp.vidyocloudstaging.com'



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


def agent_send_invite_message(agent_browser):
    print("Searching the SEND MESSAGE button")
    if check_exists_by_xpath(agent_browser, 10, "//div[contains(@id, 'LP_RichTextChatInputViewController')]//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"):
        print("SEND MESSAGE button FOUND")
        print("Trying to click the SEND MESSAGE button...")
        try:
            WebDriverWait(agent_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'LP_RichTextChatInputViewController')]//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
        except:
            print("Exception: Agent SEND MESSAGE button NOT FOUND")
            print("Trying click Agent SEND MESSAGE button for one more time, by PRESENSE of the ELEMENT....")
            WebDriverWait(agent_browser, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'LP_RichTextChatInputViewController')]//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
            #agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
            #agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
            #agent_browser.execute_script("$find('.lpview_send_msg_button chat_input_button').click();")
            agent_browser.execute_script("$('.lpview_send_msg_button chat_input_button').trigger('click';")
    else:
        print("SEND MESSAGE button NOT FOUND")


"""
def agent_invite_visitor(agent_browser):
    print("Verifying that the Agent IFRAME exists...")
    if check_exists_by_xpath(agent_browser, 2, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"):
        print("Agent IFRAME FOUND")
        print("Switching the Agent to IFRAME...")
        WebDriverWait(agent_browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                                          "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
        print("Searching for 'Connecting to visitor' string")
        if check_exists_by_xpath(agent_browser, 2, "//div[@id='pre-call']//h1[contains(text(),'Connecting')]"):
            print("'Connecting to visitor' FOUND")
        else:
            print("'Connecting to visitor' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        print("Searching for 'Detecting video capability' string")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                                         "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
        if check_exists_by_xpath(agent_browser, 2, "//div[@id='pre-call']//h1[contains(text(),'Detecting')]"):
            print("'Detecting video capability' FOUND")
        else:
            print("'Detecting video capability' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        print("Searching for 'Click invite to initialize a video call' string")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                                         "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
        if check_exists_by_xpath(agent_browser, 2,
                                 "//div[@id='pre-call']//h1[contains(text(),'Click invite to initialize a video call')]"):
            print("'Click invite to initialize a video call' FOUND")
        else:
            print("'Click invite to initialize a video call' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
    else:
        print("Agent IFRAME NOT FOUND")
        raise NoSuchElementException

    # Unable to establish connection. Please check your network. [CRLF] Refresh this widget to attempt to continue.
"""

def agent_invite_visitor(agent_browser):
    print("Verifying that the Agent IFRAME exists...")
    if check_exists_by_xpath(agent_browser, 2, agent_iframe_xpath):
        print("Agent IFRAME FOUND")
        print("Switching the Agent to IFRAME...")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
        print("Searching for 'Connecting to visitor' string")
        if check_exists_by_xpath(agent_browser, 2, "//div[@id='pre-call']//h1[contains(text(),'Connecting')]"):
            print("'Connecting to visitor' FOUND")
        else:
            print("'Connecting to visitor' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        print("Searching for 'Detecting video capability' string")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
        if check_exists_by_xpath(agent_browser, 2, "//div[@id='pre-call']//h1[contains(text(),'Detecting')]"):
            print("'Detecting video capability' FOUND")
        else:
            print("'Detecting video capability' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        print("Searching for 'Click invite to initialize a video call' string")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
        if check_exists_by_xpath(agent_browser, 2,
                                 "//div[@id='pre-call']//h1[contains(text(),'Click invite to initialize a video call')]"):
            print("'Click invite to initialize a video call' FOUND")
        else:
            print("'Click invite to initialize a video call' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        # agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//*[contains(@id,'invite-btn')]"))).click()
        agent_browser.switch_to.default_content()
    else:
        print("Agent IFRAME NOT FOUND")
        raise NoSuchElementException



def agent_open_LPVE_widget(agent_browser):
    #agent_browser.switch_to.default_content()
    print("Checking existense LPVE widget button")
    #agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")
    
    #WebDriverWait(agent_browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='LP_MainWidgetsManagerViewController_1']//div[contains(@class,'custom_widget_icon')]")))
    #while not check_exists_by_xpath(agent_browser, 5, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon_pilot disabled selected')]"):
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

def agent_reinvite_call(agent_browser):
    
    #print("Switching to Agent IFRAME")
    #agent_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"))))
    """
    print("Checking that the Agent 'The video session has ended' is PRESENT")
    if check_exists_by_xpath(agent_browser, 5, "//div[@id='post-call']//h3[contains(text(),'The video session has ended')]"):
        print("Agent 'The video session has ended' is PRESENT")
        print("Checking that the Agent 'Please click Invite to re-start the session' is PRESENT")
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='post-call']//h3/p[contains(text(),'Please click Invite to re-start the session')]"):
            print("Agent 'Please click Invite to re-start the session' is PRESENT")
            print("Checking that the Agent 'RE-INVITE' button is PRESENT")
            if check_exists_by_xpath(agent_browser, 5, "//div[@id='post-call']//button[contains(@id,'resend-invite-btn')]"):
                try:
                    print("Trying to click Agent 'RE-INVITE' button")
                    WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='post-call']//button[contains(@id,'resend-invite-btn')]"))).click()
                except:
                    print("Exception: Agent 'RE-INVITE' button NOT FOUND")
                    print("Trying click Agent 'RE-INVITE' button for one more time....")
                    WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='post-call']//button[contains(@id,'resend-invite-btn')]"))).click()
        else:
            print("Agent 'Please click Invite to re-start the session' is NOT FOUND")
    else:
        print("Agent 'The video session has ended' is NOT FOUND")
    """
    
    print("Switching the Agent to DEFAUL CONTENT")
    agent_browser.switch_to.default_content()
    agent_browser.execute_script("$('.iframeElement').contents().find('#resend-invite-btn').click()")
    agent_browser.switch_to.default_content()
    print("Agent: Sending the INVITE MESSAGE")
    agent_send_invite_message(agent_browser)
    print("Switching to Agent IFRAME")
    agent_browser.switch_to_frame(WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"))))
    print("Checking that the Agent END CALL button is PRESENT")

    if check_exists_by_xpath(agent_browser, 5, "//button[@id='call-btn']"):
        print("Agent END CALL button found")
    else:
        print("Agent END CALL button NOT FOUND")
        print("Trying to find the END CALL button for one more time...") 
        try:
            agent_browser.switch_to.default_content()
            agent_browser.switch_to_frame(WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"))))
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='call-btn']")))
        except:
            print("Agent END CALL button NOT FOUND after RE-INVITE after 2 search attempts")
    print("Switching back to Agent DEFAULT CONTENT")       
    agent_browser.switch_to_default_content()




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



def visitor_mute_own_in_call_camera(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    print("Checking that the Visitor CAMERA EXISTS and NOT MUTED")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"):
        try:
            print("Trying to MUTE the Visitor CAMERA")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"))).click()
            
        except:
            print("Exception: UNMUTED Visitor CAMERA NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
            print("Visitor CAMERA is already MUTED")
        else:
            print("Visitor CAMERA control NOT FOUND")
    print("Checking that the CAMERA has been really MUTED...")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"):
        print("Visitor CAMERA is MUTED")
    else:
        print("Visitor CAMERA is NOT MUTED")
        print("Trying to find the MUTED Visitor CAMERA for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]")))
        except:
            print("Visitor CAMERA control NOT FOUND in MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")       
    visitor_browser.switch_to_default_content()


def visitor_unmute_own_in_call_camera(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    print("Checking that the Visitor CAMERA EXISTS and  MUTED")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"):
        try:
            print("Trying to UN-MUTE the Visitor CAMERA")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"))).click()
            
        except:
            print("Exception: MUTED Visitor CAMERA NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"):
            print("Visitor CAMERA is already UN-MUTED")
        else:
            print("Visitor CAMERA control NOT FOUND")
    # Checking that MIC has changed its state to UN-MUTED
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"):
        print("Visitor CAMERA is UNMUTED")
    else:
        print("Visitor CAMERA is STILL MUTED")
        print("Trying to find the UNMUTED Visitor CAMERA for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]")))
        except:
            print("Visitor CAMERA control NOT FOUND in UN-MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")       
    visitor_browser.switch_to_default_content()


def visitor_end_call(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    print("Checking that the Visitor END CALL button EXISTS")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"):
        try:
            print("Trying to END the call from Visitor side")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"))).click()
            
        except:
            print("Exception: END CALL button for Visitor NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"))).click()
    else:
        print("Visitor END CALL button not found")
        
    # Checking that Visitor screen shows 'The video session has ended'
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='post-call']/div[contains(@id,'post-call-content')]/h3/span[contains(text(),'The video session has ended')]"):
        print("Visitor call has been ENDED with 'The video session has ended'")
    else:
        print("Visitor 'The video session has ended' NOT FOUND")
        print("Trying to find the Visitor 'The video session has ended' for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='post-call']/div[contains(@id,'post-call-content')]/h3/span[contains(text(),'The video session has ended')]")))
        except:
            print("Visitor 'The video session has ended' NOT FOUND after 2 search attempts")

    # Checking that Visitor screen shows 'REJOIN' button
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"):
        print("Visitor call has been ENDED and REJOIN button displayed")
    else:
        print("Visitor REJOIN button NOT FOUND")
        print("Trying to find the Visitor REJOIN button for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]")))
        except:
            print("Visitor REJOIN button NOT FOUND after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")       
    visitor_browser.switch_to_default_content()



def visitor_rejoin_call(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    print("Checking that the Visitor REJOIN button is PRESENT")
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"):
        try:
            print("Trying to click Visitor REJOIN button")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"))).click()
            
        except:
            print("Exception: Visitor REJOIN button NOT FOUND")
            print("Trying click Visitor REJOIN button for one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"))).click()
    else:
        print("Visitor REJOIN button NOT FOUND")
    # Checking that Visitor REJOINED the call (END CALL button present)
    if check_exists_by_xpath(visitor_browser, 5, "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"):
        print("Visitor Re-Joined the call")
    else:
        print("Visitor could not REJOIN the call, END CALL button NOT FOUND")
        print("Trying to find the END CALL button for one more time...") 
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]")))
        except:
            print("Visitor END CALL button NOT FOUND after REJOIN after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")       
    visitor_browser.switch_to_default_content()


#CONFIG

timeout = 30
counter = 1

email_fromaddr = 'selenium.probe@vidyo.io.test'
email_toaddrs  = 'pavlo.ivanov@globallogic.com, pavelivanov1@gmail.com'
email_msg = 'There was a terrible error that occured and I wanted you to know!'
email_username = 'vidyo.automation'
email_password = 'v1dy0123'
velp_server = "ve4lp.vidyocloudstaging.com"

agent_site = "https://authentication.liveperson.net/"
agent_acc_number = "79228492"
agent_login = "Probe"
agent_password = "Probe123"

visitor_site = "https://amitsarm85.github.io/"

timeout = 30
default_timeout = 10
small_timeout = 2
counter = 1

agent_iframe_xpath = "//div[contains(@class,'lpview_widget right_pane_widget_wrapper_iframe') and contains(@style,'display: block')]//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"
visitor_iframe_xpath = "//iframe[contains(@id,'LPFRM')]"

while counter == 1:
    print("Run " + str(counter) + " started")
    try:
        options = webdriver.ChromeOptions()
        #print(options)
        #options.addArguments("start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-web-security")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--mute-audio")
        
        
        #print(options.to_capabilities()) --disable-web-security
        #agent_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        #agent_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=options.to_capabilities())
        agent_browser = webdriver.Chrome(chrome_options=options)
        
        agent_browser.get(agent_site)
        agent_browser.maximize_window()
        #agent_browser.implicitly_wait(30)
        agent_site_login(agent_browser, agent_login, agent_password, agent_acc_number) #VEL-QA
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
        
        visitor_browser.get(visitor_site)  
        
        agent_wait_page_load_finished(agent_browser)
        time.sleep(20)
        visitor_browser.refresh()
        visitor_open_chat(visitor_browser)
        
        agent_pickup_call(agent_browser)

        #agent_open_LPVE_widget(agent_browser)

        agent_open_LPVE_widget(agent_browser)
        
        agent_close_advertisement_panel(agent_browser)
        
        agent_invite_visitor(agent_browser)
        
  
      
        # Sending the invitation message on the Agent side
        WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
        
        # Waiting for the invitation indicator on the Visitor side
        visitor_chat_vidyo_invitation_indicator = WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_notification_text')]")))
        
        # Visitor opens the widget after an invite
        WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'lp_slider')]"))).click()

        # id LPFRM_eb3f01-4a22-9d2e
        visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
        WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'join-button')]"))).click()
        visitor_browser.switch_to_default_content()
        time.sleep(20)

        # End the call at the Visitor side
        visitor_end_call(visitor_browser)

        email_msg = "Subject: Call successful on " + str(velp_server) #+ " at " + str(datetime.datetime.now())[:19]




    except StaleElementReferenceException as ex:
        print("StaleElementReferenceException exception: " + str(ex))
        email_msg = "Subject: Call StaleElementReferenceException on " + str(velp_server) + "\n\n" + str(ex) #" at " + str(datetime.datetime.now())[:19] + 
        pass
    except TimeoutException as ex:
        print("TimeOut exception in MAIN FLOW: " + str(ex))
        email_msg = "Subject: Call TimeoutException on " + str(velp_server) + "\n\n" + str(ex) #" at " + str(datetime.datetime.now())[:19] + "\n\n" + str(ex)
        pass
    except:
        email_msg = "Subject: Call FAILED on " + str(velp_server) + ".\n\nUnknown exception" #" at " + str(datetime.datetime.now())[:19] 
        pass    
    finally:
        #time.sleep(10)
        agent_browser.quit()
        #print(agent_browser)
        visitor_browser.quit()
        #print(visitor_browser)
        #time.sleep(10)
        print("Creating email ...")
        print(email_msg)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(email_username,email_password)
        server.sendmail(email_fromaddr, email_toaddrs, email_msg)
        server.quit()
        print("Email sent")

        print("Run " + str(counter) + " finished")
        counter = counter + 1
        time.sleep(20)
