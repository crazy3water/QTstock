'''
用于制作特征 API
X,Y
X，Y时间窗口的形式，涨跌幅
X 窗口X_w
Y 窗口Y_w之和
'''
import pandas as pd
import numpy as np

def rolling(data,agg,w=14):
    res=[]
    data_len = len(data)
    if data_len < w:
        return False
    for ii in range(w):
        res.append(0)
    for i in range(w, data_len):
        datause = data[i-w:i]
        res.append(agg(datause))
    return res

def statis_rate_rolling(emadata,w=14):
    '''
    统计一个窗口内的均线斜率，用于判断均线趋势
    :return: 返回是否是上升期，是：True，否：False
    '''
    res = []
    data_len = len(emadata)
    def win_statis(now,data):
        return 1 if sum([1 if now>ii else -1 for ii in data]) > 0 else 0

    for ii in range(w):
        res.append(0)
    for i in range(w, data_len):
        res.append(win_statis(emadata[i],emadata[i-w:i]))
    return res




def yali(High, Low, Close):
    '''
    压力位算法
    :param data:
    :return:
    '''

    # 由低到高排序
    # 枢轴点
    PivotPoint = (High + Low + Close) / 3
    # 支持位
    Support3 = PivotPoint + (High + Low) * 1.0
    Support2 = PivotPoint + (High + Low) * 0.618
    Support1 = PivotPoint + (High + Low) * 0.382

    # PivotPoint = (High + Low + Close) /3

    # 阻力位
    Resistance1 = PivotPoint + (High + Low) * 0.382
    Resistance2 = PivotPoint + (High + Low) * 0.618
    Resistance3 = PivotPoint + (High + Low) * 1.0
    return Support3, Support2, Support1, PivotPoint, Resistance1, Resistance2, Resistance3

if __name__ == "__main__":
    import matplotlib.pylab as plt
    from matplotlib.widgets import Cursor

    dataPath = r"D:\stock_analys\QTstock\data\ts_data\tushare_002459.csv"

    codeData = pd.read_csv(dataPath,index_col=1)
    codeData.index = pd.to_datetime(codeData.index)
    codeData["rate"] = (codeData.close - codeData.open)*100/codeData.open

    S_R = yali(codeData.high,codeData.low,codeData.close)
    close_max_my = rolling(codeData.close.values,np.max)
    close_min_my = rolling(codeData.close.values,np.min)

    Y = codeData.groupby(lambda x:x.weekday).mean()
    Y1_mean_5 = codeData["close"].rolling(5).mean().fillna(0)
    Y1_mean_10 = codeData["close"].rolling(10).mean().fillna(0)

    srr = statis_rate_rolling(Y1_mean_10.values)

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    codeData.close.plot(c='r')
    Y1_mean_5.plot(c='g',style='--')
    Y1_mean_10.plot(c='#808080',style='--')

    codeData["close_max_my"] = close_max_my
    codeData["close_min_my"] = close_min_my
    codeData.close_max_my.plot(c='b',style='--')
    codeData.close_min_my.plot(c='b',style='-.')

    cursor = Cursor(ax1,useblit=True, color='black', linewidth=0.7)

    ax2 = fig.add_subplot(212)

    codeData["srr"] = srr
    codeData.srr.plot(c='b',style='--')

    close = codeData.close.values

    codeData["min_yali"] = np.where(codeData.close.values - close_min_my > 0,1,0)
    codeData.min_yali.plot(c='r',style='-.')
    # ax3 = fig.add_subplot(213)

    plt.show()
