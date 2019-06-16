import csv
import json
import re

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

from transformers.rgtransformers import RGTransformer

### Utils ###
def clean_data(data):
    return bytes(data, 'utf-8').decode('unicode_escape')

def parse_url(url):
    player_id = url.split('-')[-1]
    player_url = f'https://rotogrinders.com{url}?&format=json'
    return player_id, player_url

class RGStatsParser(object):

    def __init__(self, page_html):
        self.soup_html = BeautifulSoup(clean_data(page_html), 'html.parser')
        self.columns = []

        # Parse projected stats and data URLs
        self.parse_proj_stats()
    
    def parse_proj_stats(self):
        stats_table = self.soup_html.find('div', id='proj-stats')
        columns = stats_table.find_all('div', attrs={'class': 'rgt-col'})
        for col in columns:
            # Find all rows in the column (row 0 will be the column name)
            self.columns.append([div.text for div in col.find_all('div')])
    
    def get_columns(self):
        return self.columns


class RGPlayerUrlParser(object):

    def __init__(self, page_html):
        self.soup_html = BeautifulSoup(clean_data(page_html), 'html.parser')
        self.data_urls = []

        # Parse player data URLs
        self.parse_data_urls()

    def parse_data_urls(self):
        stats_table = self.soup_html.find('div', id='proj-stats')
        anchors = stats_table.find_all('a', attrs={'data-url': True})
        for anchor in anchors:
            # Each parsed url will be a tuple (player_id, player_url)
            self.data_urls.append(parse_url(anchor.attrs['data-url']))

    def urls(self):
        return self.data_urls

