'''
功能：用于制作数据库
描述：首次使用时本机不存在数据库，所以此程序用于制作数据库
'''
import tushare
import pandas as pd

from src.dataSet.FindData import FindData
from src.tools.Properties import Properties

class MakeDataBase(object):
    def __init__(self):
        self.findData = FindData()
        pass

    def makeCodeWithName(self):
        # 用于制作代码与名字对应的数据库
        # self.findData.getCodeWithName()保存一个pd文件
        df = pd.read_csv(r"D:\Downloads\lp\QTstock-main\QTstock-main\temp\get_today_all.csv",dtype=str)
        return df.code,df.name

    def makeCodeWithPrice(self,code):
        dataDF_standard = self.findData.get_data('000001')
        print(dataDF_standard.head(10))
        dataDF = self.findData.get_data(code)
        print(dataDF.head(10))
        dataDF = pd.merge(dataDF_standard,dataDF,left_index=True,right_index=True,how="outer")
        print(dataDF)
        return dataDF


if __name__ == "__main__":
    mdb = MakeDataBase()
    codes,name = mdb.makeCodeWithName()
    mdb.makeCodeWithPrice(codes.values[0])
    # print(type(codes.values[0]))
    # print(mdb.makeCodeWithPrice(codes.values[0]))