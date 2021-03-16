import tushare
import os
import pandas as pd

class FindData(object):
    para = dict(
        code=None,
        dataPath=None
        )
    def __init__(self,dataPath=r"tsdata/",code=None,fromLocal=False,ktype='D',start='',end=''):
        # time = xxxx-xx-xx
        super(object,self).__init__()
        self.dataPath = dataPath
        self.para["code"] = code
        self.fromLocal = fromLocal
        self.start = start
        self.end = end
        self.ktype = ktype

    def getCodeWithName(self,date=None):
        #用于查找代码与名字对应
        return tushare.get_today_all().to_csv(r"D:\Downloads\lp\QTstock-main\QTstock-main\temp/get_today_all.csv")

    def check_exits_files(self):
        # 检查指定文件夹中是否存在该代码的数据，如果存在则跳过，不存在去tushare下载
        list_files = os.listdir(self.dataPath)
        exist_codes = [file_name.split('_')[1] for file_name in list_files]
        if self.para["code"] not in exist_codes:
            self.get_data_tushare(code=self.para["code"],start=self.start,end=self.end)

    def get_data(self,code):
        if self.fromLocal:
            self.check_exits_files()
            return pd.read_csv(os.path.join(self.dataPath, "tushare_%s.csv" % (code)), index_col=0, parse_dates=True)
        else:
            return self.get_data_tushare(code,
                                         ktype=self.ktype,
                                         start=self.start,
                                         end = self.end)


    def get_data_tushare(self,code,ktype ='D',start='2020-01-01',end="2020-12-31"):
        '''
        单代码获取数据
        :return:
        '''
        dfData = tushare.get_k_data(code = code,
                                    start= start,
                                    end = end,
                                    ktype =ktype,
                                    retry_count=3,
                                    pause=0.001).sort_index()
        dfData.index = pd.to_datetime(dfData.date)
        dfData['openinterest'] = 0
        if self.fromLocal:
            dfData.to_csv(os.path.join(self.dataPath, "tushare_{}.csv".format(code)))
        return dfData

if __name__ == "__main__":
    # df = pd.DataFrame()
    # df.to_csv(r"D:\Downloads\lp\QTstock-main\QTstock-main\temp/temp.csv")

    findData = FindData()

    # findData.getCodeWithName("2021-03-15")
