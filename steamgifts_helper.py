import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

#create instance of (headless) Firefox driver
options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)
print("Headless Firefox initialized.")

root = "https://www.steamgifts.com"

# navigate to steamgifts
driver.get(root)

#load cookies for login from pickled object
with open("cookies/baked_cookies.pkl", "rb") as baked_cookies:
    for cookie in pickle.load(baked_cookies):
        driver.add_cookie(cookie)

#navigate to wishlist
driver.get("https://www.steamgifts.com/giveaways/search?type=wishlist")
try:
    #select titles for each giveaway for use of their hyperlink
    elements = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div/div[2]/div[3]//div[@class='giveaway__row-inner-wrap']//a[@class='giveaway__heading__name']")

    #extract hyperlinks
    href_list = []
    for element in elements:
        href_list.append(element.get_attribute("href"))
    for href in href_list:
        driver.get(href)
        try:
            driver.find_element(By.CLASS_NAME, "sidebar__entry-insert").click()
        except ElementNotInteractableException as e:
            pass

finally:
    driver.quit()
