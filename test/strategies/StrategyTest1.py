from test.strategies.MultiStrategy import MultiStrategy

class StrategyTest(MultiStrategy):
    time_windows = 5
    def low_RSI(self,code_i):
        # 判断RSI底部
        if self.rsis[code_i][0]>self.rsis[code_i][-1] and \
                self.rsis[code_i][-2]>self.rsis[code_i][-1]:
            return True
        return False

    def low_RSI_min(self,code_i):
        # 判断RSI前一天是时间窗口底部
        prices_window = self.rsis[code_i].array[:self.day_count+1]
        prices = self.rsis[code_i][0]
        if self.rsis[code_i][0]>self.rsis[code_i][-1] and \
                self.rsis[code_i][-2]>self.rsis[code_i][-1]:
            return True
        return False

    def low_MACD(self,code_i):
        # 判断MACD底部
        if self.macd_ps[code_i][0]>self.macd_ps[code_i][-1] and \
                self.macd_ps[code_i][-2]>self.macd_ps[code_i][-1]:
            return True
        return False


    def get_buy_strategy(self,code_i):
        if self.day_count > 10:
            if self.rsis[code_i][0] < 35 and self.macd_ps[code_i][0]<0 and self.low_RSI(code_i) and self.low_RSI_min(code_i):
                return True
        return False
    def get_sell_strategy(self,code_i):
        if self.day_count > 10:
            if self.rsis[code_i][0] > 60:
                return True
        return False

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
                    self.order = self.buy(code_data,size=self.buy_nums)

        for i in range(len(self.params.codes)):
            if self.get_sell_strategy(i):
                num = int(self.positionsbyname["code_"+self.params.codes[i]].size/2)
                if num<100:
                    num = int(self.positionsbyname["code_"+self.params.codes[i]].size)
                if self.positionsbyname["code_"+self.params.codes[i]].size > 0:
                    code_data = eval("self.data"+str(i))
                    self.order = self.sell(code_data,size=num) #size 交易单位1股 size=100 一手   percents

        self.day_count += 1