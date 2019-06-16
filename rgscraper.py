import click
import sys
import datetime
import requests
import re
import pandas as pd
import numpy as np

from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from configs.rgconfigers import RGConfiger
from parsers.rgparsers import RGStatsParser
from parsers.rgparsers import RGPlayerUrlParser
from transformers.rgtransformers import RGTransformer

def validate_player_type(ctx, param, value):
    if value not in RGConfiger.PLAYER_TYPES:
        print(f'Unknown player type: {value}, select one of: {RGConfiger.PLAYER_TYPES}')
        sys.exit(1)
    return value

def validate_site_type(ctx, param, value):
    if value not in RGConfiger.SITE_TYPES:
        print(f'Unknown site type: {value}, select one of: {RGConfiger.PLAYER_TYPES}')
        sys.exit(1)
    return value

@click.command()
@click.option('--playertype', default='hitter', callback=validate_player_type, help=f'Select "hitter" or "pitcher"')
@click.option('--site', default='draftkings', callback=validate_site_type)
@click.option('--numdays', default='1', help=f'Select number of days for data')
@click.argument('start_date', type=click.DateTime())
def get_proj_stats(playertype, site, start_date, numdays):
    """
    Get projected MLB stats from RotoGrinders.com
    """

    configer = RGConfiger(playertype, site)

    for _ in range(int(numdays)):

        url = configer.get_url(start_date)
        click.echo(click.style(f'Fetching data from url={url}', fg='green'))

        # create a new Firefox session
        # TODO: Move driver config into configer
        options = Options()
        options.set_headless()
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(10) # wait for html to generate

        try:
            driver.get(url)
        except Exception as err:
            click.echo(f'Failed to get {url}, error: {err}')
            sys.exit(1)

        # TODO Move parse and transformer into wrapper class
        try:
            stats_parser = RGStatsParser(driver.page_source)
            url_parser = RGPlayerUrlParser(driver.page_source)
        except Exception as err:
            click.echo(f'Failed to parse page, error: {err}')
            sys.exit(1)

        try:
            stats_df = RGTransformer(configer, stats_parser.get_columns())
            stats_df.to_csv(start_date, playertype)
        except Exception as err:
            click.echo(f'Failed to transform stats, error: {err}')
            sys.exit(1)

        try:
            url_df = pd.DataFrame(data=url_parser.urls(), columns=['player_id', 'url'])
        except Exception as err:
            click.echo(f'Failed to transform stats, error: {err}')
            sys.exit(1)

        # TODO: Hande this in a stats and urls wrapper class
        urls_path = 'output/{}_{}_urls.csv'.format(start_date.strftime('%Y-%m-%d'), playertype)
        url_df.to_csv(path_or_buf=urls_path, index=False, na_rep='NA')

        start_date += datetime.timedelta(days=1)
        driver.quit() 
    # merge_proj_actual()

# def merge_proj_actual():
    # urls = pd.DataFrame.from_csv('')
    # base_url = f'https://rotogrinders.com/players/{}?&format=json'
    # click.echo('CALLBACK!')
