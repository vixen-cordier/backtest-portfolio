import yfinance as yf
import pandas as pd
import numpy as np
from typing import List

class Graphics:
    def __init__(self, ticker):
        ''' Initialisation of graphic '''
        self.ticker: str = ticker
        self.data: pd.DataFrame

    def fetch_yf(self):
        ''' Fetch daily data from yahoo finance API'''
        self.data = yf.Ticker(self.ticker).history(period="max")[['Close']].reset_index()
        print(f"{self.ticker}:  {self.data.iloc[0]['Date'].strftime('%Y-%m-%d')} --> {self.data.iloc[-1]['Date'].strftime('%Y-%m-%d')}")

    def set_flag(self):
        ''' Flags end of Week and end of Month '''
        self.data['FlagCloseDaily'] = False
        self.data['FlagCloseWeekly'] = False
        self.data['FlagCloseMonthly'] = False
        for idx in self.data.index[:-1]:
            curr_date = self.data.at[idx, 'Date']
            next_date = self.data.at[idx+1, 'Date']
            if curr_date.day != next_date.day:
                self.data.at[idx, 'FlagCloseDaily'] = True 
            if curr_date.week != next_date.week:
                self.data.at[idx, 'FlagCloseWeekly'] = True 
            if curr_date.month != next_date.month:
                self.data.at[idx, 'FlagCloseMonthly'] = True 

    def add_mm(self, mm: int, time='Daily'):
        ''' Add moving average to the graph data (Daily|Weekly|Monthly) '''
        data_mm = self.data[self.data[f'FlagClose{time}'] == True].reset_index(drop=True)
        data_mm[f'MM{mm}{time}'] = ""
        for idx in data_mm.index[mm-1:]:
            data_mm.at[idx, f'MM{mm}{time}'] = np.mean(data_mm.loc[idx-mm+1:idx+1]['Close'])
        self.data = pd.merge(self.data, data_mm[['Date', f'MM{mm}{time}']], on='Date', how='left').fillna(method='bfill')


    def add_mom(self, mom: int, time='Daily'):
        ''' Add momentum value to the graph data (Daily|Weekly|Monthly) '''
        data_mom = self.data[self.data[f'FlagClose{time}'] == True].reset_index(drop=True)
        data_mom[f'Mom{mom}{time}'] = ""
        for idx in data_mom.index[mom:]:
            data_mom.at[idx, f'Mom{mom}{time}'] = data_mom.at[idx, 'Close'] / data_mom.at[idx-mom, 'Close'] - 1
        self.data = pd.merge(self.data, data_mom[['Date', f'Mom{mom}{time}']], on='Date', how='left').fillna(method='bfill')

    def add_rsi(self, rsi, time='Daily'):
        ''' Add RSI index to the graph data (Daily|Weekly|Monthly) '''
        data_rsi = self.data[self.data[f'FlagClose{time}'] == True].reset_index(drop=True)
        data_rsi[f'RSI{rsi}{time}'] = ""
        data_rsi['tmp_var'] = 0
        data_rsi['tmp_bull'] = 0
        data_rsi['tmp_bear'] = 0
        for idx in data_rsi.index[1:]:
            data_rsi.at[idx,'tmp_var'] = data_rsi.at[idx, 'Close'] / data_rsi.at[idx-1, 'Close'] -1
            if data_rsi.at[idx,'tmp_var'] > 0:
                data_rsi.at[idx,'tmp_bull'] = data_rsi.at[idx,'tmp_var']
            else:
                data_rsi.at[idx,'tmp_bear'] = data_rsi.at[idx,'tmp_var']
        for idx in data_rsi.index[rsi:]:
            data_rsi.at[idx, f'RSI{rsi}{time}'] = 100 - (100 / (1 + np.mean(data_rsi.loc[idx-rsi:idx]['tmp_bull']) / np.mean(data_rsi.loc[idx-rsi:idx]['tmp_bear'])))
        self.data = pd.merge(self.data, data_rsi[['Date', f'RSI{rsi}{time}']], on='Date', how='left').fillna(method='bfill') 
















# if __name__ == '__main__':
#     assets: List[Asset] = None
#     # tickers = ['SPY','QQQ','IWM','XLE','TLT','GLD','ESE.PA','PUST.PA','RS2K.PA','BRE.PA','OBLI.PA','DBXN.F','GOLD.PA','BTC-USD','EURUSD=X']
#     # for ticker in tickers:
#     for ticker in ['SPY']:
#         asset = Asset(ticker)
#         asset.fetch_yf()
#         asset.set_flag()
#         asset.mm_daily([20])
#         asset.mm_weekly([20])
#         assets.append(asset)
