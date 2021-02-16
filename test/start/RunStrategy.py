import tushare
import os
import pandas as pd
import datetime

import backtrader as bt
import backtrader.analyzers as btanalyzers

from src.my_indicators.MyIndicators import MyIndicatorTest
from test.data.FindData import FindData
from test.strategies.MultiStrategy import MultiStrategy
from test.strategies import StrategyTest1

class RunStrtegy():
    params = dict(
        original_rate=(), # [("000001",0.2)]
    )
    def __init__(self,code,cash=1e4,
                 fromLocal=False,
                 sourceData = r"H:\MyProject\QuantitativeTrading\QT_2021_1_11\data\ts_data"):
        #准备数据
        self.code = code
        self.init_cash = cash
        self.fromLocal = fromLocal
        self.sourceData = sourceData

        self.cerebro = None
        self.ready_cerebro()    # 创建框架
        self.ready_broker()     # 准备券商（包括初始资金、印花税等）
        self.ready_strategy()   # 准备交易策略
        self.ready_data(datetime.datetime(2020,1,1),datetime.datetime(2020,12,31))    #准备数据
        self.ready_analyzers()  #准备评价指标(年化利率等)
        self.main()

    def check_data(self,fromDate,toDate):
        return FindData(dataPath=self.sourceData,
                        code=self.code,
                        fromLocal=self.fromLocal,
                        ktype='D',
                        start=fromDate,
                        end=toDate
                        )

    def ready_data(self,fromDate,toDate):
        findData = self.check_data(fromDate.strftime("%Y-%m-%d"),toDate.strftime("%Y-%m-%d"))
        # 在cerebro中添加数据
        data = findData.get_data(self.code)

        feeddata = bt.feeds.PandasData(dataname=data,
                                       fromdate=fromDate,
                                       todate=toDate,
                                       timeframe=bt.TimeFrame.Days,
                                   )
        self.cerebro.adddata(feeddata, name="code_%s" % self.code)
        # self.cerebro.resampledata(feeddata,
        #                           timeframe=bt.TimeFrame.Months,
        #                           compression=1,    # 下载数据是N分钟，compression就是N
        #                           name="code_%s_resample" % self.code)

        self.params["original_rate"] = (self.code,"%.2f%%"%((data.close[-1]-data.close[0])*100/data.close[0]) )

    def ready_cerebro(self):
        #准备cerebro
        self.cerebro = bt.Cerebro()

    def ready_broker(self):
        #准备代理
        #初始资金
        self.cerebro.broker.set_cash(self.init_cash)
        #交易费用
        self.cerebro.broker.setcommission(commission=0.00003)

    def ready_strategy(self):
        self.cerebro.addstrategy(StrategyTest1.StrategyTest,
                                    code=self.code,
                                 init_value=self.init_cash)

    def ready_analyzers(self):
        # Analyzers
        self.cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')  # 夏普率
        self.cerebro.addanalyzer(btanalyzers.Returns, _name='returns')  # rnorm100 年利率
        self.cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')  # 回撤

    def get_analyzers(self,back):
        # 提取数据分析
        return [[
            x.analyzers.sharpe.get_analysis()['sharperatio'],
            x.analyzers.returns.get_analysis()['rnorm100'],
            x.analyzers.returns.get_analysis()['rtot'],
            x.analyzers.drawdown.get_analysis()['max']['drawdown'],
        ]

            for x in back
        ]

    def plot(self):
        # 绘图
        params = dict(
            style="bar",
            barup="red",
            bardown="green",
            volup="red",
            voldown="green",
            volume=False,
        )

        self.cerebro.plot(
            style="bar",
            barup="red",
            bardown="green",
            volup="red",
            voldown="green",
        )

    def main(self):
        back = self.cerebro.run()

        ratio_list = self.get_analyzers(back)

        ratio_df = pd.DataFrame(ratio_list, columns=['SharpeRatio', 'APR', 'Total_return', 'DrawDown'])

        print('\n', ratio_df.head())

        print("股票code:{},原始收益:{}\n".format(self.params["original_rate"][0],self.params["original_rate"][1]) )

        self.plot() #start=datetime.date(2018, 1, 1), end=datetime.date(2019, 12, 31),


if __name__ == "__main__":
    # RunStrtegy(codes=["000001","000589","002385","600893"])
    RunStrtegy(code="600519",
               cash=1e6,
               fromLocal=False,
               sourceData=r"D:\stock_analys\QTstock\data\ts_data")
