from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome("./chromedriver")

##################### To Maximize the brower window ###################
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
##########################################33333########################



df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Sponsored", "Description"])

for i in range(0, 200, 10):
    driver.get('https://ca.indeed.com/jobs?q=KPMG&l=canada&start=' + str(i))
    jobs = []
    driver.implicitly_wait(4)

    for job in driver.find_elements_by_class_name('result'):

        soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')

        try:
            title = soup.find("a", class_="jobtitle").text.replace("\n", "").strip()

        except:
            title = 'None'

        try:
            location = soup.find(class_="location").text
        except:
            location = 'None'

        try:
            company = soup.find(class_="company").text.replace("\n", "").strip()
        except:
            company = 'None'

        try:
            salary = soup.find(class_="salary").text.replace("\n", "").strip()
        except:
            salary = 'None'

        try:
            sponsored = soup.find(class_="sponsoredGray").text
            sponsored = "Sponsored"
        except:
            sponsored = "Organic"

        sum_div = job.find_element_by_xpath('./div[3]')
        try:
            sum_div.click()
        except:
            close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
            close_button.click()
            sum_div.click()

        job_desc = driver.find_element_by_id('vjs-desc').text

        df = df.append({'Title': title, 'Location': location, "Company": company, "Salary": salary,
                        "Sponsored": sponsored, "Description": job_desc}, ignore_index=True)

        print("Got these many results:", df.shape)
        time.sleep(0.5)

df.to_csv("KPMG-Canada.csv", index=False)
print('Done, check your file')
