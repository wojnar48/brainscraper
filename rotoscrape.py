import click
import sys
import datetime
import requests
import re
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from schemas import player_schema
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from rotoparser import RotoProjParser

# Player types
HITTER = 'hitter'
PITCHER = 'pitcher'
PLAYER_TYPES = [HITTER, PITCHER]

# Site types
DF = 'draftkings'
FD = 'fanduel'
SITE_TYPES = [DF, FD]

def clean_data(data):
    return bytes(data, 'utf-8').decode('unicode_escape')

def parse_data(data, pattern):
    matches = pattern.findall(data)
    if matches:
        return clean_data(matches[0])
    raise Exception(f'Got no matches for pattern: {pattern}')

def validate_player_type(ctx, param, value):
    if value not in PLAYER_TYPES:
        print(f'Unknown player type: {value}, select one of: {PLAYER_TYPES}')
        sys.exit(1)
    return value

def validate_site_type(ctx, param, value):
    if value not in SITE_TYPES:
        print(f'Unknown site type: {value}, select one of: {PLAYER_TYPES}')
        sys.exit(1)
    return value

@click.command()
@click.option('--playertype', default=f'{HITTER}', callback=validate_player_type, help=f'Select one of: {PLAYER_TYPES}')
@click.option('--site', default=f'{DF}', callback=validate_site_type, help=f'Select one of: {SITE_TYPES}')
@click.option('--numdays', default='1', help=f'Select number of days for data')
@click.argument('start_date', type=click.DateTime())
def get_stats(playertype, site, start_date, numdays):
    """
    Get projected MLB stats from RotoGrinders.com
    """

    for _ in range(int(numdays)):
        url = f"https://rotogrinders.com/projected-stats/mlb-{playertype}?site={site}&date={start_date.strftime('%Y-%m-%d')}"
        click.echo(click.style(f'Fetching data from url={url}', fg='green'))

        # create a new Firefox session
        options = Options()
        options.set_headless()
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(10) # wait for html to generate

        try:
            driver.get(url)
        except Exception as err:
            click.echo(err)
            sys.exit(1)

        soup = BeautifulSoup(clean_data(driver.page_source), 'html.parser')
        stats_table = soup.find('div', id='proj-stats')

        columns = []

        cols = stats_table.find_all('div', attrs={'class': 'rgt-col'})
        for col in cols:
            # find all children divs of rgt-col div
            columns.append([clean_data(item.text) for item in col.find_all('div')])

        features = RotoProjParser(columns, playertype, start_date.strftime('%Y-%m-%d'))
        features.to_csv()

        # increment date by 1 day
        start_date += datetime.timedelta(days=1)
        driver.quit() 
