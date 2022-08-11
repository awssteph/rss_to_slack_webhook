from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
import requests
import json
import logging


# Adapted from: https://timothybramlett.com/recieving_notifications_of_rss_feeds_matching_keywords_with_Python.html

# Just some sample keywords to search for in the title
key_words = ['cost','price','optimize','optimization','costs','prices','pricing','advisor', 'graviton','CFM','financial','finops','finance']

# Slack Webhook for Publishing Target
webhook = 'https://hooks.slack.com/workflows/T016M3G908HSKLSL/9734HHKS/FFESfRF0'

# RSS Feed
rss = 'https://aws.amazon.com/about-aws/whats-new/recent/feed/'


# View list of previously shared URLs
f = open('viewed_urls.txt', 'r')
urls = f.readlines()
urls = [url.rstrip() for url in urls] # remove the '\n' char
f.close()

#logging
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
file1 = open('logfile.log', 'a')
file1.write(date + " Logging script execution")
file1.write("\n")
file1.close()


def contains_wanted(in_str):
    # returns true if the in_str contains a keyword
    # we are interested in. Case-insensitive
    for wrd in key_words:
        if wrd.lower() in in_str:
            return True
    return False

def url_is_new(urlstr):
    # returns true if the url string does not exist
    # in the list of strings extracted from the text file
    if urlstr in urls:
        return False
    else:
        return True

feed = feedparser.parse(rss)
for key in feed["entries"]:
    url = key['links'][0]['href']
    title = key['title']
    rawDescription = key['description']
    description = BeautifulSoup(rawDescription, 'html.parser')

    if contains_wanted(title.lower()) and url_is_new(url):
        print('{} - {} - {}'.format(title, url, description.get_text()))

        #msgtitle = title
        #msg = '{}\n{}'.format(title, url, description)

        body = {
            "title": title,
            "description": description.get_text(),
            "url": url,
        }


        jsonData = json.dumps(body)
        response = requests.post(webhook, jsonData)
        responseBody = response.json()

        #logging
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        file1 = open('logfile.log', 'a')
        file1.write(date + " Attempting post to webhook: "  + jsonData)
        file1.write("\n")
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        file1.write(date + " Response: " + str(response) + " : ")
        file1.write(json.dumps(responseBody))
        file1.write("\n")
        file1.close()

                # recording URLs to file
        with open('viewed_urls.txt', 'a') as f:
            f.write('{}\n'.format(url))
            f.close()
