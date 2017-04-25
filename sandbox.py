"""
Created on 6 апр. 2017 г.

@author: pavlo.ivanov


if __name__ == '__main__':
    pass
"""
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
        # webdriver.find_element_by_xpath(xpath)
        # WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))) presence_of_element_located
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
        print("Unknown exception in EXISTENCE check: ")
        return False
    return True


# finally:
#    print("Unknown Exception wheen trying to fing the: " + str(xpath))
# print("Element NOT VISIBLE: " + str(xpath))
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
        print("Unknown exception in VISIBILITY check: ")
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
    while check_exists_by_xpath(agent_browser,
                                "//div[contains(@class,'lpview_dropdown_menu_container lpview_dropdown_menu_button actions_menu')]"):
        agent_engagement_dropdown_menu = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable([By.XPATH,"//div[contains(@class,'lpview_dropdown_menu_container lpview_dropdown_menu_button actions_menu')]"]))
        agent_engagement_dropdown_menu.click()
        if check_exists_by_xpath(agent_browser, "//div[contains(text(),'End engagement')]"):
            agent_dropdown_menu_end_engagement = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'End engagement')]")))
            agent_dropdown_menu_end_engagement.click()
            # agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class(),'lpview_okButton button dark_bg grey operative')]")))
            # agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class(),'lpview_okButton')]")))
            if not check_exists_by_xpath(agent_browser, "//*[@id='LP_undefined_2']/div/div[2]/div[3]/div[2]/span"):
                print("End Engagement OK button not found")
            agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='LP_undefined_2']/div/div[2]/div[3]/div[2]/span")))
            # agent_dropdown_menu_end_engagement_confirm_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'End engagement')]")))
            agent_dropdown_menu_end_engagement_confirm_button.click()
        else:
            agent_dropdown_menu_end_engagement = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class(),'lpview_hideConversation_engagement_menu_item LP_header_floating_actions_menu_item hideConversation')]")))
            agent_dropdown_menu_end_engagement.click()
    else:
        print("Conversation control drop-down not found")


def agent_cancel_vidyo_invitation(agent_browser):
    """
    This function requires the INVITE button to be pressed in IFrame 
    This function requires the Driver to be in Default Content
    :param agent_browser: Webdriver instance
    :return: none
    """
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Clicking CANCEL invitation button")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='pre-call-confirm']//button[contains(text(),'Cancel')]"))).click()
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()


def agent_send_invite_message(agent_browser):
    print("Searching the SEND MESSAGE button")
    if check_exists_by_xpath(agent_browser, 10, "//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"):
        print("SEND MESSAGE button FOUND")
        print("Trying to click the SEND MESSAGE button...")
        try:
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
        except:
            print("Exception: Agent SEND MESSAGE button NOT FOUND")
            print("Trying click Agent SEND MESSAGE button for one more time, by PRESENSE of the ELEMENT....")
            WebDriverWait(agent_browser, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                  "//div[contains(@id, 'LP_RichTextChatInputViewController')]//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
            # agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
            # agent_browser.execute_script("$('.iframeElement').contents().find('#invite-btn').click()")
            # agent_browser.execute_script("$find('.lpview_send_msg_button chat_input_button').click();")
            agent_browser.execute_script("$('.lpview_send_msg_button chat_input_button').trigger('click';")
    else:
        print("SEND MESSAGE button NOT FOUND")


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
        if check_exists_by_xpath(agent_browser, 1, "//div[@id='pre-call']//h1[contains(text(),'Detecting')]"):
            print("'Detecting video capability' FOUND")
        else:
            print("'Detecting video capability' NOT FOUND")
        agent_browser.switch_to.default_content()
        WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                              "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()

        print("Searching for 'Click invite to initialize a video call' string")
        WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
        if check_exists_by_xpath(agent_browser, 1,
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

        # Unable to establish connection. Please check your network. [CRLF] Refresh this widget to attempt to continue.


def agent_open_LPVE_widget(agent_browser):
    # agent_browser.switch_to.default_content()
    print("Checking existense LPVE widget button")
    # agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")

    # WebDriverWait(agent_browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='LP_MainWidgetsManagerViewController_1']//div[contains(@class,'custom_widget_icon')]")))
    while not check_exists_by_xpath(agent_browser, 5,
                                    "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon_pilot disabled selected')]"):
        try:
            WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH,
                                                                                        "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]")))
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                    "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()
        except StaleElementReferenceException:
            print("StaleElementReferenceException exception: " + str(ex))
            # agent_browser.execute_script("$('.custom_widget_icon').click()")
            print("Trying one more time....")
            WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH,
                                                                                        "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]")))
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                    "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]"))).click()
    print("Clicked the LPVE widges button")
    # agent_custom_vi_widget.click()


def agent_wait_page_load_finished(agent_browser):
    agent_upper_menu = WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='top-level-menu-switch']")))


def agent_pickup_call(agent_browser):
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@id='LP_QueueOrbView_1']//div[contains(text(), 'Accept')]"))).click()


def agent_close_advertisement_panel(agent_browser):
    if check_exists_by_xpath(agent_browser, 10, "//div[contains(@class, 'connection-profile-close-arrow')]"):
        print("Closing the Advertizement panel")
        WebDriverWait(agent_browser, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'connection-profile-close-arrow')]"))).click()


def agent_end_call(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                          "//*[contains(@id,'call-btn')]"))).click()
    agent_browser.switch_to.default_content()
    print("Clicked on Agent END CALL button")


def agent_mute_own_in_call_camera(agent_browser):
    print("Muting the Agent CAMERA")
    agent_browser.switch_to_frame(
        WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                          "//button[contains(@id,'video-btn')]"))).click()
    #agent_browser.execute_script("$('.iframeElement').contents().find('#video-btn').click()")
    print("Agent CAMERA muted")
    agent_browser.switch_to.default_content()
    time.sleep(1)


