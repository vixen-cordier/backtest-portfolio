from chart import Chart
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np


class TestChart:
    def __init__(self):
        self.err = 0
        self.chart = Chart()
        self.chart.data = pd.read_csv('data.csv', parse_dates=['Date'])


    def test_set_flag(self):
        self.chart.set_flag()
        self.equal_test('FlagCloseDaily')
        self.equal_test('FlagCloseWeekly')
        self.equal_test('FlagCloseMonthly')


    def equal_test(self, col):
        err = 0
        msg = f"Equality test on {col} ... "
        for idx, equal in self.chart.data.apply(lambda x: x[f'{col}_expected'] == x[f'{col}'], axis = 1).items():
            if not equal:
                err = err + 1
                print(f"{msg} ERR on index {idx} -> expected:{self.chart.data.iloc[idx][f'{col}_expected']}, value:{self.chart.data.iloc[idx][f'{col}']}.")
        if err == 0:
            print(f"{msg} OK")
        self.err = self.err + err



if __name__ == '__main__':
    tchart = TestChart()
    tchart.test_set_flag()
    print(f"\n{tchart.err} error(s)") 


