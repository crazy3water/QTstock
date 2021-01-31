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
        original_rate=[], # [("000001",0.2)]
    )
    def __init__(self,codes,sourceData = r"H:\MyProject\QuantitativeTrading\QT_2021_1_11\data\ts_data"):
        #准备数据
        self.codes = codes
        self.sourceData = sourceData

        self.cerebro = None
        self.ready_cerebro()    # 创建框架
        self.ready_broker()     # 准备券商（包括初始资金、印花税等）
        self.ready_strategy()   # 准备交易策略
        self.ready_data((2018,1,1),(2020,12,31))    #准备数据
        self.ready_analyzers()  #准备评价指标(年化利率等)
        self.main()

    def check_data(self):
        return FindData(dataPath=self.sourceData,
                        codes=self.codes,
                        fromLocal=False
                        )

    def ready_data(self,fromDate,toDate):
        findData = self.check_data()
        fromdate = datetime.datetime(fromDate[0], fromDate[1], fromDate[2])
        todate = datetime.datetime(toDate[0], toDate[1], toDate[2])
        # 在cerebro中添加数据
        for code in self.codes:
            data = findData.get_data(code,
                                          "%d-%d-%d"%(fromDate[0], fromDate[1], fromDate[2]),
                                          "%d-%d-%d"%(toDate[0], toDate[1], toDate[2])
                                          )
            feeddata = bt.feeds.PandasData(dataname=data,
                                       fromdate=fromdate,
                                       todate=todate
                                       )
            self.cerebro.adddata(feeddata, name="code_%s" % code)

            self.params["original_rate"].append((code,"%.2f"%((data.close[-1] - data.close[0])/data.close[0]) ))

    def ready_cerebro(self):
        #准备cerebro
        self.cerebro = bt.Cerebro()

    def ready_broker(self):
        #准备代理
        #初始资金
        self.cerebro.broker.set_cash(1e4)
        #交易费用
        self.cerebro.broker.setcommission(commission=0.00003)

    def ready_strategy(self):
        self.cerebro.addstrategy(StrategyTest1.StrategyTest,
                                    codes=self.codes)

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
            style="candle",
            barup="#FF0033",
            bardown="#32CD32",
            volup="#F66269",
            voldown="#43A047",
        )

        self.cerebro.plot(
            params=params
        )

    def main(self):
        back = self.cerebro.run()

        ratio_list = self.get_analyzers(back)

        ratio_df = pd.DataFrame(ratio_list, columns=['SharpeRatio', 'APR', 'Total_return', 'DrawDown'])

        print('\n', ratio_df.head())

        for i in range(len(self.codes)):
            print("股票code:{},原始收益:{}\n".format(self.params["original_rate"][i][0],self.params["original_rate"][i][1]) )

        self.plot()


if __name__ == "__main__":
    # RunStrtegy(codes=["000001","000589","002385","600893"])
    RunStrtegy(codes=["002385"])
    # RunStrtegy(codes=["002385"])