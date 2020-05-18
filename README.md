# steamgifts_helper
A SteamGifts giveaway entry bot using Selenium.

Currently, you can run this locally, or alternatively run it as a Heroku app with Amazon S3 for a minimal amount of storage.

## Setup

1. To set up locally, first clone the repo: `$ git clone https://github.com/necrotoxin44/steamgifts_helper.git`
2. Make sure [Mozilla geckodriver](https://github.com/mozilla/geckodriver/) is in the root directory, or is in your system's PATH. [Other](https://www.seleniumhq.org/download/) browser drivers are available, but it will need to be slightly reconfigured.
3. Download the Python bindings for Selenium with `pip install selenium`

## Heroku Setup

- As Heroku slugs are built and destroyed as need be with no built-in persistent storage, in order for us to use Selenium, we'll need to find a way to include the Firefox binary and the geckodriver, which we'll do through a Heroku builtpack, which will dictate how the slug is built.
- `$ heroku buildpacks:add https://github.com/ronnielivingsince1994/heroku-integrated-firefox-geckodriver`
- The Heroku app will use this new build pack on the next release, so you can use `$ git push heroku master` to create a new release with the additional buildpack
- Set the environmental variables below, either through the Heroku Dashboard web interface, or the Heroku CLI using `heroku config:set KEY=value`
```
FIREFOX_BIN:      /app/vendor/firefox/firefox

GECKODRIVER_PATH: /app/vendor/geckodriver/geckodriver

LD_LIBRARY_PATH:  /usr/local/lib:/usr/lib:/lib:/app/vendor

PATH:             /usr/local/bin:/usr/bin:/bin:/app/vendor/
```


## Usage

1. For first time usage, run `cookiebaker.py`. Once the browser opens, log-in to SteamGifts, and the press enter in the command prompt. This saves the log-in cookies as a pickled Python object. The helper script renews the cookies, though this may still need to be done manually if the cookies time-out.
2. Now you can run `steamgifts_helper.py`! By default, it will only look at entries under "wishlist".
