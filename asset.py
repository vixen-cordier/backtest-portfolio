import yfinance as yf
import pandas as pd
import numpy as np
from typing import List

class Asset:
    def __init__(self, ticker):
        self.ticker: str = ticker
        self.data: pd.DataFrame

    def fetch_yf(self):
        ''' Fetch daily data from yahoo finance API'''
        self.data = yf.Ticker(self.ticker).history(period="max")[['Close']].reset_index()
        print(f"{self.ticker}:  {self.data.iloc[0]['Date'].strftime('%Y-%m-%d')} --> {self.data.iloc[-1]['Date'].strftime('%Y-%m-%d')}")

    def set_flag(self):
        ''' Flags end of Week and end of Month '''
        self.data['EndOfWeek'] = False
        self.data['EndOfMonth'] = False
        for idx in self.data.index[:-1]:
            curr_date = self.data.at[idx, 'Date']
            next_date = self.data.at[idx+1, 'Date']
            if curr_date.week != next_date.week:
                self.data.at[idx, 'EndOfWeek'] = True 
            if curr_date.month != next_date.month:
                self.data.at[idx, 'EndOfMonth'] = True 

    def mm_daily(self, mms: List[int]):
        ''' Moving average daily '''
        for mm in mms:
            self.data[f'MM{mm}Daily'] = ""
            for idx in self.data.index[mm-1:]:
                self.data.at[idx, f'MM{mm}Daily'] = np.mean(self.data.iloc[idx-mm+1:idx+1]['Close'])

    def mm_weekly(self, mms: List[int]):
        ''' Moving average weekly '''
        data_weekly = self.data[self.data['EndOfWeek'] == True].reset_index(drop=True)
        for mm in mms:
            data_weekly[f'MM{mm}Weekly'] = ""
            for idx in range(mm-1, data_weekly.shape[0]):
                data_weekly.at[idx, f'MM{mm}Weekly'] = np.mean(data_weekly.iloc[idx-mm+1:idx+1]['Close'])
            self.data = self.data.merge(data_weekly[['Date', f'MM{mm}Weekly']], on='Date', how='left')


if __name__ == '__main__':
    assets: List[Asset] = None
    # tickers = ['SPY','QQQ','IWM','XLE','TLT','GLD','ESE.PA','PUST.PA','RS2K.PA','BRE.PA','OBLI.PA','DBXN.F','GOLD.PA','BTC-USD','EURUSD=X']
    # for ticker in tickers:
    for ticker in ['SPY']:
        asset = Asset(ticker)
        asset.fetch_yf()
        asset.set_flag()
        asset.mm_daily([20])
        asset.mm_weekly([20])
        assets.append(asset)
