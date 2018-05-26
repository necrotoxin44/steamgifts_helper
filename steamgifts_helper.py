import pickle
from selenium import webdriver
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

#create instance of Firefox driver
driver = webdriver.Firefox()

# navigate to steamgifts
driver.get("https://www.steamgifts.com/")

#load cookies for login from pickled object
with open("cookies/baked_cookies.pkl", "rb") as baked_cookies:
    for cookie in pickle.load(baked_cookies):
        driver.add_cookie(cookie)

#navigate to wishlist
driver.get("https://www.steamgifts.com/giveaways/search?type=wishlist")

driver.quit()