def agent_unmute_own_in_call_camera(agent_browser):
    print("Muting the Agent CAMERA")
    agent_browser.switch_to_frame(
        WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                          "//button[contains(@id,'video-btn')]"))).click()
    #agent_browser.execute_script("$('.iframeElement').contents().find('#video-btn').click()")
    print("Agent CAMERA muted")
    agent_browser.switch_to.default_content()
    time.sleep(1)


def agent_mute_own_in_call_microphone(agent_browser):
    print("Muting the Agent MICROPHONE")
    agent_browser.switch_to_frame(
        WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                          "//button[contains(@id,'mic-btn')]"))).click()
    #agent_browser.execute_script("$('.iframeElement').contents().find('#mic-btn').click()")
    print("Agent MICROPHONE muted")
    agent_browser.switch_to.default_content()
    time.sleep(1)


def agent_unmute_own_in_call_microphone(agent_browser):
    print("Muting the Agent MICROPHONE")
    agent_browser.switch_to_frame(
        WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
    WebDriverWait(agent_browser, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                          "//button[contains(@id,'mic-btn')]"))).click()
    #agent_browser.execute_script("$('.iframeElement').contents().find('#mic-btn').click()")
    print("Agent MICROPHONE unmuted")
    agent_browser.switch_to.default_content()
    time.sleep(1)


def agent_reinvite_call(agent_browser):
    # print("Switching to Agent IFRAME")
    # agent_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"))))
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

    # print("Switching the Agent to DEFAUL CONTENT")
    # agent_browser.switch_to.default_content()
    # agent_browser.execute_script("$('.iframeElement').contents().find('#resend-invite-btn').click()")
    # WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//div[contains(@id,'LP_CustomWidget') and contains(@style,'display: block')]//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
    # WebDriverWait(visitor_browser, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id, 'resend')]"))).click()

    print("Switching to Agent IFRAME")
    agent_browser.switch_to_frame(WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
    print("Resending invite")
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "// button[contains( @ id, 'resend-invite-btn')]"))).click()


    #agent_browser.execute_script("$('.iframeElement').contents().find('#resend-invite-btn').click()")

    """
    if check_exists_by_xpath(agent_browser, 5, "//button[contains(@id,'resend-invite-btn')]"):
        print("Agent RE-INVITE CALL button found")
        print("Clicking on the RE-INVITE CALL button")
        WebDriverWait(visitor_browser, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id, 'resend')]"))).click()
        #agent_browser.switch_to.default_content()
        #WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//div[contains(@id,'LP_CustomWidget') and contains(@style,'display: block')]//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]")))
        #WebDriverWait(visitor_browser, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id, 'resend-invite-btn')]"))).click()
    else:
        print("Agent RE-INVITE CALL button NOT FOUND")
        print("Trying to find the RE-INVITE CALL button for one more time...")
        try:
            agent_browser.switch_to.default_content()
            agent_browser.switch_to_frame(WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_CustomWidget') and contains(@style,'display: block')]//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"))))
            WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='call-btn']")))
        except:
            print("Agent END CALL button NOT FOUND after RE-INVITE after 2 search attempts")
    """
    agent_browser.switch_to.default_content()
    print("Agent: Sending the INVITE MESSAGE")
    agent_send_invite_message(agent_browser)
    print("Switching to Agent IFRAME")
    agent_browser.switch_to_frame(WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
    print("Checking that the Agent END CALL button is PRESENT")

    if check_exists_by_xpath(agent_browser, 5, "//button[@id='call-btn']"):
        print("Agent END CALL button found")
    else:
        print("Agent END CALL button NOT FOUND")
        print("Trying to find the END CALL button for one more time...")
        try:
            agent_browser.switch_to.default_content()
            agent_browser.switch_to_frame(WebDriverWait(agent_browser, 10).until(EC.presence_of_element_located((By.XPATH, agent_iframe_xpath))))
            WebDriverWait(agent_browser, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='call-btn']")))
        except:
            print("Agent END CALL button NOT FOUND after RE-INVITE after 2 search attempts")
    print("Switching back to Agent DEFAULT CONTENT")
    agent_browser.switch_to_default_content()


def agent_put_call_on_hold(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#hold-btn').click()")

    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()

    if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()='Put call on hold']"):
        print("Putting the call on hold...")
        WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='hold-menu']//button[text()='Put call on hold']"))).click()
        # Checking that the call is really put on hold
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()='Resume call']"):
            print("The AGENT call is NOW on HOLD")
        else:
            print("The AGENT call is still ONGOING")
            # Insert FAILURE here
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
    else:
        print("The AGENT call is ALREADY on HOLD")
        # probably one more attempt is needed here
    agent_browser.switch_to_default_content()
    """
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Putting the call on hold...")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='hold-menu']//button[text()='Put call on hold']"))).click()
    agent_browser.switch_to_default_content()
    """


def agent_resume_call(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#hold-btn').click()")

    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()

    if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()='Resume call']"):
        print("Resuming the call...")
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='hold-menu']//button[text()='Resume call']"))).click()
        # Checking that the call is really put on hold
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()='Put call on hold']"):
            print("The AGENT call is NOW RESUMED")
        else:
            print("The AGENT call is still ON HOLD")
            # Insert FAILURE here
            # probably one more attempt is needed here
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
    else:
        print("The AGENT call is ALREADY ONGOIND")

    agent_browser.switch_to_default_content()


def agent_mute_visitor_mic(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#hold-btn').click()")

    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()

    if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Mute visitor's mic\"]"):
        print("Putting the Visitor's MIC on MUTE...")
        WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='hold-menu']//button[text()=\"Mute visitor's mic\"]"))).click()
        # Checking that the call is really put on hold
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Unmute visitor's mic\"]"):
            print("The Visitor's MIC is NOW on MUTE")
        else:
            print("The Visitor's MIC is still ON")
            # Insert FAILURE here
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
    else:
        print("The Visitor's MIC is ALREADY MUTED")
        # probably one more attempt is needed here
    agent_browser.switch_to_default_content()
    """
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Putting the call on hold...")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='hold-menu']//button[text()='Put call on hold']"))).click()
    agent_browser.switch_to_default_content()
    """


