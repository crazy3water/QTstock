class BaseStrategy(object):
    win = 12        #窗口
    buy_nums = 100   #单位：手
    sell_nums = 100  #单位：手

    trend_hist = []

    def set_buy_nums(self,nums):
        self.buy_nums = nums

    def set_sell_nums(self,nums):
        self.sell_nums = nums

    def win_statis(self, now, data):
        '''
        统计一个窗口内的均线斜率，用于判断均线趋势
        :return: 返回是否是上升期，是：1，否：0
        '''
        return 1 if sum([1 if now > ii else -1 for ii in data]) > 0 else 0

    def rolling(self,now, data, agg=min):
        '''
        目前价格窗口的agg函数值
        :param data:
        :param agg:
        :param w:
        :return:
        '''
        datamin = agg(data)
        return 1 if now>datamin else 0