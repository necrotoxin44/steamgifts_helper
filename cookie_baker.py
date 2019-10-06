import argparse
import os
import pickle
from selenium import webdriver
import sys


def bake_cookies(pickle_path=''):
    with webdriver.Firefox() as driver:
        input('Press enter when done preparing cookies: ')
        pickle_path += 'baked_cookies.pkl'
        # TODO: could make sure browser hasn't been prematurely closed
        with open(pickle_path, 'wb') as cookie_file:
            pickle.dump(driver.get_cookies(), cookie_file)

if __name__ == '__main__':
    def dir_path(path):
        if os.path.isdir(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f'readable_dir:{path} is not a valid path')
    parser = argparse.ArgumentParser(description='Pickles session cookies for use by the SteamGifts little helper. Yum!')
    parser.add_argument(
        '--dir',
        dest='output_dir',
        help='Path to the output directory where we will store our precious pickled cookies.',
        type=dir_path
        )

    parsed_args = parser.parse_args(sys.argv[1:])
    if parsed_args.output_dir:
        bake_cookies(pickle_path=parsed_args.output_dir)
    else:
        bake_cookies()
