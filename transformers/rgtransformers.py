import pandas as pd
import numpy as np

from configs.rgconfigers import RGConfiger

class RGTransformer(object):
    """
        Class that handles parsing projected stats data from RotoGrinders.com
    """

    def __init__(self, configer, columns):
        self.configer = configer
        self.stats_df = self.build_stats_df(columns)
    
    def build_stats_df(self, columns):
        columns, *rows = np.array(columns).transpose()
        stats_df = pd.DataFrame(data=rows, columns=columns)
        return self.clean_df(stats_df)
    
    def clean_df(self, df):
        # Drop columns missing data (Rank, Average, pOWN% and ContR)
        drop_cols = self.configer.get_drop_columns(df.columns)
        df.drop(columns=drop_cols, inplace=True)

        # Apply cleaner callbacks if applicable
        for col in self.configer.get_columns():
            cb = self.configer.get_cleaner_callback(col)
            if cb:
                df[col] = [cb(d) for d in df[col]]

        # Rename columns
        df.rename(index=str, columns=self.configer.get_name_map(), inplace=True)
        return df
    
    def to_csv(self, date, playertype):
        stats_path = 'output/{}_{}.csv'.format(date.strftime('%Y-%m-%d'), playertype)
        self.stats_df.to_csv(path_or_buf=stats_path, index=False, na_rep='NA')
