# - *- coding: utf- 8 - *-
import re
import random
import logging
import requests
from datetime import datetime
from time import sleep

from utils.decorators import catcherError
from pprint import pprint

@catcherError
def log(e):
    print(e)
    logging.exception(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

@catcherError
def log_action(data):
    print(str(data) + '\n')
    logging.exception(f"""***************************************************
{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
{str(data)}
***************************************************""")

def randWord(count):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    number = 1
    length = count
    for pwd in range(number):
            word = ''
            for c in range(length):
                word += random.choice(chars)
    return word
