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
    dfZipCode = pd.DataFrame()
    try: 
        url = f"https://www.yellowpages.com/search?search_terms=" + tag + "&geo_location_terms=" + zipCode
        driver.get(url)
        driver.implicitly_wait(1)
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
            dfElement = pd.DataFrame()
            dfElement['Name'] = [nameElement]
            dfElement['Category'] = [categoryElement]
            dfElement['priceElement'] = [priceElement]
            dfElement['ZipCode'] = [zipCode]
            dfZipCode = pd.concat([dfElement, dfZipCode], ignore_index=True)
        return dfZipCode
    except:
        return dfZipCode


for i in [str(num).zfill(5) for num in range(10001,10031)]:
    zipToAdd = getURL(i, "restaurant")
    df = pd.concat([zipToAdd, df], ignore_index=True)
driver.quit()

print(df)
