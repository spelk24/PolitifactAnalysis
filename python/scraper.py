### Politifact Scraper ###
# imports
import pandas as pd
import numpy as np
import re
import time
import datetime
import os
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

os.chdir("/Users/spelkofer/Desktop/Documents/chromedriver")

# individual person scraper
def individual_history(person):
    url = "https://www.politifact.com/personalities/" + person
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    # Scroll Down to load elements
    element = driver.find_element_by_class_name("o-platform__header")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    # Wait 5 seconds to load
    time.sleep(5)
    # Pull out data
    category_class = driver.find_elements_by_class_name("m-scorecard__title")
    category_list = [i.text for i in category_class]
    percent_class = driver.find_elements_by_class_name("m-scorecard__value")
    percent_list = [i.text for i in percent_class]
    total_class = driver.find_elements_by_class_name("m-scorecard__checks")
    total_list = [i.text for i in total_class]
    df = pd.DataFrame(
        {
            "Person": [person] * len(total_list),
            "Category": category_list,
            "Percent": percent_list,
            "Total": total_list,
        }
    )
    driver.close()
    return df


# Create dataset
people = [
    "donald-trump",
    "barack-obama",
    "joe-biden",
    "elizabeth-warren",
    "nancy-pelosi",
    "bernie-sanders",
]
politifact_df = pd.DataFrame(columns=["Person", "Category", "Percent", "Total"])
for person in people:
    politifact_df = politifact_df.append(
        individual_history(person), ignore_index=False, sort=False
    )
politifact_df
