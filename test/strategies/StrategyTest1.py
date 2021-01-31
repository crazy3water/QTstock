from test.strategies.MultiStrategy import MultiStrategy

class StrategyTest(MultiStrategy):
    time_windows = 5
    def low_RSI_min(self,code_i):
        '''
        判断RSI底部  左侧>最底部<右侧
        :param code_i:
        :return:
        '''
        # 判断RSI前一天是时间窗口底部
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

    def boll_buy(self,code_i):
        '''
        使用布林策略 买入
        :param code_i:
        :return:
        '''
        now_p = self.datas[code_i][0]
        bot_p = self.lines.bot[code_i][-1]
        if self.datas[code_i][0] < self.lines.bot[code_i][-1]:
            return True
        return False

    def boll_sell(self,code_i):
        if self.datas[code_i][0] > self.lines.top[code_i][-1]:
            return True
        return False

    def high_RSI_max(self,code_i):
        '''
        判断RSI顶部  左侧 < 最顶部 > 右侧
        :param code_i:
        :return:
        '''
        # 判断RSI前一天是时间窗口底部
        if self.rsis[code_i][0] < self.rsis[code_i][-1] and \
                self.rsis[code_i][-2]<self.rsis[code_i][-1]:
            return True
        return False

    def high_MACD(self,code_i):
        # 判断MACD顶部
        if self.macd_ps[code_i][0]<self.macd_ps[code_i][-1] and \
                self.macd_ps[code_i][-2]<self.macd_ps[code_i][-1]:
            return True
        return False

    def MACD_0(self,code_i):
        if -0.05< self.macd_ps[code_i][0] < 0.05 :
            return True
        return False

    def get_buy_strategy(self,code_i):
        '''
        买入逻辑
        :param code_i:
        :return:
        '''
        if self.day_count > 10:
            if self.rsis[code_i][-1] < 35 \
                    and self.macd_ps[code_i][0]<0 \
                    and self.MACD_0(code_i)\
                    and self.low_RSI_min(code_i) or self.boll_buy(code_i):
                return True
        return False

    def get_sell_strategy(self,code_i):
        '''
        卖出逻辑
        :param code_i:
        :return:
        '''
        if self.day_count > 10:
            if self.rsis[code_i][-1] > 80 \
                    and self.high_RSI_max(code_i) or self.boll_sell(code_i):
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