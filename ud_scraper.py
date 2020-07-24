# Scraping Urban dictionary

# -*- coding: utf-8 -*-
import random
import pprint
import re
import requests
from bs4 import BeautifulSoup
#import json

def scrape_word_ud(url):
    '''
    Scrape Urban Dictionary web page and return word with meaning and example
    '''   
    content = BeautifulSoup(requests.get(url).text, 'html5lib')

    word_day_result = {}
    word_day_result['word'] = alexa_format(content.find(class_='word').text)
    word_day_result['meaning'] = alexa_format(content.find(class_='meaning').text)
    
    word_day_examples = content.find(class_='example')
    split_examples = ''
    for e in word_day_examples.descendants:
        if isinstance(e, str):
            split_examples += e
        elif e.name == 'br':
            split_examples += '\n'
    word_day_result['example'] = alexa_format(split_examples.splitlines()[0])
    
    pprint.pprint(word_day_result)
    return word_day_result

def alexa_format(input_text):
    '''
    Format text that Alexa can handle
    '''
    return re.sub(r'[^\w,]', ' ',input_text).lower()

def word_of_the_day():
    '''
    Get a word of tje day
    '''
    url = 'https://www.urbandictionary.com/'

    return scrape_word_ud(url)


def random_word():
    '''
    Get random word
    '''
    url = 'https://www.urbandictionary.com/random.php?page=' + str(random.randint(11,999))
    
    return scrape_word_ud(url)


a = word_of_the_day()

b = a['example'] + a['word']

print(b)


# def main():
#     word_of_the_day()


# if __name__ == '__main__':
#     main()
