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

        try:
            element = browser.find_element_by_xpath(
                '//*[@id="form-action-continue"]')  # placeholder
            element.click()
            button_two = browser.find_element_by_xpath(
                '//*[@id="ia-ApplyFormScreen"]/div/form/div[2]/div[2]/div/div[2]/button[1]')
            continue_button = browser.find_element_by_xpath(
                '//*[@id="form-action-continue"]')
            submit_button = browser.find_element_by_xpath(
                '//*[@id="form-action-submit"]')
            button_four = browser.find_element_by_xpath(
                '//*[@id="ia-container"]/div/div[2]/a')
        except:
            break
    time.sleep(Loading_time)

    def questionaire():
        # will start a while true function with if statements to funnel down to the least likely option
        # Text fields -> radio buttons ->dropdowns
        text_feild_q = browser.find_elements_by_class_name(
            'icl-TextInput-control')  # I am hoping this will catch every textinput field
        # icl-TextInput-control icl-TextInput-control--sm is-error

        drop_menu_q = browser.find_elements_by_class_name(
            'icl-Select-control is-error')
        text_feild_q_a = browser.find_elements_by_class_name(
            'icl-TextInput-control icl-TextInput-control--sm')
        radio_btn_q = browser.find_element_by_id('radio-option-1')


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
