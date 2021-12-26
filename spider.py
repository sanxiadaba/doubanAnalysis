from bs4 import BeautifulSoup     #网页解析
import re       #正则表达式
import urllib.request,urllib.response       #制定URL，获取网页数据
import xlwt     #进行excel操作
from constant import cookies,n
n_1=n
n_2=25*n_1

# 这一部分是搜索年份的re
pt=r'\b\d{4}\b'
rc=re.compile(pt)
def reSearch(s):
    rs=re.search(rc,s)
    return rs.group(0)

def askURL(url):
    # 这里是伪装了下
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
        "Cookie":cookies

    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except Exception as e:
        print(e)
    return html

#影片详情链接
findLink = re.compile(r'<a href="(.*?)">')         #创建正则表达式对象，表示规则(字符串的模式)
#影片图片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)          #re.S让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq = re.compile(r'<span class="inq">(.*?)</span>')
#影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

# 初始的网页
baseurl = "https://movie.douban.com/top250?start="

# 爬取网页
def getData(baseurl):
    datalist=[]
    # 这里的n_1是获取数据前多少页（每页25个电影）
    for i in range(0,n_1):  
        url = baseurl + str(i*25)
        html = askURL(url)  #保存获取到的网页源码

        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"):    
            data = []      #保存电影信息
            item = str(item)
            item = item.replace("\u00a0", "")       #去除数据库NBSP问题

            #影片详情链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定字符串
            data.append(link)  # 添加影片详情链接
            imgsrc = re.findall(findImgSrc, item)[0]
            data.append(imgsrc)  # 添加影片图片链接

            titles = re.findall(findTitle, item)
            if(len(titles)==2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")      #去掉无关字符
                data.append(otitle)
            else:
                data.append(titles[0])  # 添加影片片名
                data.append(' ')

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加影片评分

            judge = re.findall(findJudge, item)[0]
            data.append(judge)  # 添加影片评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)  # 添加影片概况
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)         #去掉<br/>
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())  # 添加影片相关内容,去掉空格
            print(data)
            datalist.append(data)
    print("爬取完毕,等待保存")
    return datalist
datalist = getData(baseurl)

def save_excel():
    # 1.爬取网页
    savepath = "豆瓣电影Top250.xls"
    # 3.保存数据
    saveData(datalist, savepath)




#保存数据
def saveData(datalist,savepath):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet('豆瓣电影Top250')
    col = ("排名","影片详情链接","影片图片链接","影片中文名","影片外文名","影片评分","影片评价人数","影片概况","影片相关内容","年份")
    # 先写第一行索引名
    for i in range(0,10):
        worksheet.write(0,i,col[i])     #列名
    for i in range(0,n_2):
        print("第%d条"%i)
        data = datalist[i]
        for j in range(0,9):
            if j==0:
                worksheet.write(i+1,j,i+1)
            else:
                worksheet.write(i+1,j,data[j-1])
                if j==8:
                    lin=reSearch(data[j-1])
                    worksheet.write(i+1,9,lin)
    workbook.save(savepath)

