#!/usr/bin/env python3
import os
import sys
import re
import argparse
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
init()


parser = argparse.ArgumentParser()
parser.add_argument('dirname', nargs='?', help='Enter the name of the directory to write the file to', default='.')
args = parser.parse_args()
user_dir = args.dirname
cwd = os.getcwd() + '/'
path = os.path.join(cwd, user_dir)
try:
    if not os.access(user_dir, os.F_OK):
        os.mkdir(path)
except Exception as e:
    print('An error occurred while processing the file: ', e)
    


def browser():
    url = ''
    stack = deque()
    history = {}
    while True:
        url = input('Enter a website url: ')
        if url.lower() == 'exit' or url.lower() == 'quit':
            print('Goodbye!')
            exit()
        if url == 'back' and stack:
            if len(stack) == 1:
                print(stack.pop())
            else:
                stack.pop()
                print(stack.pop())
        elif url == 'back':
            return
        else:
            validation = re.match(r"[\S]+", url)
            # validation = url[-3:] in ['com', 'org', 'net', 'gov', 'edu']
            if not validation and history.get(url) is None:
                print('Incorrect URL')
                exit()
            elif history.get(url) is not None:
                text = history.get(url)
                print(text)
                stack.append(text)
            elif not url.startswith('https://'):
                url = 'https://' + url
            if url.startswith('https://'):
                name = user_dir + '/' + url[8:].split('.')[0]
                try:
                    request = requests.get(url)
                except requests.exceptions.ConnectionError:
                    print('Invalid URL')
                    exit()
                if request.status_code > 299:
                    return f'The URL returned error code {request.status_code}.'
                soup = BeautifulSoup(request.content, 'html.parser')
                for i in soup.find_all('a'):
                    i.string = ''.join([Fore.BLUE, i.get_text(), Fore.RESET])
                print(soup.text)
                stack.append(soup.text)
                history[url[8:].split('.')[0]] = soup.text
                with open(name, 'w', encoding='UTF-8') as file:
                    file.write(soup.text)
                if url == name:
                    print(open(name).read())


if __name__ == '__main__': browser()