def agent_unmute_visitor_mic(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#hold-btn').click()")

    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()

    if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Unmute visitor's mic\"]"):
        print("UNMUTING the Visitor's MIC...")
        WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='hold-menu']//button[text()=\"Unmute visitor's mic\"]"))).click()
        # Checking that the call is really put on hold
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Mute visitor's mic\"]"):
            print("The Visitor's MIC is now UNMUTED")
        else:
            print("The Visitor's MIC is still ON MUTE")
            # Insert FAILURE here
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
    else:
        print("The Visitor's MIC is ALREADY UNMUTED")
        # probably one more attempt is needed here
    agent_browser.switch_to_default_content()
    """
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Putting the call on hold...")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='hold-menu']//button[text()='Put call on hold']"))).click()
    agent_browser.switch_to_default_content()
    """


def agent_mute_visitor_cam(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#hold-btn').click()")

    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()

    if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Mute visitor's cam\"]"):
        print("Resuming the call...")
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='hold-menu']//button[text()=\"Mute visitor's cam\"]"))).click()
        # Checking that the call is really put on hold
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Unmute visitor's cam\"]"):
            print("The Visitor's CAM is NOW on MUTE")
        else:
            print("The Visitor's CAM is still ON")
            # Insert FAILURE here
            # probably one more attempt is needed here
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
    else:
        print("The Visitor's CAM is ALREADY MUTED")
    agent_browser.switch_to_default_content()


def agent_unmute_visitor_cam(agent_browser):
    # agent_browser.execute_script("$('.iframeElement').contents().find('#hold-btn').click()")

    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()

    if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Unmute visitor's cam\"]"):
        print("Resuming the VISITOR's CAMERA...")
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='hold-menu']//button[text()=\"Unmute visitor's cam\"]"))).click()
        # Checking that the call is really put on hold
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
        if check_exists_by_xpath(agent_browser, 5, "//div[@id='hold-menu']//button[text()=\"Mute visitor's cam\"]"):
            print("The Visitor's CAM is now RESUMED")
        else:
            print("The Visitor's CAM is still ON MUTE")
            # Insert FAILURE here
            # probably one more attempt is needed here
        WebDriverWait(agent_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hold-btn')]"))).click()
    else:
        print("The Visitor's CAM is ALREADY UNMUTED")
    agent_browser.switch_to_default_content()


def agent_click_menu_button(agent_browser):
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Clicking HAMBURGER (MENU) button")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'hamburger-btn')]"))).click()
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()


def agent_click_settings_button(agent_browser):
    """
    This function requires the menu to be open by agent_click_menu_button()
    :param agent_browser: Webdriver instance
    :return: none
    """
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Clicking SETTINGS button")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'settings-button')]"))).click()
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()


def agent_click_done_in_settings(agent_browser):
    """
    This function requires the Settings dialogue to be open by agent_click_settings_button() 
    :param agent_browser: Webdriver instance
    :return: none
    """
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Clicking DONE button")
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'done-button')]"))).click()
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()


def agent_select_camera_in_dropdown_by_index(agent_browser, index):
    """
    This function requires the Settings dialogue to be open by agent_click_settings_button()
    :param agent_browser: Webdriver instance
    :param index: 
    :return: True if item exists and selected, False otherwise 
    """
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Checking that CAMERA SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'cameraSelect')]/option[" + str(index) + "]"
    #if check_exists_by_xpath("//select[contains(@id,'cameraSelect')]"):
        #WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).selectByIndex(index)
    #WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).selectByIndex(index)
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).click()
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in Camera selector")
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()



def agent_select_microphone_in_dropdown_by_index(agent_browser, index):
    """
    This function requires the Settings dialogue to be open by agent_click_settings_button()
    :param agent_browser: Webdriver instance
    :param index: 
    :return: none 
    """
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Checking that MICROPHONE SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'microphoneSelect')]/option[" + str(index) + "]"
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'microphoneSelect')]"))).click()
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in MICROPHONE selector")
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()


def agent_select_speaker_in_dropdown_by_index(agent_browser, index):
    """
    This function requires the Settings dialogue to be open by agent_click_settings_button()
    :param agent_browser: Webdriver instance
    :param index: 
    :return: none 
    """
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Checking that SPEAKER SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'speakerSelect')]/option[" + str(index) + "]"
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'speakerSelect')]"))).click()
    WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in SPEAKER selector")
    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()



def agent_download_diagnostic_reports_from_incall_settings(agent_browser):
    """
    This function requires the Settings dialogue to be open by agent_click_settings_button()
    :param agent_browser: 
    :return: 
    """
    print("Downloading the DIAGNOSTICS from INCALL SETTINGS dialogue")
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Clicking the Download diagnostic reports button")

    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='settings-content']//a[@id='settings-logs-button']"))).click()

    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()



def agent_download_diagnostic_reports_from_postcall_settings(agent_browser):
    """
    This function requires the Settings dialogue to be open by agent_click_settings_button()
    :param agent_browser: 
    :return: 
    """
    print("Downloading the DIAGNOSTICS from INCALL SETTINGS dialogue")
    print("Switching to IFrame")
    WebDriverWait(agent_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))
    print("Clicking the Download diagnostic reports button")

    WebDriverWait(agent_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='post-call']//a[@id='post-logs-button']"))).click()

    print("Switching to Default Contents")
    agent_browser.switch_to_default_content()


