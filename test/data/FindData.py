import tushare
import os
import pandas as pd

class FindData(object):
    para = dict(
        code=None,
        codes=[],
        dataPath=None
        )
    def __init__(self,dataPath=r"tsdata/",codes=[],fromLocal=False):
        super(object,self).__init__()
        self.dataPath = dataPath
        self.para["codes"] = codes
        self.fromLocal = fromLocal

        self.check_exits_files()

    def check_exits_files(self):
        # 检查指定文件夹中是否存在该代码的数据，如果存在则跳过，不存在去tushare下载
        if self.fromLocal:
            list_files = os.listdir(self.dataPath)
            exist_codes = [file_name.split('_')[1] for file_name in list_files]
            for codei in self.para["codes"]:
                if codei not in exist_codes:
                    self.get_data_tushare(codei)

    def get_data(self,code,start,end):
        if self.fromLocal:
            return pd.read_csv(os.path.join(self.dataPath, "tushare_%s" % (code)), index_col=0, parse_dates=True)
        else:
            return self.get_data_tushare(code,start,end)


    def get_data_tushare(self,code,start='2020-01-01',end="2020-12-31"):
        '''
        单代码获取数据
        :return:
        '''
        dfData = tushare.get_k_data(code = code,
                                    start= start,
                                    end = end,
                                    ktype ='D',
                                    retry_count=3,
                                    pause=0.001).sort_index()
        dfData.index = pd.to_datetime(dfData.date)
        dfData['openinterest'] = 0
        if self.fromLocal:
            dfData.to_csv(os.path.join(self.dataPath, "tushare_%s" % (code)))
        return dfData