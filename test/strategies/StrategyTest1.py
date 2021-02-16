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

    def statis_buy(self,now,data):
        if self.win_statis(now, data) == 1 and self.rolling(now,data) == 1:  # 趋势上升
            return True
        return False

    def statis_sell(self,now,data):
        if self.win_statis(now, data) == 0:  # 趋势下降
            return True
        return False

    def get_buy_strategy(self):
        '''
        买入逻辑
        :param code_i:
        :return:
        '''
        if self.day_count > self.win:
            for i, d in enumerate(self.datas):
                if d._name in self.inds.keys():
                    now = d.array[self.day_count]
                    data = d.array[self.day_count - self.win:self.day_count]
                    self.trend_hist.append(self.win_statis(now, data))
                    if self.statis_buy(now, data):
                        return True
        return False

    def get_sell_strategy(self):
        '''
        卖出逻辑
        :param code_i:
        :return:
        '''
        if self.day_count > self.win:
            for i, d in enumerate(self.datas):
                if d._name in self.inds.keys():
                    now = d.array[self.day_count]
                    data = d.array[self.day_count - self.win:self.day_count]
                    self.trend_hist.append(self.win_statis(now, data))
                    if self.statis_sell(now,data):
                        return True
        return False

    def next(self):
        self.log("code:{}".format(self.inds.keys()),doprint=False)


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
            # num = int(self.positionsbyname["code_"+self.params.code].size/2)
            # if num<100:
            #     num = int(self.positionsbyname["code_"+self.params.code].size)
            if self.positionsbyname["code_"+self.params.code].size > 0:
                self.order = self.sell(size=self.sell_nums) #size 交易单位1股 size=100 一手   percents

        self.day_count += 1