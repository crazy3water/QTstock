import tushare as ts
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