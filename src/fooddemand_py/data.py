import pandas as pd
from datetime import datetime

def init_data(file_path):
    df = read_data(file_path=file_path)
    return add_week_date(df=df)

def read_data(file_path):
    df = pd.read_csv(file_path)
    return df

def add_week_date(df):
    # Get maximum & minimum weeks
    max_week = df['week'].max()

    week = pd.date_range(start=datetime(2022,1,3),
                         periods=max_week,
                         freq='W-MON'
                         )

    pd_week = pd.DataFrame({'calendar_date':week, 'week':pd.RangeIndex(1,(max_week+1)).to_series()})

    df = df.merge(pd_week, on='week')
    df = df.drop(['week'], axis=1)
    
    return df

def aggregate_df(df):
    df=df\
        .groupby(['center_id', 'calendar_date'], as_index=False)\
        .agg({'num_orders': 'sum'})\
        .reset_index()
    
    return df

def create_test_train(df, date):
    train = df.loc[df['calendar_date'] < date]
    valid = df.loc[(df['calendar_date'] >= date)]
    return train, valid