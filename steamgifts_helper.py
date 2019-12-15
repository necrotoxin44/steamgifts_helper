import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import boto3
import os
import argparse


MAX_PAGES = 10
root = 'https://www.steamgifts.com'
source_dict = {
    'all':
        'https://www.steamgifts.com/',
    'wishlist':
        'https://www.steamgifts.com/giveaways/search?type=wishlist',
    'recommended':
        'https://www.steamgifts.com/giveaways/search?type=recommended',
    'group':
        'https://www.steamgifts.com/giveaways/search?type=group',
    'new':
        'https://www.steamgifts.com/giveaways/search?type=new'
}
trail_of_cookies = 'baked_cookies.pkl'
cookie_jar = 'steamgift-helper-for-d'


class Giveaway:
    """docstring for ."""
    def __init__(self, href, end_time, cost):
        self.href = href
        self.end_time = end_time
        self.cost = cost


def load_last_cookies(driver, path, heroku=False):
    # Navigate driver to steamgifts.
    driver.get(root)

    if heroku:
        # TODO: Implement Heroku
        heroku['client'].download_file(
            heroku['b_name'],
            heroku['f_name'],
            heroku['f_name']
        )
        print('Download Successful')
    # Add cookies for login to the driver, from a pickled object.
    with open(path, 'rb') as baked_cookies:
        for cookie in pickle.load(baked_cookies):
            driver.add_cookie(cookie)

def initialize_driver():
    # create instance of (headless) Firefox driver
    options = Options()
    options.add_argument('-headless')
    return webdriver.Firefox(options=options)

def check_login_success(driver):
    # Reload the page.
    driver.get(root)
    # Assert login was loaded from cookies.
    try:
        element = driver.find_element(By.XPATH,
            "//a[@class='nav__avatar-outer-wrap']")
    except NoSuchElementException as e:
        print('Successful login not found.')
        raise
    else:
        print('Account loaded successfully:')
        print(element.get_attribute('href'))
        return True

def get_user_points(driver):
    driver.get(root)
    element = driver.find_element(By.CLASS_NAME, 'nav__points')
    points = int(element.text)
    return points

def crawl_giveaway_pages(driver, start):
    pages = 0
    next_page = start
    giveaways = []
    while(pages < MAX_PAGES):
        driver.get(next_page)
        pages += 1
        print(driver.title)
        giveaways.extend(gather_page_giveaways(driver))
        try:
            np_selector = "//span[text()='Next']/ancestor::a"
            next_page_el = driver.find_element(By.XPATH, np_selector)
            next_page = next_page_el.get_attribute('href')
        except:
            break
    return giveaways

def gather_page_giveaways(driver):
    r_selector = "//div[@class='pinned-giveaways__outer-wrap']/following-sibling::div[2]//a[@class='giveaway__heading__name']"
    p_selector = "//div[@class='pinned-giveaways__outer-wrap']/following-sibling::div[2]//span[@class='giveaway__heading__thin' and position()=last()]"
    t_selector = ""

    r_elements = driver.find_elements(By.XPATH, r_selector)
    refs = [element.get_attribute('href') for element in r_elements]

    p_elements = driver.find_elements(By.XPATH, p_selector)
    points = [int(element.text[1:-2]) for element in p_elements]

    # t_elements = driver.find_elements(By.XPATH, t_selector)

    new_giveaways = zip(refs, points)
    return new_giveaways

def enter_giveaways(driver, giveaways, points):
    entered = 0
    p = points
    for g in giveaways:
        if g[1] <= p:
            if enter_giveaway(driver, g[0]):
                p -= g[1]
                entered += 1
    return entered

def enter_giveaway(driver, g_path):
    driver.get(g_path)
    try:
        driver.find_element(By.CLASS_NAME, 'sidebar__entry-insert').click()
    except (ElementNotInteractableException, NoSuchElementException) as e:
        return False
    else:
        return True

def renew_cookies(driver, path, heroku=False):
    with open(path, 'wb') as cookies_to_bake:
        pickle.dump(driver.get_cookies(), cookies_to_bake)
    print('Cookies renewed.')
    if heroku:
        # TODO: Implement heroku
        heroku['client'].upload_file(
            heroku['f_name'],
            heroku['b_name'],
            heroku['f_name']
        )
        print('Upload Successful')


parser = argparse.ArgumentParser(description='Helper to enter SteamGifts giveaways.')
parser.add_argument('--heroku', dest='heroku', action='store_true')
args = parser.parse_args()

with initialize_driver() as d:
    print('Firefox driver initialized.')

    S3 = {}
    if args.heroku:
        S3 = {
            # 'client': S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET']),
            'client': boto3.client('s3',
                aws_access_key_id=os.environ['S3_KEY'],
                aws_secret_access_key=os.environ['S3_SECRET']
            ),
            'f_name': trail_of_cookies,
            'b_name': cookie_jar
        }

    print('Adding cookies...')
    load_last_cookies(d, trail_of_cookies, heroku=S3)
    print('Cookies added.')

    check_login_success(d)

    user_points = get_user_points(d)
    print(user_points)

    crawl_start = source_dict['wishlist']
    giveaways = crawl_giveaway_pages(d, crawl_start)
    # print(giveaways)

    print(enter_giveaways(d, giveaways, user_points))

    renew_cookies(d, trail_of_cookies, heroku=S3)
