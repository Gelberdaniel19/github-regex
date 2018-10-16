import threading
import requests
from bs4 import BeautifulSoup
import sys
import os
import re

terminalwidth = 50

# Try to get arguments
try:
    url = sys.argv[1]
    search = re.compile(sys.argv[2])
except:
    print('usage: ./githubregex.py link regex')
    exit(0)

# Function for recursively finding all pages
pages = []
def getPages(page):
    global pages
    print(" | Searching in {}".format(page))
    
    # Soup it!
    pageText = requests.get(page).text
    soup = BeautifulSoup(pageText, 'lxml')
    links = soup.findAll('tr', {'class': 'js-navigation-item'})

    for link in links:
        try:
            if link.td.svg['class'] == ['octicon', 'octicon-file-directory']:
                newlink = 'https://github.com' + link.findAll('td', {'class': 'content'})[0].span.a['href']
                getPages(newlink)
            else:
                pages.append('https://github.com' + link.findAll('td', {'class': 'content'})[0].span.a['href'])
                print(" | Found {}".format(pages[-1]))
        except:
            pass

# Function to search a page for the text
def searchPage(page):
    pagetext = requests.get(page).text
    if search.search(pagetext) != None:
        print(" | {}".format(page))

        
# Fill the list of pages
print(' |', end='')
for i in range(terminalwidth):
    print('-', end='')
print('\n | SEARCHING FOR PAGES...')
getPages(url)


# Search every page for the string
print(' |', end='')
for i in range(terminalwidth):
    print('-', end='')
print('\n | SCANNING PAGES FOR TEXT...')
for page in pages:
    t = threading.Thread(target=searchPage, args=[page])
    t.start()
