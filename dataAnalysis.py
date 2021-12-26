import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# 基本设置
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False ## 设置正常显示符号

#读取数据
df=pd.read_excel('./Top250.xls') #数据读取

# 取出对应的数据
df_1=df[["影片评分","排名"]]
df_2=df[["影片评分","排名","影片评价人数"]]

# 图一
plt.figure(1)
sns.stripplot(x='影片评分',y='排名',data = df_1,jitter=True)

# 图二
plt.figure(2)
sns.regplot(x='影片评分',y='排名',data = df_1)

plt.figure(3)
sns.pairplot(df_2, kind="reg")
# 把图画出来
plt.show()