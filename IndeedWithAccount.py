import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import time
import random
import math


# note: this if you already have an account / if you don't want to use your account; I will make another class


Loading_time = random.randint(5, 13)


def openbrowser():
    global browser
    current_directory = os.getcwd()
    path_to_chromedriver = current_directory + '/chromedriver'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)


def navigateToSite(username, password, search_id, search_loc):
    browser.get('https://www.indeed.ca')  # start the site
    time.sleep(Loading_time)
    browser.find_element_by_class_name(
        'gnav-LoggedOutAccountLink-text').click()
    time.sleep(Loading_time)
    # inout the username
    uNameBar = browser.find_element_by_xpath('//*[@id="login-email-input"]')
    uNameBar.clear()
    uNameBar.send_keys(username)
    time.sleep(Loading_time)
    # input the password
    passwdBar = browser.find_element_by_xpath(
        '//*[@id="login-password-input"]')
    passwdBar.clear()
    passwdBar.send_keys(password)
    time.sleep(Loading_time)
    # click login/ submit
    browser.find_element_by_xpath('//*[@id="login-submit-button"]').click()
    # you should be signed in by now # therefore: will navigate to search menu
    # input the search_id
    jobSearch = browser.find_element_by_xpath('//*[@id="text-input-what"]')
    jobSearch.clear()
    jobSearch.send_keys(search_id)
    time.sleep(Loading_time)
    # input the location of the search
    locSearch = browser.find_element_by_xpath('//*[@id="text-input-where"]')
    locSearch.clear()
    locSearch.send_keys(search_id)
    time.sleep(Loading_time)
    # click search / go
    browser.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
    time.sleep(Loading_time)


def checkJobSearch():
    easy_counter = 0
    easy_results = pd.DataFrame(columns=["Title", "Location", "Company"])
    hard_counter = 0
    hard_results = pd.DataFrame(
        columns=["Title", "Location", "Company", "ApplyURL"])

    next_page_counter = 0

    easy_button_class = 'indeed-apply-button-label'
    hard_button_class = 'view-apply-button blue-button'

    for job in browser.find_element_by_class_name('jobsearch-SerpJobCard unifiedRow row result clickcard'):
        # check if the the button is easy apply:
        if job.find_element_by_class_name('indeed-apply-button-label') == easy_button_class:
            job.find_element_by_class_name(easy_button_class).click()
            easy_counter = easy_counter+1
            title = job.find_element_by_id('vjs-jobtitle').text()
            location = job.find_element_by_id('vjs-loc').text()
            company = job.find_element_by_id('vjs-cn').text()
            easy_results = easy_results.append(
                {'Title': title, 'Location': location, "Company": company}, ignore_index=True)
            # //TODO: loop through the job application pages and return to the orginal page
            submitApplication()

        # method to navigate the application process
        # check if the button is not easy apply:
        if job.find_element_by_class('view-apply-button blue-button') == hard_button_class:
            hard_counter = hard_counter+1
            title = job.find_element_by_id('vjs-jobtitle').text()
            location = job.find_element_by_id('vjs-loc').text()
            company = job.find_element_by_id('vjs-cn').text()
            applylink = job.find_element_by_id(
                'apply-button-container').find_element_by_tag_name('a').get_attribute('href').strip()
            hard_results = hard_results.append(
                {'Title': title, 'Location': location, "Company": company, "ApplyURL": applylink}, ignore_index=True)
    # click the next page
    next_page_counter = next_page_counter+1
    while next_page_counter < 5:
        clickNextPage()


def clickNextPage():
    browser.find_element_by_class_name('np').click()

# submit your application


def submitApplication():
    while True:
        trail_and_error()
        time.sleep(Loading_time)
        break
    # time.sleep(Loading_time)


def questionaire():
    text_feild_q = []
    drop_menu_q = []
    radio_btn_q = []
    text_feild_q = browser.find_elements_by_class_name('icl-TextInput-control')
    for texf in text_feild_q:
        time.sleep(Loading_time)
        texf.send_keys('3')
    drop_menu_q = browser.find_elements_by_class_name(
        'icl-Select-control is-error')
    for drp_mn in drop_menu_q:
        time.sleep(Loading_time)
        try:
            if drp_mn == 'Canada':
                drp_mn.select_by_value('Canada')
            drp_mn.select_by_index(1)
        except:
            continue
    radio_btn_q = browser.find_elements_by_id('radio-option-1')
    for rdbtn in radio_btn_q:
        rdbtn.select_by_index(1)


def trail_and_error():
    action_button = browser.find_element_by_xpath(
        '//*[@id="form-action-continue"]')
    continue_button = browser.find_element_by_xpath(
        '//*[@id="form-action-continue"]')
    submit_button = browser.find_element_by_xpath(
        '//*[@id="form-action-submit"]')
    button_two = browser.find_element_by_xpath(
        '//*[@id="ia-ApplyFormScreen"]/div/form/div[2]/div[2]/div/div[2]/button[1]')
    button_three = browser.find_element_by_xpath(
        '//*[@id="ia-container"]/div/div[2]/a')
    try:
        values = browser.find_elements(By.XPATH, '//*[id')
        for value in values:
            if value == '//*[@id="form-action-continue"]':
                action_button.click()
            elif value == '//*[@id="ia-ApplyFormScreen"]/div/form/div[2]/div[2]/div/div[2]/button[1]':
                button_two.click()
            elif value == '//*[@id="form-action-continue"]':
                continue_button.click()
            elif value == '//*[@id="form-action-submit"]':
                submit_button.click()
            elif value == '//*[@id="ia-container"]/div/div[2]/a':
                button_three.click()
            else:
                questionaire()
    except Exception:
        trail_and_error()


def run(username, password, search_id, search_loc):
    print('Welcome to the end of your pain')
    print('This code will replace your job search on indeed.')
    try:
        print('I am here to help you find a job')
        openbrowser()
        navigateToSite(username, password, search_id, search_loc)
        checkJobSearch()
        print('We are done')
    except:
        pass
        print('something went wrong Message Hussam Hammad for help')


        ############################# change the following strings to your data ###################
Login_username = 'hussamhammad@cap.canada.ca'  # change to yours
Login_password = 'place_holder'  # change to yours

Search_keyword = 'finance'  # job / field / keyword
Search_location = 'Canada'  # location / City or state or country

run(Login_username, Login_password, Search_keyword, Search_location)
