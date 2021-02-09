from test.strategies.MultiStrategy import MultiStrategy

class StrategyTest(MultiStrategy):
    time_windows = 5
    def low_RSI_min(self):
        '''
        判断RSI底部  左侧>最底部<右侧
        :param code_i:
        :return:
        '''
        # 判断RSI前一天是时间窗口底部
        if self.rsis[0]>self.rsis[-1] and \
                self.rsis[-2]>self.rsis[-1]:
            return True
        return False

    def low_MACD(self):
        # 判断MACD底部
        if self.macd_ps[0]>self.macd_ps[-1] and \
                self.macd_ps[-2]>self.macd_ps[-1]:
            return True
        return False

    def boll_buy(self):
        '''
        使用布林策略 买入
        :param code_i:
        :return:
        '''
        now_p = self.datas[0]
        bot_p = self.lines.bot[-1]
        if self.datas[0] < self.lines.bot[-1]:
            return True
        return False

    def boll_sell(self):
        if self.datas[0] > self.lines.top[-1]:
            return True
        return False

    def high_RSI_max(self):
        '''
        判断RSI顶部  左侧 < 最顶部 > 右侧
        :param code_i:
        :return:
        '''
        # 判断RSI前一天是时间窗口底部
        if self.rsis[0] < self.rsis[-1] and \
                self.rsis[-2]<self.rsis[-1]:
            return True
        return False

    def high_MACD(self):
        # 判断MACD顶部
        if self.macd_ps[0]<self.macd_ps[-1] and \
                self.macd_ps[-2]<self.macd_ps[-1]:
            return True
        return False

    def MACD_0(self):
        if -0.05< self.macd_ps[0] < 0.05 :
            return True
        return False

    def get_buy_strategy(self):
        '''
        买入逻辑
        :param code_i:
        :return:
        '''
        if self.day_count > 10:
            if self.rsis[-1] < 35 \
                    and self.macd_ps[0]<0 \
                    and self.MACD_0()\
                    and self.low_RSI_min():
                return True
        return False

    def get_sell_strategy(self):
        '''
        卖出逻辑
        :param code_i:
        :return:
        '''
        if self.day_count > 10:
            if self.rsis[-1] > 80 \
                    and self.high_RSI_max():
                return True
        return False

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("code:{}".format(self.inds.keys()),doprint=True)

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        # if not self.position:#判断是否有仓位

        if self.get_buy_strategy():
            # if not self.positionsbyname["code_"+self.params.codes[i]]:
            if self.broker_buy_control() > 0:
                self.order = self.buy(size=self.buy_nums)

        if self.get_sell_strategy():
            num = int(self.positionsbyname["code_"+self.params.code].size/2)
            if num<100:
                num = int(self.positionsbyname["code_"+self.params.code].size)
            if self.positionsbyname["code_"+self.params.code].size > 0:
                self.order = self.sell(size=num) #size 交易单位1股 size=100 一手   percents

        self.day_count += 1