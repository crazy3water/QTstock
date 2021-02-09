import tushare as ts
from test.data.FindData import FindData
import os
import pandas as pd
import datetime

import backtrader as bt

class ChooseCode(object):
    def __init__(self):
        pass

    def getAllCodeData(self):
        all_data = ts.get_today_all()

    def next(self):
        pass

    def choosePrice(self):
        pass

    def chooseMLL(self):
        '''
        选择毛利率
        :return:
        '''
        pass

    def chooseJLR(self):
        '''
        选择净利润
        :return:
        '''
        pass

if __name__ == "__main__":
    dataPath = r"D:\stock_analys\QTstock\data\ts_data"
    codes = ["000001"]
    fromLocal = False

    findData = FindData(dataPath=dataPath,
                         codes=codes,
                         fromLocal=fromLocal
                         )

    data = findData.get_data(code=codes[0],
                      start="2020-01-01",
                      end="2020-12-31")

    print(data.head())