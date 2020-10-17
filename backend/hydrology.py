from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import re
import glob
import shutil
import zipfile
import subprocess
import requests
from pcraster import *
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
from tifffile import imread, imwrite
from skimage.transform import resize
import rasterio
from rasterio.enums import Resampling
from os.path import expanduser

home = expanduser("~")
cwd = os.getcwd()

try:
    shutil.rmtree('dataset')
except:
    pass
try:
    os.makedirs('dataset')
except:
    pass
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option("prefs", {
  "download.default_directory": cwd+"/dataset",
  "download.prompt_for_download": False,
})
driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", options=options)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': cwd+"/dataset"}}
command_result = driver.execute("send_command", params)
driver.get('https://bhuvan-app3.nrsc.gov.in/data/download/index.php')

DOWNLOAD_PATH = home + '/Downloads'
lat_min, lat_max, lng_min, lng_max = -1, -1, -1, -1


with open('credentials.txt', 'r') as myfile:
    cred = myfile.read().split('\n')
    username = cred[0]
    password = cred[1]


def login(username, password):
    login_button = driver.find_element_by_link_text('Login')
    login_button.click()
    sleep(5)
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])
    username_box = driver.find_element_by_id('username')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('password')
    password_box.send_keys(password)
    submit_button = driver.find_element_by_name('submit')
    submit_button.click()
    sleep(5)
    driver.switch_to_default_content()
    sleep(2)
login(username, password)


def download(lat_min, lng_min, lat_max, lng_max):
    assert lat_min >= 6 and lat_min <= 40, "latitude should be between 6 and 40 degree"
    assert lat_max >= 6 and lat_max <= 40, "latitude should be between 6 and 40 degree"
    assert lng_min >= 66 and lng_min <= 102, "longiitude should be between 66 and 102 degree"
    assert lng_max >= 66 and lng_max <= 102, "longiitude should be between 66 and 102 degree"
    driver.switch_to_default_content()
    driver.switch_to.frame(driver.find_element_by_id("startPageFrame"))
    category = driver.find_element_by_id('Prj')
    category.click()
    project = Select(driver.find_element_by_id('subcategory'))
    project.select_by_value('C3')
    product = Select(driver.find_element_by_id('prdcts'))
    product.select_by_value('cdv3r1|MAP')
    min_lon = driver.find_element_by_id('bottom')
    min_lat = driver.find_element_by_id('left')
    max_lon = driver.find_element_by_id('right')
    max_lat = driver.find_element_by_id('top')
    min_lon.send_keys(str(lng_min))
    max_lon.send_keys(str(lng_max))
    min_lat.send_keys(str(lat_min))
    max_lat.send_keys(str(lat_max))
    sleep(2)
    select_button = driver.find_element_by_name('select_button')
    select_button.click()
    sleep(2)
    next_button = driver.find_element_by_xpath("//img[@alt='Next']")
    next_button.click()
    sleep(2)
    download_button = driver.find_element_by_xpath(
        "//img[@title='Click to download tile']")
    download_button.click()
    sleep(20)


def process_file():
    file_name = os.listdir('./dataset')[0]
    with zipfile.ZipFile('./dataset/' + file_name, 'r') as zip_ref:
        zip_ref.extractall('./dataset')
    file_path = glob.glob('./dataset/*/*.tif')[0]


def get_bounding_box(city):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
        city + ",India&key=AIzaSyDUjKlnObDJwUO6f2ueMvzc3UyF_Jepd5U"
    resp = requests.get(url=url)
    data = resp.json()
    global lat_min, lat_max, lng_max, lng_min
    north_east = data['results'][0]['geometry']['bounds']['northeast']
    south_west = data['results'][0]['geometry']['bounds']['southwest']
    lat_min = south_west['lat'] - 1
    lat_max = north_east['lat'] + 1
    lng_min = south_west['lng'] - 1
    lng_max = north_east['lng'] + 1
    return 1
    # except:
    # return 0


def hydrology_mapping(rainfall, infiltration=None, soil=None):
    # try:
    with rasterio.Env():
        dem = glob.glob('./dataset/*/*.tif')[0]
        with rasterio.open(dem) as dataset:
            data = dataset.read(1, out_shape=(100, 100),
                                resampling=Resampling.bilinear)
            transform = dataset.transform * dataset.transform.scale(
                (dataset.height / data.shape[0]),
                (dataset.width / data.shape[1])
            )
            profile = dataset.profile
            profile.update(transform=transform, width=data.shape[
                           1], height=data.shape[0])
            with rasterio.open('scaled.tif', 'w', **profile) as dataset:
                dataset.write(data, 1)
    x = gdal.Open("scaled.tif")
    gdal_band = x.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    x = x.ReadAsArray().astype(np.float)
    if np.any(x == nodataval):
        x[x == nodataval] = 1e31
    setclone(x.shape[0], x.shape[1], 0.1, -lng_min, lat_min)
    x = numpy2pcr(Scalar, x, -1)
    ldd = lddcreate(x, 1e31, 1e31, 1e31, 1e31)
    infilcap = scalar(0)
    if soil is not None:
        if infiltration is not None:
            infilcap = lookupscalar(infiltration, soil)
        else:
            infilcap = scalar(soil)
    randomField = scalar(rainfall)
    runoff = accuthresholdflux(ldd, randomField, infilcap)
    x = pcr2numpy(runoff, -1)
    return x
    # except:
    # return []


def map_hydrology(city, date):
    # update later with rainfall api call
    # rainfall = get_rainfall(date)
    rainfall = 0.5
    get_bounding_box(city)
    download(lat_min, lng_min, lat_max, lng_max)
    process_file()
    return hydrology_mapping(rainfall)
