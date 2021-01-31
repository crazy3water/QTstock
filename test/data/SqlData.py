import tushare as ts
import os
import pandas as pd
from sqlalchemy import create_engine

class SqlData(object):
    def __init__(self):
        # 建立数据库连接
        self.conn = create_engine("mysql+pymysql://root:root@localhost:3306/stocks_his_price")

    def creatCode(self,code):
        today_all = ts.get_k_data(
            code=code
        )
        today_all.to_sql(name="CodeName20_8_21", con=self.conn, if_exists="replace", index=False)