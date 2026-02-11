import pandas as pd
from datetime import datetime

class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self._init_data()
        # self.df = self._aggregate_df(self.df)

    def _init_data(self):
        df = self._read_data()
        df = self.add_week_date(df)
        return df

    def _read_data(self):
        return pd.read_csv(self.file_path)

    @staticmethod
    def add_week_date(df):
        max_week = df['week'].max()
        week_dates = pd.date_range(start=datetime(2022, 1, 3), periods=max_week, freq='W-MON')
        pd_week = pd.DataFrame({'calendar_date': week_dates, 'week': range(1, max_week + 1)})
        df = df.merge(pd_week, on='week')
        df = df.drop(['week'], axis=1)
        return df