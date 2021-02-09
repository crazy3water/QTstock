import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table
import matplotlib.pyplot as plt

dataPath = r"D:\stock_analys\QTstock\data\ts_data\tushare_002459.csv"

codeData = pd.read_csv(dataPath)
print(codeData.head())

high = codeData.high
low = codeData.low
close = codeData.close

b = sm.add_constant(low) # 添加常数项
model = sm.OLS(high,b)
model = model.fit()

st, data, ss2 = summary_table(model, alpha=0.05)
low.plot()
close.plot()
model.fittedvalues.plot()
plt.legend(["low",
            "close",
            "model_predict"])
plt.show()