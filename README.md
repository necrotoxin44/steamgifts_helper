# steamgifts_helper
A SteamGifts giveaway entry bot using Selenium.

## Setup

1. To set up locally, first clone the repo: `$ git clone https://github.com/necrotoxin44/steamgifts_helper.git`
2. Make sure [Mozilla geckodriver](https://github.com/mozilla/geckodriver/) is in the root directory, or is in your system's PATH. [Other](https://www.seleniumhq.org/download/) browser drivers are available, but it will need to be slightly reconfigured. 
3. Download the Python bindings for Selenium with `pip install selenium`

## Usage

1. For first time usage, run `cookiebaker.py`. Once the browser opens, log-in to SteamGifts, and the press enter in the command prompt. This saves the log-in cookies as a pickled Python object. The helper script renews the cookies, though this may still need to be done manually if the cookies time-out.
2. Now you can run `steamgifts_helper.py`! By default, it will only look at entries under "wishlist".