def visitor_open_chat(visitor_browser):

    WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@class,'LPMimage')]"))).click()
    WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_top-text')]")))
    if check_exists_by_xpath(visitor_browser,"5","//div[contains(@id,'lab') and contains(text(),'From')]"):
        visitor_browser.refresh()
        WebDriverWait(visitor_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@class,'LPMimage')]"))).click()
        WebDriverWait(visitor_browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_top-text')]")))

def visitor_open_slider(visitor_browser):
    print("Visitor: searching for the invitation notification...")
    visitor_chat_vidyo_invitation_indicator = WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_notification_text')]")))
    # Visitor opens the widget after an invite
    print("Visitor: opening the slider...")
    WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'lp_slider')]"))).click()


def visitor_press_join_button(visitor_browser):
    visitor_browser.switch_to.frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'LPFRM')]"))))
    WebDriverWait(visitor_browser, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'join-button')]"))).click()
    visitor_browser.switch_to.default_content()


def visitor_mute_own_in_call_microphone(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, visitor_iframe_xpath))))
    print("Checking that the Visitor MICROPHONE EXISTS and NOT MUTED")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"):
        try:
            print("Trying to MUTE the Visitor MICROPHONE")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"))).click()

        except:
            print("Exception: UNMUTED Visitor MICROPHONE NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5,
                                 "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
            print("Visitor MICROPHONE is already MUTED")
        else:
            print("Visitor MICROPHONE control NOT FOUND")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
        print("Visitor MICROPHONE is MUTED")
    else:
        print("Visitor MICROPHONE is NOT MUTED")
        print("Trying to find the MUTED Visitor MICROPHONE for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]")))
        except:
            print("Visitor MICROPHONE control NOT FOUND in MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")
    visitor_browser.switch_to_default_content()


def visitor_unmute_own_in_call_microphone(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, visitor_iframe_xpath))))
    print("Checking that the Visitor MICROPHONE EXISTS and  MUTED")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
        try:
            print("Trying to UN-MUTE the Visitor MICROPHONE")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"))).click()

        except:
            print("Exception: MUTED Visitor MICROPHONE NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5,
                                 "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"):
            print("Visitor MICROPHONE is already UN-MUTED")
        else:
            print("Visitor MICROPHONE control NOT FOUND")
    # Checking that MIC has changed its state to UN-MUTED
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]"):
        print("Visitor MICROPHONE is UNMUTED")
    else:
        print("Visitor MICROPHONE is STILL MUTED")
        print("Trying to find the UNMUTED Visitor MICROPHONE for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'mic-btn')]/i[contains(@class,'lpicon-mic-on')]")))
        except:
            print("Visitor MICROPHONE control NOT FOUND in UN-MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")
    visitor_browser.switch_to_default_content()


def visitor_mute_own_in_call_camera(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, visitor_iframe_xpath))))
    print("Checking that the Visitor CAMERA EXISTS and NOT MUTED")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"):
        try:
            print("Trying to MUTE the Visitor CAMERA")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"))).click()

        except:
            print("Exception: UNMUTED Visitor CAMERA NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5,
                                 "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-mic-off red-icon')]"):
            print("Visitor CAMERA is already MUTED")
        else:
            print("Visitor CAMERA control NOT FOUND")
    print("Checking that the CAMERA has been really MUTED...")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"):
        print("Visitor CAMERA is MUTED")
    else:
        print("Visitor CAMERA is NOT MUTED")
        print("Trying to find the MUTED Visitor CAMERA for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]")))
        except:
            print("Visitor CAMERA control NOT FOUND in MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")
    visitor_browser.switch_to_default_content()


def visitor_unmute_own_in_call_camera(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, visitor_iframe_xpath))))
    print("Checking that the Visitor CAMERA EXISTS and  MUTED")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"):
        try:
            print("Trying to UN-MUTE the Visitor CAMERA")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"))).click()

        except:
            print("Exception: MUTED Visitor CAMERA NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-off red-icon')]"))).click()
    else:
        if check_exists_by_xpath(visitor_browser, 5,
                                 "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"):
            print("Visitor CAMERA is already UN-MUTED")
        else:
            print("Visitor CAMERA control NOT FOUND")
    # Checking that MIC has changed its state to UN-MUTED
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]"):
        print("Visitor CAMERA is UNMUTED")
    else:
        print("Visitor CAMERA is STILL MUTED")
        print("Trying to find the UNMUTED Visitor CAMERA for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='call-controls']/button[contains(@id,'video-btn')]/i[contains(@class,'lpicon-video-on')]")))
        except:
            print("Visitor CAMERA control NOT FOUND in UN-MUTED state after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")
    visitor_browser.switch_to_default_content()


def visitor_end_call(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, visitor_iframe_xpath))))
    print("Checking that the Visitor END CALL button EXISTS")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"):
        try:
            print("Trying to END the call from Visitor side")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"))).click()

        except:
            print("Exception: END CALL button for Visitor NOT FOUND")
            print("Trying one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"))).click()
    else:
        print("Visitor END CALL button not found")

    # Checking that Visitor screen shows 'The video session has ended'
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='post-call']/div[contains(@id,'post-call-content')]/h3/span[contains(text(),'The video session has ended')]"):
        print("Visitor call has been ENDED with 'The video session has ended'")
    else:
        print("Visitor 'The video session has ended' NOT FOUND")
        print("Trying to find the Visitor 'The video session has ended' for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='post-call']/div[contains(@id,'post-call-content')]/h3/span[contains(text(),'The video session has ended')]")))
        except:
            print("Visitor 'The video session has ended' NOT FOUND after 2 search attempts")

    # Checking that Visitor screen shows 'REJOIN' button
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"):
        print("Visitor call has been ENDED and REJOIN button displayed")
    else:
        print("Visitor REJOIN button NOT FOUND")
        print("Trying to find the Visitor REJOIN button for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]")))
        except:
            print("Visitor REJOIN button NOT FOUND after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")
    visitor_browser.switch_to_default_content()


