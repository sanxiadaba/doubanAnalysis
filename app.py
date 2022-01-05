from flask import Flask, render_template
app = Flask(__name__ ,template_folder='template')
import pandas as pd
n_row=250


@app.route('/',methods=["GET"])
def home():
    df=pd.read_excel('./Top250.xls')
    movies=df[["影片中文名","影片详情链接","影片评分","影片评价人数","影片概况"]]
    names=list(movies["影片中文名"][0:n_row])
    links=list(movies["影片详情链接"][0:n_row])
    scores=list(movies["影片评分"][0:n_row])
    counts=list(movies["影片评价人数"][0:n_row])
    overviews=list(movies["影片概况"][0:n_row])
    # print(names)
    return render_template("douban.html",n=list(range(1,n_row+1)),names=names,links=links,scores=scores,counts=counts,overviews=overviews)




if __name__ == '__main__':
    app.run(host="127.0.0.1",port=1237,debug=True)