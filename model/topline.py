import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

class Topline:
    def __init__(self, df):
        self.df = self.get_topline_data(df)
    
    def get_topline_data(self, df):
        # 1. Ensure calendar_date is in datetime format
        df['calendar_date'] = pd.to_datetime(df['calendar_date'])

        # 2. Aggregate num_orders by center_id and date
        # We use .reset_index() to keep the structure flat
        df = df.groupby(['center_id', 'calendar_date'])['num_orders'].sum().reset_index()
        
        # 3. Rename columns to Nixtla requirements
        df = df.rename(columns={
            'center_id': 'unique_id',
            'calendar_date': 'ds',
            'num_orders': 'y'
        })

        # 4. Optional: Sort by ID and Date (recommended for clarity)
        df = df.sort_values(['unique_id', 'ds']).reset_index(drop=True)
        
        return df
    
    def fit(self):
        # 2. Instantiate the model
        # 'season_length' is crucial for SARIMA models (e.g., 12 for monthly)
        models = [AutoARIMA(season_length=52)]
        
        # 3. Setup StatsForecast
        sf = StatsForecast(
            models=models, 
            freq='W-MON',  # Frequency (Weekly)
            n_jobs=-1  # Use all CPU cores
        )

        # 4. Forecast
        forecasts = sf.forecast(df=self.df, h=52) # Forecast 12 weeks    ahead
        return forecasts