def visitor_rejoin_call(visitor_browser):
    print("Switching to Visitor IFRAME")
    visitor_browser.switch_to_frame(WebDriverWait(visitor_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, visitor_iframe_xpath))))
    print("Checking that the Visitor REJOIN button is PRESENT")
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"):
        try:
            print("Trying to click Visitor REJOIN button")
            WebDriverWait(visitor_browser, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"))).click()

        except:
            print("Exception: Visitor REJOIN button NOT FOUND")
            print("Trying click Visitor REJOIN button for one more time....")
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='post-call']/div[contains(@id,'post-call-content')]//button[contains(@id,'rejoin-call-btn')]"))).click()
    else:
        print("Visitor REJOIN button NOT FOUND")
    # Checking that Visitor REJOINED the call (END CALL button present)
    if check_exists_by_xpath(visitor_browser, 5,
                             "//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]"):
        print("Visitor Re-Joined the call")
    else:
        print("Visitor could not REJOIN the call, END CALL button NOT FOUND")
        print("Trying to find the END CALL button for one more time...")
        try:
            WebDriverWait(visitor_browser, timeout).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='bottom-control-bar']//button[contains(@id,'call-btn')]/i[contains(@class,'lpicon-phone')]")))
        except:
            print("Visitor END CALL button NOT FOUND after REJOIN after 2 search attempts")
    print("Switching back to Visitor DEFAULT CONTENT")
    visitor_browser.switch_to_default_content()


def visitor_click_done_in_settings(visitor_browser):
    """
    This function requires the Settings dialogue to be open by visitor_click_settings_button() 
    :param visitor_browser: Webdriver instance
    :return: none
    """
    print("Switching to IFrame")
    WebDriverWait(visitor_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, visitor_iframe_xpath)))
    print("Clicking DONE button")
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Done')]"))).click()
    print("Switching to Default Contents")
    visitor_browser.switch_to_default_content()



def visitor_click_settings_button(visitor_browser):


    """
    This function requires the menu to be open by visitor_click_menu_button()
    :param visitor_browser: Webdriver instance
    :return: none
    """
    print("Switching to IFrame")
    WebDriverWait(visitor_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, visitor_iframe_xpath)))
    print("Clicking SETTINGS button")
    WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'settings-button')]"))).click()
    print("Switching to Default Contents")
    visitor_browser.switch_to_default_content()


def visitor_select_camera_in_dropdown_by_index(visitor_browser, index):


    """
    This function requires the Settings dialogue to be open by visitor_click_settings_button()
    :param visitor_browser: Webdriver instance
    :param index: 
    :return: True if item exists and selected, False otherwise 
    """
    print("Switching to IFrame")
    WebDriverWait(visitor_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, visitor_iframe_xpath)))
    print("Checking that CAMERA SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'cameraSelect')]/option[" + str(index) + "]"
    # if check_exists_by_xpath("//select[contains(@id,'cameraSelect')]"):
    # WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).selectByIndex(index)
    # WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).selectByIndex(index)
    WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).click()
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in Camera selector")
    print("Switching to Default Contents")
    visitor_browser.switch_to_default_content()


def visitor_select_microphone_in_dropdown_by_index(visitor_browser, index):
    """
    This function requires the Settings dialogue to be open by visitor_click_settings_button()
    :param visitor_browser: Webdriver instance
    :param index: 
    :return: none 
    """
    print("Switching to IFrame")
    WebDriverWait(visitor_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, visitor_iframe_xpath)))
    print("Checking that MICROPHONE SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'microphoneSelect')]/option[" + str(index) + "]"
    WebDriverWait(visitor_browser, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'microphoneSelect')]"))).click()
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in MICROPHONE selector")
    print("Switching to Default Contents")
    visitor_browser.switch_to_default_content()


def visitor_select_speaker_in_dropdown_by_index(visitor_browser, index):
    """
    This function requires the Settings dialogue to be open by visitor_click_settings_button()
    :param visitor_browser: Webdriver instance
    :param index: 
    :return: none 
    """
    print("Switching to IFrame")
    WebDriverWait(visitor_browser, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, visitor_iframe_xpath)))
    print("Checking that SPEAKER SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'speakerSelect')]/option[" + str(index) + "]"
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'speakerSelect')]"))).click()
    WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in SPEAKER selector")
    print("Switching to Default Contents")
    visitor_browser.switch_to_default_content()



