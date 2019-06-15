import csv
import json
import re
import pandas as pd
import numpy as np

COLS_CONFIG = {
  'Name': {
    'name': 'name'
  },
  'Salary': {
    'name': 'salary'
  },
  'Hand': {
    'name': 'hand'
  },
  'Team': {
    'name': 'team'
  },
  'Position': {
    'name': 'pos'
  },
  'Opp': {
    'name': 'opp',
    'cb': lambda s: re.sub(r'[^a-zA-Z ]', '', s)
  },
  'Order': {
    'name': 'order',
  },
  'Pitcher': {
    'name': 'pitcher'
  },
  'PHND': {
    'name': 'pitcher_hand'
  },
  'PLTN?': {
    'name': 'pltn_adv',
    'cb': lambda s: s != ''
  },
  'SalDiff': {
    'name': 'sal_diff'
  },
  'RankDiff': {
    'name': 'rank_diff'
  },
  'O/U': {
    'name': 'over_under'
  },
  'Line': {
    'name': 'line'
  },
  'Total': {
    'name': 'total'
  },
  'Movement': {
    'name': 'movement'
  },
  'AB': {
    'name': 'ab'
  },
  'AVG': {
    'name': 'avg'
  },
  'wOBA': {
    'name': 'woba'
  },
  'ISO': {
    'name': 'iso'
  },
  'OBP': {
    'name': 'oba'
  },
  'SLG': {
    'name': 'slg'
  },
  'OPS': {
    'name': 'ops'
  },
  'K%': {
    'name': 'k_perc'
  },
  'BB%': {
    'name': 'bb_perc'
  },
  'BABIP': {
    'name': 'bibp'
  },
  'Points': {
    'name': 'proj_pts'
  },
  'Pt/$/K': {
    'name': 'proj_val'
  }
}

class RotoProjParser(object):
    """
        Class that handles parsing projected stats data from RotoGrinders.com
    """

    def __init__(self, features, player_type, date_str):
        self.date_str = date_str
        self.player_type = player_type
        self.players_df = RotoProjParser.parse_data(features)
    
    @classmethod
    def build_name_map(cls, config):
        return { f'{key}': val['name'] for key, val in COLS_CONFIG.items() }


    @classmethod
    def parse_data(cls, features):
        columns, *rows = np.array(features).transpose()
        player_df = pd.DataFrame(data=rows, columns=columns)
        return RotoProjParser.transform_df(player_df)
    
    @classmethod
    def transform_df(cls, df):
        # Drop columns not in COLS_CONFIG (Rank, Average, pOWN% and ContR)
        for col in df.columns:
            if col not in COLS_CONFIG.keys():
                df.drop([col], axis=1, inplace=True)

        # Apply cleaner callbacks if applicable
        for col, config in COLS_CONFIG.items():
            if 'cb' in config:
                df[col] = [config['cb'](d) for d in df[col]]

        # Rename columns
        df.rename(index=str, columns=cls.build_name_map(COLS_CONFIG), inplace=True)
        return df

    def to_csv(self):
        path = f'output/{self.date_str}_{self.player_type}.csv'
        self.players_df.to_csv(path_or_buf=path, index=False, na_rep='NA')        