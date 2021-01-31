# from __future__ import (absolute_import, division, print_function, unicode_literals)
import tushare
import os
import pandas as pd
import datetime

import backtrader as bt
import backtrader.analyzers as btanalyzers

from src.my_indicators.MyIndicators import MyIndicatorTest
from src.strategies.BaseStrategy import BaseStrategy

def get_data(code):
    dfData = tushare.get_k_data(code=code,
                       start = '2020-01-01',
                       end = "2020-12-31",
                       ktype = 'D',
                       retry_count = 3,
                       pause = 0.001).sort_index()
    dfData.index = pd.to_datetime(dfData.date)
    dfData['openinterest'] = 0
    dfData.to_csv(os.path.join(dataPath,"tushare_%s"%(code)))
    return dfData


class MultiStrategy(bt.Strategy,BaseStrategy):
    params = (
        ('codes',[]),
        ('maperiod', 15),
        ('printlog', False),
        # MACD
        ("period_me1",12),
        ("period_me2",26),
        ("period_signal",9),

    )
    def __init__(self):

        self.dataclose = self.datas[0].close
        self.order = None

        self.day_count = 1

        #引用数据
        self.index_data_names = ["self.dnames.code_"+str(code) for code in self.p.codes]
        self.macd_ps = []
        self.rsis = []

        self.MACD_RSI_signal = MyIndicatorTest(codes=self.p.codes)

        # indicators 技术指标
        for index_data_name in self.index_data_names:
            macd = bt.ind.MACDHisto(eval(index_data_name))

            self.macd_ps.append(macd.lines.histo)

            rsi = bt.ind.RelativeStrengthIndex(eval(index_data_name))
            self.rsis.append(rsi.lines.rsi)

        buy_sigs = []

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def log(self,txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def get_buy_strategy(self,code_i):
        return False
        # if self.day_count > 10:
        #     if self.macd_ps[code_i][0]<0 and self.macd_ps[code_i][-2] < self.macd_ps[code_i][-1] and self.macd_ps[code_i][0] > self.macd_ps[code_i][-1] and \
        #             self.rsis[code_i][0] < 40 and \
        #             self.rsis[code_i][-1]<self.rsis[code_i][-2] and self.rsis[code_i][-1] < self.rsis[code_i][0]:
        #         return True
        #     else:
        #         return False


    def get_sell_strategy(self,code_i):
        return False
        # if self.day_count > 10:
        #     if self.macd_ps[code_i][0]>0 and self.macd_ps[code_i][-1] >= self.macd_ps[code_i][-2] and self.macd_ps[code_i][0] < self.macd_ps[code_i][-1] and \
        #             self.rsis[code_i][0] > 60:
        #         return True
        #     else:
        #         return False

    def broker_buy_control(self,code_i):
        # 查看目前多少钱，够不够买 self.buy_nums
        broker_value = self.broker.getvalue()   #   目前现金
        return int(broker_value/(self.datas[code_i].close[0]*self.buy_nums*100))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return


        # Check if we are in the market
        # if not self.position:#判断是否有仓位

        for i in range(len(self.params.codes)):
            if self.get_buy_strategy(i):
                # if not self.positionsbyname["code_"+self.params.codes[i]]:
                if self.broker_buy_control(i) > 0:
                    code_data = eval("self.data"+str(i))
                    self.order = self.buy(code_data,size=1000)

        for i in range(len(self.params.codes)):
            if self.get_sell_strategy(i):
                num = int(self.positionsbyname["code_"+self.params.codes[i]].size/2)
                if self.positionsbyname["code_"+self.params.codes[i]].size > 0:
                    code_data = eval("self.data"+str(i))
                    self.order = self.sell(code_data,size=num) #size 交易单位1股 size=100 一手   percents

        self.day_count += 1

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.period_me1, self.broker.getvalue()), doprint=True)




if __name__ == "__main__":
    dataPath = r"H:\MyProject\QuantitativeTrading\QT_2021_1_11\data\ts_data"
    codes = [
        "000001",
    ]
    # code = "002385"
    list_files = os.listdir(dataPath)
    exist_codes = [file_name.split('_')[1] for file_name in list_files]
    if codes not in exist_codes:
        for code in codes:
            get_data(code)

    cerebro = bt.Cerebro()
    # 代理(经纪人) 设置初始金额，手  续费
    cerebro.broker.set_cash(1e6)
    cerebro.broker.setcommission(commission=0.00003)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=100) #买卖数量
    # cerebro.addsizer(bt.sizers.PercentSizer, percents=100) #买卖百分比

    # 添加策略
    cerebro.addstrategy(MultiStrategy,
                        codes=codes)

    # cerebro.optstrategy(TestStrategy,
    #                     period_me1=[6,12,18],
    #                     period_me2=[13, 26, 39],
    #                     printlog=False)

    # 添加数据
    for code in codes:
        data = pd.read_csv(os.path.join(dataPath,"tushare_%s"%(code)), index_col=0, parse_dates=True)
        data = bt.feeds.PandasData(dataname=data,
                                fromdate=datetime.datetime(2020, 1, 1),
                                todate=datetime.datetime(2020, 12, 31)
            )
        cerebro.adddata(data,name="code_%s" % code)


    #Analyzers
    cerebro.addanalyzer(btanalyzers.SharpeRatio,_name='sharpe')  #夏普率
    cerebro.addanalyzer(btanalyzers.Returns,_name='returns')     # rnorm100 年利率
    cerebro.addanalyzer(btanalyzers.DrawDown,_name='drawdown') # 回撤

    # 开始运行
    print("Starting value: %.2f" % cerebro.broker.get_value())
    back = cerebro.run()
    print("Now value: %.2f" % cerebro.broker.get_value())

    # 提取数据分析
    ratio_list = [[
        x.analyzers.sharpe.get_analysis()['sharperatio'],
        x.analyzers.returns.get_analysis()['rnorm100'],
        x.analyzers.returns.get_analysis()['rtot'],
        x.analyzers.drawdown.get_analysis()['max']['drawdown'],
                   ]

        for x in back
    ]

    ratio_df = pd.DataFrame(ratio_list,columns=['SharpeRatio','APR','Total_return','DrawDown'])

    print('\n', ratio_df.head())
    # 绘图
    params = dict(
        style="candle",
        barup = "#FF0033",
        bardown = "#32CD32",
        volup = "#F66269",
        voldown = "#43A047",
    )


    cerebro.plot(
        params = params
    )