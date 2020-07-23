# Scraping Urban dictionary

# -*- coding: utf-8 -*-
import pprint
import re
import requests
from bs4 import BeautifulSoup
#import json

def alexa_format(input_text):

    return re.sub(r'[^\w,]', ' ',input_text).lower()

def word_of_the_day():

    url = 'https://www.urbandictionary.com/'
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



def main():
    word_of_the_day()


if __name__ == '__main__':
    main()