def agent_enable_video(agent_browser):
    active_video_button = "//button[contains(@class,'active') and contains(@id,'video-toggle-button')]"
    video_toggle_button = 'video-toggle-button'
    for_this_call_only = "//p[contains(@class,'text-muted')]"

    print("Switching to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()
    print("Switching to Agent IFRAME")
    WebDriverWait(agent_browser, default_timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))

    if check_exists_by_xpath(agent_browser, small_timeout, active_video_button):
        print("Agent VIDEO BUTTON is already enabled")
    else:
        print("Checking that the Agent VIDEO BUTTON EXISTS and 'DISABLED'")
        try:
            agent_browser.find_element(By.ID, video_toggle_button).click()
            print("Agent VIDEO BUTTON has been clicked")
            # bug work-around
            agent_browser.find_element(By.XPATH, for_this_call_only).click()
            time.sleep(1)
        except:
            print("Exception: Agent 'DISABLED' VIDEO BUTTON NOT FOUND")
    print("Switching back to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()


def agent_disable_video(agent_browser):
    active_video_button = "//button[contains(@class,'active') and contains(@id,'video-toggle-button')]"
    video_toggle_button = 'video-toggle-button'
    for_this_call_only = "//p[contains(@class,'text-muted')]"

    print("Switching to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()
    print("Switching to Agent IFRAME")
    WebDriverWait(agent_browser, default_timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))

    if check_exists_by_xpath(agent_browser, small_timeout, active_video_button):
        print("Checking that the Agent VIDEO BUTTON EXISTS and 'ENABLED'")
        try:
            agent_browser.find_element(By.ID, video_toggle_button).click()
            print("Agent VIDEO BUTTON has been clicked")
            # bug work-around
            agent_browser.find_element(By.XPATH, for_this_call_only).click()
            time.sleep(1)
        except:
            print("Exception: Agent 'ENABLED' VIDEO BUTTON NOT FOUND")
    else:
        print("Agent VIDEO BUTTON is already disabled")

    print("Switching back to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()


def agent_enable_audio(agent_browser):
    active_video_button = "//button[contains(@class,'active') and contains(@id,'microphone-toggle-button')]"
    microphone_toggle_button = 'microphone-toggle-button'
    for_this_call_only = "//p[contains(@class,'text-muted')]"

    print("Switching to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()
    print("Switching to Agent IFRAME")
    WebDriverWait(agent_browser, default_timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))

    if check_exists_by_xpath(agent_browser, small_timeout, active_video_button):
        print("Agent MICROPHONE BUTTON is already enabled")
    else:
        print("Checking that the Agent MICROPHONE BUTTON EXISTS and 'DISABLED'")
        try:
            agent_browser.find_element(By.ID, microphone_toggle_button).click()
            print("Agent MICROPHONE BUTTON has been clicked")
            # bug work-around
            agent_browser.find_element(By.XPATH, for_this_call_only).click()
            time.sleep(1)
        except:
            print("Exception: Agent 'DISABLED' MICROPHONE BUTTON NOT FOUND")

    print("Switching back to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()


def agent_disable_audio(agent_browser):
    active_video_button = "//button[contains(@class,'active') and contains(@id,'microphone-toggle-button')]"
    microphone_toggle_button = 'microphone-toggle-button'
    for_this_call_only = "//p[contains(@class,'text-muted')]"

    print("Switching to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()
    print("Switching to Agent IFRAME")
    WebDriverWait(agent_browser, default_timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))

    if check_exists_by_xpath(agent_browser, small_timeout, active_video_button):
        print("Checking that the Agent MICROPHONE BUTTON EXISTS and 'ENABLED'")
        try:
            agent_browser.find_element(By.ID, microphone_toggle_button).click()
            print("Agent MICROPHONE BUTTON has been clicked")
            # bug work-around
            agent_browser.find_element(By.XPATH, for_this_call_only).click()
            time.sleep(1)
        except:
            print("Exception: Agent 'ENABLED' MICROPHONE BUTTON NOT FOUND")
    else:
        print("Agent MICROPHONE BUTTON is already disabled")

    print("Switching back to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()


def agent_download_diagnostic_reports_from_precall(agent_browser):
    diagnostic_reports_button = "pre-logs-button"
    diagnostic_reports_title = "//a[contains(@title,'Download zip')]"

    print("Switching to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()
    print("Switching to Agent IFRAME")
    WebDriverWait(agent_browser, default_timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))

    print("Checking that the Agent REPORT BUTTON Exists")
    if check_exists_by_xpath(agent_browser, default_timeout, diagnostic_reports_title):
        try:
            agent_browser.find_element(By.ID, diagnostic_reports_button).click()
            print("Agent REPORT BUTTON has been clicked")
        except:
            print("Exception: Agent REPORT BUTTON NOT FOUND")
    else:
        print("Exception: Agent REPORT BUTTON NOT FOUND")

    print("Switching back to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()



def guest_join_call(guest_browser):
    """
    
    :param guest_browser: 
    :return: 
    """
    print("Guest joins the call...")
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='guest-join']//input"))).send_keys("LP_Guest")
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'join-button')]"))).click()



def guest_click_done_in_settings(guest_browser):
    """
    This function requires the Settings dialogue to be open by guest_click_settings_button() 
    :param guest_browser: Webdriver instance
    :return: none
    """
    print("Clicking Guest DONE button")
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Done')]"))).click()




def guest_click_settings_button(guest_browser):


    """
    This function requires the menu to be open by guest_click_menu_button()
    :param guest_browser: Webdriver instance
    :return: none
    """
    print("Clicking Guest SETTINGS button")
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'settings-button')]"))).click()



def guest_select_camera_in_dropdown_by_index(guest_browser, index):


    """
    This function requires the Settings dialogue to be open by guest_click_settings_button()
    :param guest_browser: Webdriver instance
    :param index: 
    :return: True if item exists and selected, False otherwise 
    """
    print("Checking that Guest CAMERA SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'cameraSelect')]/option[" + str(index) + "]"
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'cameraSelect')]"))).click()
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in Camera selector")



def guest_select_microphone_in_dropdown_by_index(guest_browser, index):
    """
    This function requires the Settings dialogue to be open by guest_click_settings_button()
    :param guest_browser: Webdriver instance
    :param index: 
    :return: none 
    """
    print("Checking that Guest MICROPHONE SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'microphoneSelect')]/option[" + str(index) + "]"
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'microphoneSelect')]"))).click()
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in MICROPHONE selector")



def guest_select_speaker_in_dropdown_by_index(guest_browser, index):
    """
    This function requires the Settings dialogue to be open by guest_click_settings_button()
    :param guest_browser: Webdriver instance
    :param index: 
    :return: none 
    """
    print("Checking that Guest SPEAKER SELECTOR exists")
    select_option_xpath = "//select[contains(@id,'speakerSelect')]/option[" + str(index) + "]"
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'speakerSelect')]"))).click()
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, select_option_xpath))).click()
    print("SELECTED item " + str(index) + " in SPEAKER selector")



def guest_end_call(guest_browser):


    """
    This function requires the menu to be open by guest_click_menu_button()
    :param guest_browser: Webdriver instance
    :return: none
    """
    print("Clicking Guest END CALL button")
    WebDriverWait(guest_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'call-btn')]"))).click()



