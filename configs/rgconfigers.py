import re

RG_PITCHER_COLS = {
    'Name': {
        'name': 'name'
    }
}

RG_HITTER_COLS = {
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

class RGConfiger(object):

    # Player types
    HITTER = 'hitter'
    PITCHER = 'pitcher'
    PLAYER_TYPES = [HITTER, PITCHER]

    # Site type
    DF = 'draftkings'
    FD = 'fanduel'
    SITE_TYPES = [DF, FD]

    def __init__(self, player_type, site):
        self.columns = RG_HITTER_COLS if player_type == RGConfiger.HITTER else RG_PITCHER_COLS   
        self.player_type = player_type
        self.site = site

    def get_name_map(self):
        return { f'{key}': val['name'] for key, val in self.columns.items() }

    def get_url(self, date):
        # TODO: Add arg validation
        return f"https://rotogrinders.com/projected-stats/mlb-{self.player_type}?site={self.site}&date={date.strftime('%Y-%m-%d')}"

    def get_drop_columns(self, columns):
        drop_cols = []
        for col in columns:
            if col not in self.columns.keys():
                drop_cols.append(col)
        return drop_cols
    
    def get_cleaner_callback(self, col_name):
        col = self.columns[col_name]
        if 'cb' in col:
            return col['cb']
    
    def get_columns(self):
        return self.columns.keys()
