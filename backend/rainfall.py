from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from functools import reduce
import time
from datetime import datetime
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def render_page(url):
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.get(url)
    time.sleep(10)
    r = driver.page_source
    driver.quit()
    return r


def scraper(url):
    r = render_page(url)
    soup = BS(r, "html.parser")
    container = soup.find('lib-city-hourly-forecast')
    check = container.find('tbody')
    data = []
    for c in check.find_all('tr', class_='ng-star-inserted'):
        for j in c.find_all('span', class_='wu-unit-rain'):
            i = j.find('span', 'wu-value-to')
            trial = i.text
            trial = trial.strip('  ')
            data.append(float(trial))
    return data

# date format dd-mm-yyyy
def get_rainfall(city, date):
    base_url = 'https://www.wunderground.com/hourly/in'
    date = date.split("-")
    curr_year = date[1]
    curr_month = date[1]
    curr_day = date[2]
    output = []
    date = str(curr_year) + '-' + str(curr_month) + '-' + str(curr_day)
    url = base_url + '/' + city + '/date/' + date
    out = scraper(url)
    return sum(out)
