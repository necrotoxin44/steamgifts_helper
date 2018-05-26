import pickle
from selenium import webdriver

#create instance of firefox driver
driver = webdriver.Firefox()

#do logins and create cookies

input("Press enter when done preparing cookies: ")

#pickle the cookies
with open("baked_cookies.pkl", "wb") as cookie_file:
    pickle.dump(driver.get_cookies(), cookie_file)

driver.quit()
