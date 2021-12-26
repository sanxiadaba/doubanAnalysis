import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from collections import defaultdict
data = pd.read_excel('./Top250.xls')

df_1=data["年份"]
df_1=list(df_1)
dic=defaultdict(int)
for i in df_1:
    dic[i]+=1
year=[]
count=[]
for i in range(1930,2021):
    if i in dic:
        year.append(i)
        count.append(dic[i])
        
bar = Bar()
bar.add_xaxis(year)
bar.add_yaxis("上映数目",count)
bar.set_global_opts(title_opts=opts.TitleOpts(title="各年份电影上映数量",subtitle='上映数目'),
                   toolbox_opts=opts.ToolboxOpts(is_show=True))
bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))
bar.render_notebook()    # 在 notebook 中展示
bar.render("年份与数量关系.html") 



# 评价人数的图
df = data.sort_values(by='影片评价人数', ascending=True)
c = (
    Bar()
        .add_xaxis(df['影片中文名'].values.tolist()[-20:])
        .add_yaxis('评价人数', df['影片评价人数'].values.tolist()[-20:])
        .reversal_axis()
        .set_global_opts(
        title_opts=opts.TitleOpts(title='电影评价人数'),
        yaxis_opts=opts.AxisOpts(name='片名'),
        xaxis_opts=opts.AxisOpts(name='人数'),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
    )
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .render('电影评价人数前二十.html')
)


