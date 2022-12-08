import re
import time
import requests
import csv
import pandas as pd
import ast
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import random
from datetime import datetime
from bs4 import BeautifulSoup
from shutil import which
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openpyxl import load_workbook
import openpyxl
import xlsxwriter

firefoxOptions = Options()
FIREFOXPATH = which("firefox")
# firefoxOptions.add_argument('--headless')
firefoxOptions.add_argument('--no-sandbox')
firefoxOptions.add_argument("--window-size=1920,1080")
firefoxOptions.add_argument('--disable-dev-shm-usage')
firefoxOptions.add_argument('--ignore-certificate-errors')
firefoxOptions.add_argument('--allow-running-insecure-content')
firefoxOptions.binary = FIREFOXPATH
PATH_FIREFOX = '/Users/miroslav/Desktop/geckodriver'

URLs_ = "https://eva.domclick.ru/login"
browser = webdriver.Firefox(executable_path=PATH_FIREFOX, options=firefoxOptions)
browser.get(URLs_)
time.sleep(5)
tel = browser.find_element(By.XPATH, "//input[@type='tel']")
# tel.click()
# time.sleep(2)
# browser.execute_script("arguments[0].click();", tel)
tel.send_keys('7 904 361-58-71')
psw = browser.find_element(By.XPATH, "//input[@type='password']").send_keys('956dd2876')

time.sleep(2)
submit = browser.find_element(By.XPATH, "//button[@type='submit']")
browser.execute_script("arguments[0].click();", submit)

time.sleep(10)

browser.quit()