def agent_get_invitation_link(agent_browser):
    global guest_link
    get_link_button = "//button[contains(@class,'btn btn-copy')]"
    guest_link_input = "guestLinkInput"
    close_link_button = "//button[contains(@class,'btn btn-link close')]"

    #print("Switching to Agents DEFAULT CONTENT")
    #agent_browser.switch_to_default_content()
    agent_click_menu_button(agent_browser)
    print("Switching to Agent IFRAME")
    WebDriverWait(agent_browser, default_timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, agent_iframe_xpath)))

    print("Checking that the Agent LINK BUTTON Exists")
    if check_exists_by_xpath(agent_browser, small_timeout, get_link_button):
        try:
            agent_browser.find_element(By.XPATH, get_link_button).click()
            print("Agent LINK BUTTON has been clicked")
        except:
            print("Exception: Agent LINK BUTTON NOT FOUND")
    else:
        print("Exception: Agent LINK BUTTON NOT FOUND")

    WebDriverWait(agent_browser, small_timeout).until(
        EC.visibility_of_element_located((By.ID, guest_link_input)))
    print("Trying to get GUEST LINK value ")
    try:
        guest_link = agent_browser.find_element(By.ID, guest_link_input).get_attribute('value')
        print("GUEST LINK has been extracted")
    except Exception as ex:
        print("Exception: Agent GUEST LINK NOT FOUND : " + str(ex))

    WebDriverWait(agent_browser, small_timeout).until(
        EC.visibility_of_element_located((By.XPATH, close_link_button)))
    try:
        agent_browser.find_element(By.XPATH, close_link_button).click()
        print("Guest link window has been Closed")
    except:
        print("Exception: Agent CLOSE LINK BUTTON NOT FOUND")

    print("Switching back to Agents DEFAULT CONTENT")
    agent_browser.switch_to_default_content()
    # Closing the menu on the Agent side
    agent_click_menu_button(agent_browser)


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


# driver = webdriver.Chrome(chrome_options=options)

# CONFIG

timeout = 30
default_timeout = 10
small_timeout = 2
counter = 1

agent_iframe_xpath = "//div[contains(@class,'lpview_widget right_pane_widget_wrapper_iframe') and contains(@style,'display: block')]//iframe[contains(@class,'lpview_table_items_placeholder table_items_placeholder lpview_iframe_tag iframeElement')]"
visitor_iframe_xpath = "//iframe[contains(@id,'LPFRM')]"

guest_link = None

