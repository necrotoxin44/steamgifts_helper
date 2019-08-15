import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


root = 'https://www.steamgifts.com'
source_dict = [
    'all': 'https://www.steamgifts.com/',
    'wishlist': 'https://www.steamgifts.com/giveaways/search?type=wishlist',
    'recommended': 'https://www.steamgifts.com/giveaways/search?type=recommended',
    'group': 'https://www.steamgifts.com/giveaways/search?type=group',
    'new': 'https://www.steamgifts.com/giveaways/search?type=new'
]
trail_of_cookies = 'cookies/baked_cookies.pkl'


class Giveaway:
    """docstring for ."""
    def __init__(self, href, end_time, cost):
        self.href = href
        self.end_time = end_time
        self.cost = cost


def load_last_cookies(driver, path):
    # Navigate driver to steamgifts.
    driver.get(root)

    # Add cookies for login to the driver, from a pickled object.
    with open(path, 'rb') as baked_cookies:
        for cookie in pickle.load(baked_cookies):
            driver.add_cookie(cookie)

def initialize_driver():
    # create instance of (headless) Firefox driver
    options = Options()
    options.add_argument('-headless')
    return webdriver.Firefox(firefox_options=options)

def check_login_success(driver):
    # Reload the page.
    driver.get(root)
    # Assert login was loaded from cookies.
    try:
        driver.find_element(By.XPATH, "//a[@class='nav__avatar-outer-wrap']")
    except NoSuchElementException as e:
        return False
    else:
        return True

def renew_cookies(driver, path):
    with open(path, 'wb') as cookies_to_bake:
        pickle.dump(driver.get_cookies(), cookies_to_bake)


try:
    d = initialize_driver()
    print('Firefox driver initialized.')

    print('Adding cookies...')
    load_last_cookies(d, trail_of_cookies)
    print('Cookies added.')

    if check_login_success(d):
        print("Account loaded successfully.")
    else:
        print("Successful login not found.")
        break

    giveaways = []
    while pages:
        curr_page = pages.pop()
        if curr_page in visited:
            continue
        else:
            visited.append(curr_page)
        d.get(curr_page)
        # select titles for each giveaway for use of their hyperlink
        giveaway_path = ("/html/body/div[3]/div/div/div[2]/div[3]//div[@class='giveaway__row-inner-wrap']"
                         "//a[@class='giveaway__heading__name']")
        elements = d.find_elements(By.XPATH, giveaway_path)

        total_entered = 0
        # extract hyperlinks
        for element in elements:
            href_list.append(element.get_attribute('href'))

        next_page = ''
        try:
            next_page = d.find_element(By.XPATH, "//div[@class='pagination__navigation']/a[3]")
        except NoSuchElementException as e:
            pass
        else:
            pages.insert(0, next_page.get_attribute('href'))

    # # try to enter each giveaway
    # for href in href_list:
    #     d.get(href)
    #     try:
    #         d.find_element(By.CLASS_NAME, "sidebar__entry-insert").click()
    #     except (ElementNotInteractableException, NoSuchElementException) as e:
    #         break
    #     else:
    #         total_entered += 1
    #
    # print(str(total_entered) + " entered.")

    renew_cookies(d, trail_of_cookies)

except Exception as e:
    print(e)
    raise e
finally:
    d.quit()
