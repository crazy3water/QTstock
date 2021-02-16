import backtrader as bt

class MyIndicatorTest(bt.Indicator):
    # plotinfo = dict(
    #     plot=True,
    #     subplot=False,
    #     plotname='',
    #     plotabove=False,#使数据显示到指标上
    # )
    #
    # lines = (
    #     "MACD_RSI_line",
    #     "buy_signal",
    #     "macdHisto"
    # )
    #
    # params = dict(codes=[])
    # plotinfo = dict(subplot=True)
    #
    # def __init__(self):
    #     super(MyIndicatorTest, self).__init__()
    #     index_data_name = "self.dnames.code_"+self.p.codes[0]
    #
    #     # 引用数据
    #     # self.l.MACD_RSI_line = bt.Max(bt.ind.RelativeStrengthIndex(eval(index_data_name)), 60.0)
    #     RSI = bt.ind.RelativeStrengthIndex(eval(index_data_name))
    #     self.l.buy_signal = bt.If(bt.Cmp(RSI, 50.0),10.0,0) #是否大于60


    lines = ('mid','top','bot',)
    params = (("codes",[]),
                ('maperiod',5),
              ('ema_10',10),
              ('highRate',1.2),
              ('lowRate',0.85),)
    #与价格在同一张图
    plotinfo = dict(subplot=False)
    def __init__(self,data):
        # self.l.mid = bt.ind.EMA(self.data, period=self.p.maperiod)
        # self.l.now = bt.indicators.SimpleMovingAverage(
        #     self.data, period=self.p.maperiod)
        #
        # self.l.sub = self.l.now - self.l.mid
        #计算上中下轨线
        # self.l.mid=bt.ind.EMA(ema,period=self.p.period)
        # self.l.top=bt.ind.EMA(self.mid*self.p.highRate,\
        #                       period=self.p.period)
        # self.l.bot=bt.ind.EMA(self.mid*self.p.lowRate,\
        #                       period=self.p.period)
        super(MyIndicatorTest, self).__init__()
        self.l.mid = data - bt.ind.EMA(data, period=self.p.ema_10)




