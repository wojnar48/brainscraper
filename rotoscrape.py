import click
import datetime
import requests
import re
import sys

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from schemas import player_schema
from rotoparser import RotoPlayerParser
# pip install ipython requests ipdb click enum

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
@click.argument('start_date')
def get_rotowire_data(playertype, site, start_date, numdays):
    """
    Get projected stats data from rotogrinders.com
    """

    year, month, day = map(int, start_date.split('-'))
    current = datetime.date(year, month, day)
    for _ in range(int(numdays)):
        yr, m, d = current.year, current.month, current.day
        current_str = f'{yr:04}-{m:02}-{d:02}'
        url = f'https://rotogrinders.com/projected-stats/mlb-{playertype}?site={site}&date={current_str}'
        click.echo(f'Fetching data from url={url}')
        current = current + datetime.timedelta(days=1)

        data_pattern = re.compile(r'data = (\[.*\]);', re.DOTALL)
        # schedules_pattern = re.compile(r'schedules: (.*?),\n\s*', re.MULTILINE | re.DOTALL)

        try:
            resp = requests.get(url)
            # resp.encoding = 'utf-8'
            player_data = parse_data(str(resp.content), data_pattern)
            player_parser = RotoPlayerParser(playertype, current_str, player_data, player_schema)
            player_parser.to_csv()
        except HTTPError as http_error:
            click.echo(f'HTTP error: {http_error}')
            sys.exit(1)
        except Exception as err:
            click.echo(err)
      
        