while counter == 1:
    print("Run " + str(counter) + " started")
    try:
        options = webdriver.ChromeOptions()
        # print(options)
        # options.addArguments("start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-web-security")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--mute-audio")

        options.add_experimental_option("prefs", {'download.prompt_for_download': False,
                                                  'directory_upgrade': True,
                                                  'download.default_directory': 'D:/'})

        # print(options.to_capabilities()) --disable-web-security
        # agent_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        # agent_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=options.to_capabilities())
        agent_browser = webdriver.Chrome(chrome_options=options)

        agent_browser.implicitly_wait(small_timeout)
        agent_browser.set_script_timeout(small_timeout)

        agent_browser.get('https://va-a.authentication.liveperson.net/')
        agent_browser.maximize_window()
        # agent_browser.implicitly_wait(30)
        agent_site_login(agent_browser, 'Agent3', 'Agent123', '54424706')  # VEL-QA
        # agent_site_login(agent_browser, 'Agent2', 'Agent123', '54424706')  # VEL-QA
        # agent_site_login(agent_browser, 'Bohdan', 'Bohdan123', '57877913') # VEL

        """
        visitor_options = webdriver.ChromeOptions()
        #print(options)
        #options.addArguments("start-maximized")
        visitor_options.add_argument("--disable-notifications")
        visitor_options.add_argument("--disable-web-security")
        visitor_options.add_argument("--use-fake-ui-for-media-stream")
        """

        # visitor_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        visitor_browser = webdriver.Chrome(chrome_options=options)

        visitor_browser.get('https://pavelivanov1.github.io/LPVE/')  # VEL-QA
        # visitor_browser.get('https://ishapiro11.github.io/liveperson-visitor/ilanaaws.htm') # VEL
        # time.sleep(5)

        agent_wait_page_load_finished(agent_browser)

        """
        visitor_LE_chat_tab = WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class,'LPMimage')]")))
        visitor_LE_chat_tab.click()
        """

        # visitor_browser.refresh()


        # visitor_chat_caption = WebDriverWait(visitor_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'lp_top-text')]")))
        visitor_open_chat(visitor_browser)

        # agent_incoming_call = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_QueueOrbView_1']//div[contains(text(), 'Accept')]")))
        # agent_pickup_call = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_QueueOrbView_1']//div[contains(text(), 'Accept')]"))).click()
        agent_pickup_call(agent_browser)

        # agent_open_LPVE_widget(agent_browser)
        """
        alpve = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@id='LP_MainWidgetsManagerViewController_1']//div[contains(@class,'custom_widget_icon')]")))
        alpve = WebDriverWait(agent_browser, timeout).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'LP_MainWidgetsManagerViewController')]//div[contains(@class,'custom_widget_icon')]")))
        alpve.click()
        """
        agent_open_LPVE_widget(agent_browser)

        agent_close_advertisement_panel(agent_browser)

        agent_enable_video(agent_browser)

        agent_disable_video(agent_browser)

        agent_enable_video(agent_browser)

        agent_enable_audio(agent_browser)

        agent_disable_audio(agent_browser)

        agent_enable_audio(agent_browser)

        agent_download_diagnostic_reports_from_precall(agent_browser)

        agent_invite_visitor(agent_browser)

        agent_cancel_vidyo_invitation(agent_browser)

        agent_invite_visitor(agent_browser)

        # Mute camera id="video-toggle-button"
        # Agent, Before call
        # agent_browser.execute_script("$('.iframeElement').contents().find('#video-toggle-button').click()")
        # agent_browser.execute_script("$('.iframeElement').contents().find('#video-toggle-button').click()")
        # Mute mic id="microphone-toggle-button"
        # agent_browser.execute_script("$('.iframeElement').contents().find('#microphone-toggle-button').click()")
        # agent_browser.execute_script("$('.iframeElement').contents().find('#microphone-toggle-button').click()")


        # Sending the invitation message on the Agent side
        #WebDriverWait(agent_browser, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'lpview_send_msg_button chat_input_button visible active')]"))).click()
        agent_send_invite_message(agent_browser)

        # Waiting for the invitation indicator on the Visitor side

        visitor_open_slider(visitor_browser)


        '''
        agent_invite_button = WebDriverWait(agent_browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@id,'invite-btn')]")))
        agent_invite_button = WebDriverWait(agent_browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id,'invite-btn')]")))
        print(agent_invite_button)
        agent_invite_button.click()
        '''

        # id LPFRM_eb3f01-4a22-9d2e
        visitor_press_join_button(visitor_browser)

        print("Getting the GUEST invitation link...")
        agent_get_invitation_link(agent_browser)

        print("Rinning the GUEST browser...")
        guest_browser = webdriver.Chrome(chrome_options=options)
        print("Opening the GUEST link page...")
        guest_browser.get(guest_link)
        time.sleep(1)

        guest_join_call(guest_browser)
        guest_click_settings_button(guest_browser)
        guest_select_camera_in_dropdown_by_index(guest_browser, 1)
        guest_select_microphone_in_dropdown_by_index(guest_browser, 1)
        guest_select_speaker_in_dropdown_by_index(guest_browser, 1)
        guest_click_done_in_settings(guest_browser)

        #time.sleep(5)

        visitor_mute_own_in_call_microphone(visitor_browser)
        visitor_mute_own_in_call_camera(visitor_browser)

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
        visitor_unmute_own_in_call_camera(visitor_browser)

        agent_put_call_on_hold(agent_browser)
        #time.sleep(1)

        agent_resume_call(agent_browser)
        #time.sleep(1)

        agent_mute_visitor_mic(agent_browser)
        #time.sleep(1)

        agent_mute_visitor_cam(agent_browser)
        #time.sleep(1)

        agent_unmute_visitor_cam(agent_browser)
        #time.sleep(1)

        agent_unmute_visitor_mic(agent_browser)
        #time.sleep(1)

        agent_click_menu_button(agent_browser)
        #time.sleep(1)

        agent_click_settings_button(agent_browser)
        #time.sleep(1)
        agent_select_camera_in_dropdown_by_index(agent_browser, 1)
        #time.sleep(1)
        agent_select_microphone_in_dropdown_by_index(agent_browser, 1)
        #time.sleep(1)
        agent_select_speaker_in_dropdown_by_index(agent_browser, 1)
        #time.sleep(1)
        agent_download_diagnostic_reports_from_incall_settings(agent_browser)
        #time.sleep(1)
        agent_click_done_in_settings(agent_browser)
        #time.sleep(1)
        agent_click_menu_button(agent_browser)



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

        # End the call at the Visitor side
        visitor_end_call(visitor_browser)
        # print("Clicked on Visitor END CALL button")

        # ReJoin the call at the Visitor side
        visitor_rejoin_call(visitor_browser)

        visitor_click_settings_button(visitor_browser)
        visitor_select_camera_in_dropdown_by_index(visitor_browser, 1)
        visitor_select_microphone_in_dropdown_by_index(visitor_browser, 1)
        visitor_select_speaker_in_dropdown_by_index(visitor_browser, 1)
        visitor_click_done_in_settings(visitor_browser)

        # End the call at the Agent side
        agent_browser.execute_script("$('.iframeElement').contents().find('#call-btn').click()")
        print("Clicked on Agent END CALL button")

        time.sleep(5)
        print("Agent: RE-INVITING...")
        agent_reinvite_call(agent_browser)
        time.sleep(5)
        visitor_rejoin_call(visitor_browser)
        time.sleep(5)


        #guest_end_call(guest_browser)

        agent_get_invitation_link(agent_browser)

        print("Rinning the GUEST browser...")
        #guest_browser = webdriver.Chrome(chrome_options=options)
        print("Opening the GUEST link page...")
        guest_browser.get(guest_link)
        time.sleep(1)

        guest_join_call(guest_browser)
        """
        guest_click_settings_button(guest_browser)
        guest_select_camera_in_dropdown_by_index(guest_browser, 1)
        guest_select_microphone_in_dropdown_by_index(guest_browser, 1)
        guest_select_speaker_in_dropdown_by_index(guest_browser, 1)
        guest_click_done_in_settings(guest_browser)
        """

        time.sleep(5)

        guest_end_call(guest_browser)

        print("Agent: ENDING THE CALL...")
        agent_end_call(agent_browser)
        agent_download_diagnostic_reports_from_postcall_settings(agent_browser)
        time.sleep(5)

        print("\n\nAll tests are DONE\n\n")

    except StaleElementReferenceException as ex:
        print("StaleElementReferenceException exception: " + str(ex))
        pass
    except TimeoutException as ex:
        print("TimeOut exception in MAIN FLOW: " + str(ex))
        pass
    except:
        print("Unknown exception")
        pass
    finally:
        # time.sleep(10)
        agent_browser.quit()
        # print(agent_browser)
        visitor_browser.quit()
        # print(visitor_browser)
        try:
            guest_browser.quit()
        except:
            print("Guest Browser has no instance and cannot be closed")
        # time.sleep(10)
        print("Run " + str(counter) + " finished")
        counter = counter + 1
