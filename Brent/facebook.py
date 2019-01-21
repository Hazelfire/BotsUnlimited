from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from dateutil.relativedelta import relativedelta

def create_facebook_event(event):
    _browser_profile = webdriver.FirefoxProfile()
    _browser_profile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(firefox_profile=_browser_profile)
    driver.implicitly_wait(5)

    driver.get("https://www.facebook.com/groups/rmitprogramming.club/")

    # Log in
    username_field = driver.find_element_by_xpath('//*[@id="email"]')
    password_field = driver.find_element_by_xpath('//*[@id="pass"]')
    submit_button = driver.find_element_by_css_selector('input[type=submit]')

    username_field.send_keys(os.environ["FACEBOOK_USERNAME"])
    password_field.send_keys(os.environ["FACEBOOK_PASSWORD"])
    submit_button.click()

    driver.get("https://www.facebook.com/groups/rmitprogramming.club/")


    more = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/ul/li[4]/div/a")
    more.click()

    create_event = driver.find_element_by_css_selector(".fbReactComposerAttachmentSelector_EVENT > span:nth-child(1) > span:nth-child(2)")
    create_event.click()
    
    title_field = driver.find_element_by_css_selector('div[data-testid="create_event_title_input"] input')
    location_field = driver.find_element_by_css_selector('div[data-testid="create_event_location_input"] input')
    description_field = driver.find_element_css_selector('div[data-testid="create_event_dialogue"] div[role="presentation"]')
    start_time_inputs = driver.find_elements_by_css_selector('div[data-testid="event-create-dialogue-start-time"] input')
    start_date_input = start_time_inputs[0]
    start_time_hour = start_time_inputs[1]
    start_time_minutes = start_time_inputs[1]
    end_time_inputs = driver.find_elements_by_css_selector('div[data-testid="event-create-dialogue-end-time"] input')
    end_date_input = end_time_inputs[0]
    end_time_hour = end_time_inputs[1]
    end_time_minutes = end_time_inputs[1]
    confirm_button = driver.find_elements_by_css_selector('div[data-testid="event-create-dialogue-confirm-button"]')

    title_field.send_keys(event["summary"])
    location_field.send_keys(event["location"])
    description_field.send_keys(event["description"])

    start_time = parse(event["start"]["dateTime"])

    header = driver.find_elements_by_css_selector('.uiContextualLayerAboveLeft h2 span')
    next_button = driver.find_elements_by_css_selector('button[title="Next month"]')

    while True: 
        month = header[0].get_text()
        year = header[1].get_text()
        current_visual = datettime.strptime("%B %Y", month + " " + year)
        month_later = current_visual + relativedelta(months=+1)
        if month_later < start_time:
            next_button.click()
        else:
            break


