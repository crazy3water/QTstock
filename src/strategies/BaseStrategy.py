class BaseStrategy(object):
    buy_nums = 2   #单位：手
    sell_nums = 1  #单位：手

    def set_buy_nums(self,nums):
        self.buy_nums = nums

    def set_sell_nums(self,nums):
        self.sell_nums = nums