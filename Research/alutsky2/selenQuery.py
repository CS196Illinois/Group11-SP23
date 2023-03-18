import selenium as sm
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Firefox(executable_path="geckodriver")
driver.get("https://www.yellowpages.com/")

#set firefox options 
df = pd.DataFrame();
zipCodeList = list(range(0, 99999))

#only gets first page
def getURL(zipCode, tag):
    url = f"https://www.yellowpages.com/search?search_terms=" + tag + "&geo_location_terms=" + zipCode
    driver.get(url)
    driver.implicitly_wait(3)
    scrollable_pane = driver.find_element(By.CLASS_NAME, "scrollable-pane")
    listinfo = scrollable_pane.find_elements(By.CLASS_NAME, "v-card") 
    driver.implicitly_wait(0)
    for e in listinfo:
        try:
            nameElement = e.find_element(By.CLASS_NAME,"n").text[3::]
        except:
            nameElement = ""
        try:
            categoryElement = e.find_element(By.CLASS_NAME,"categories").text
        except:
            categoryElement = ""
        try:
            priceElement = e.find_element(By.CLASS_NAME,"price-range").text
        except:
            priceElement = ""
        print(nameElement + " " + categoryElement + " " + priceElement)
getURL("01001", "restaurant")

#driver.quit()
