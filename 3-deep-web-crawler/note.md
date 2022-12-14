# Deep Web 采集

## 什么是 Deep Web？

1. 页面上的数据是存储于数据库、数据文件等地方，而非直接记录在 HTML 页面文件中
2. 为用户提供一定的查询接口，返回符合条件的记录，并生成 HTML 页面。

### Deep Web 和普通 Web 页面有什么差距？

deep web 和普通 web 最大的区别就是没有直接的超链接指向固定的页面，且不会被搜索引擎收录。

基于我的理解，就是有个表单（不论是不是通过 form 标签显现的），需要你自己输入参数调接口拿数据的动态页面都是 deep web，搜索引擎没有收录的页面。

## 爬虫选股

所要爬的是这页：[雪球选股 - https://xueqiu.com/hq/screener/](https://xueqiu.com/hq/screener/)

[![z12YIP.png](https://s1.ax1x.com/2022/11/22/z12YIP.png)](https://imgse.com/i/z12YIP)

观察条件设置模块中是没有`<form>`标签的，是通过勾选指标和输入数值，再点击“开始选股”按钮完成查询操作的。

看 html 中，每个 label 下的 input 中，都有个 value 属性。value 属性中存入的值即为请求的 key。

[![z1hiJx.png](https://s1.ax1x.com/2022/11/22/z1hiJx.png)](https://imgse.com/i/z1hiJx)

输入市盈率 10-20 ，点击“开始选股”，之后可看到筛选结果

[![z1hWkR.png](https://s1.ax1x.com/2022/11/22/z1hWkR.png)](https://imgse.com/i/z1hWkR)

### 总体流程

1. 读取 input.csv，输出为一个字典

```py
#读取筛选参数
def read_input(path):
  df=read_csv(path)
  params={}
  for i in range(len(df.index)):
    key=df['key'][i]
    max_num=df['max'][i]
    min_num=df['min'][i]
    if max_num>min_num:
      value=str(min_num)+'_'+str(max_num)
      params[key]=value
  return params
```

2. 拼接发送请求的 url

```py
#拼接url
def concat_url(params,base_params={}):
  #序列化
  url=BASE_URL+'?'
  for key in base_params.keys():
    url+=key+'='+base_params[key]+'&'
  for key in params.keys():
    url+=key+'='+params[key]+'&'

  return url[:-1] #去除最后一个&
```

输出为：`https://xueqiu.com/service/screener/screen?only_count=0&current=&page=1&size=30&exchange=sh_sz&category=CN&order_by=symbol&order=desc&indcode=&areacode=&_=1669115186746&pettm=10_20`

3. 请求，拿到数据，如下：

```py

def get_html(url):
  http = urllib3.PoolManager()
  header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) `App`leWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  }
  r = http.request('GET', url,None, header)
  if r.status==200:
    return r.data.decode('utf-8')
  return False

#获取响应数据
def handle_response_data(url):
  print('请求地址为：'+url+'\n')
  print('【请求中...请稍后】\n')
  res=get_html(url)
  if res!=False:
    print('已获取到数据，处理中...\n')
    data=json_parse(res)['data']
    list=data['list']
    return list
  return False
```

> {"data":{"count":664,"list":[{"pct":-2.1,"symbol":"SZ301365","pettm":19.598,"current":33.99,"name":"N 矩阵","exchange":"sh_sz","type":11,"areacode":"440000","tick_size":0.01,"has_follow":false,"indcode":null},{"pct":-1.61,"symbol":"SZ301356","pettm":12.056,"current":52.09,"name":"天振股份","exchange":"sh_sz","type":11,"areacode":"330000","tick_size":0.01,"has_follow":false,"indcode":"S3603"},{"pct":0,"symbol":"SZ301276","pettm":14.531,"current":24.96,"name":"嘉曼服饰","exchange":"sh_sz","type":11,"areacode":"110000","tick_size":0.01,"has_follow":false,"indcode":"S3502"},{"pct":-0.61,"symbol":"SZ301223","pettm":19.173,"current":21.16,"name":"中荣股份","exchange":"sh_sz","type":11,"areacode":"440000","tick_size":0.01,"has_follow":false,"indcode":"S3602"},{"pct":-2.73,"symbol":"SZ301177","pettm":16.959,"current":45.95,"name":"迪阿股份","exchange":"sh_sz","type":11,"areacode":"440000","tick_size":0.01,"has_follow":false,"indcode":"S3503"},{"pct":0.81,"symbol":"SZ301150","pettm":18.756,"current":74.95,"name":"中一科技","exchange":"sh_sz","type":11,"areacode":"420000","tick_size":0.01,"has_follow":false,"indcode":"S6307"},{"pct":1.58,"symbol":"SZ301118","pettm":13.854,"current":30.31,"name":"恒光股份","exchange":"sh_sz","type":11,"areacode":"430000","tick_size":0.01,"has_follow":false,"indcode":"S2202"},{"pct":0.9,"symbol":"SZ301109","pettm":13.872,"current":15.7,"name":"军信股份","exchange":"sh_sz","type":11,"areacode":"430000","tick_size":0.01,"has_follow":false,"indcode":"S7601"},{"pct":-2.13,"symbol":"SZ301108","pettm":17.792,"current":35.89,"name":"洁雅股份","exchange":"sh_sz","type":11,"areacode":"340000","tick_size":0.01,"has_follow":false,"indcode":"S7701"},{"pct":2.27,"symbol":"SZ301090","pettm":19.518,"current":10.82,"name":"华润材料","exchange":"sh_sz","type":11,"areacode":"320000","tick_size":0.01,"has_follow":false,"indcode":"S2205"},{"pct":-0.63,"symbol":"SZ301061","pettm":12.081,"current":30.1,"name":"匠心家居","exchange":"sh_sz","type":11,"areacode":"320000","tick_size":0.01,"has_follow":false,"indcode":"S3603"},{"pct":-7.14,"symbol":"SZ301060","pettm":16.693,"current":26.29,"name":"兰卫医学","exchange":"sh_sz","type":11,"areacode":"310000","tick_size":0.01,"has_follow":false,"indcode":"S3706"},{"pct":-2.14,"symbol":"SZ301035","pettm":14.462,"current":86.4,"name":"润丰股份","exchange":"sh_sz","type":11,"areacode":"370000","tick_size":0.01,"has_follow":false,"indcode":"S2208"},{"pct":-1.81,"symbol":"SZ301006","pettm":17.494,"current":16.83,"name":"迈拓股份","exchange":"sh_sz","type":11,"areacode":"320000","tick_size":0.01,"has_follow":false,"indcode":"S6401"},{"pct":-3.42,"symbol":"SZ301004","pettm":18.133,"current":33.06,"name":"嘉益股份","exchange":"sh_sz","type":11,"areacode":"330000","tick_size":0.01,"has_follow":false,"indcode":"S3603"},{"pct":1.44,"symbol":"SZ301003","pettm":18.391,"current":24.69,"name":"江苏博云","exchange":"sh_sz","type":11,"areacode":"320000","tick_size":0.01,"has_follow":false,"indcode":"S2205"},{"pct":2.01,"symbol":"SZ300994","pettm":19.576,"current":21.35,"name":"久祺股份","exchange":"sh_sz","type":11,"areacode":"330000","tick_size":0.01,"has_follow":false,"indcode":"S2804"},{"pct":-1.81,"symbol":"SZ300979","pettm":17.714,"current":48.82,"name":"华利集团","exchange":"sh_sz","type":11,"areacode":"440000","tick_size":0.01,"has_follow":false,"indcode":"S3501"},{"pct":-4.45,"symbol":"SZ300911","pettm":19.718,"current":39.25,"name":"亿田智能","exchange":"sh_sz","type":11,"areacode":"330000","tick_size":0.01,"has_follow":false,"indcode":"S3304"},{"pct":-0.42,"symbol":"SZ300873","pettm":15.336,"current":28.18,"name":"海晨股份","exchange":"sh_sz","type":11,"areacode":"320000","tick_size":0.01,"has_follow":false,"indcode":"S4208"},{"pct":3.97,"symbol":"SZ300852","pettm":18.785,"current":37.18,"name":"四会富仕","exchange":"sh_sz","type":11,"areacode":"440000","tick_size":0.01,"has_follow":false,"indcode":"S2702"},{"pct":-4.73,"symbol":"SZ300841","pettm":17.989,"current":97.45,"name":"康华生物","exchange":"sh_sz","type":11,"areacode":"510000","tick_size":0.01,"has_follow":false,"indcode":"S3703"},{"pct":-0.45,"symbol":"SZ300821","pettm":16.787,"current":13.32,"name":"东岳硅材","exchange":"sh_sz","type":11,"areacode":"370000","tick_size":0.01,"has_follow":false,"indcode":"S2203"},{"pct":-1.13,"symbol":"SZ300815","pettm":12.828,"current":16.63,"name":"玉禾田","exchange":"sh_sz","type":11,"areacode":"340000","tick_size":0.01,"has_follow":false,"indcode":"S7601"},{"pct":-0.59,"symbol":"SZ300801","pettm":10.502,"current":23.56,"name":"泰和科技","exchange":"sh_sz","type":11,"areacode":"370000","tick_size":0.01,"has_follow":false,"indcode":"S2203"},{"pct":-1.29,"symbol":"SZ300787","pettm":12.218,"current":30.57,"name":"海能实业","exchange":"sh_sz","type":11,"areacode":"360000","tick_size":0.01,"has_follow":false,"indcode":"S2705"},{"pct":-0.36,"symbol":"SZ300780","pettm":18.334,"current":16.42,"name":"德恩精工","exchange":"sh_sz","type":11,"areacode":"510000","tick_size":0.01,"has_follow":false,"indcode":"S6401"},{"pct":-1.67,"symbol":"SZ300773","pettm":18.36,"current":14.71,"name":"拉卡拉","exchange":"sh_sz","type":11,"areacode":"110000","tick_size":0.01,"has_follow":false,"indcode":"S4903"},{"pct":-2.04,"symbol":"SZ300772","pettm":18.664,"current":15.81,"name":"运达股份","exchange":"sh_sz","type":11,"areacode":"330000","tick_size":0.01,"has_follow":false,"indcode":"S6306"},{"pct":-1.01,"symbol":"SZ300771","pettm":11.717,"current":12.75,"name":"智莱科技","exchange":"sh_sz","type":11,"areacode":"440000","tick_size":0.01,"has_follow":false,"indcode":"S7101"}]},"error_code":0,"error_description":""}

4. 对 JSON 数据进行处理，存入本地 csv

```py
def save_data(path,rows):
  if rows!=False:
    #制作header
    header=[]
    for key in rows[0].keys():
      header.append(key)
    initial_csv(path,header)
    append_csv(rows,path,header)
    print('写入完毕!')
```

#### 最终输出

[![z1vwSe.png](https://s1.ax1x.com/2022/11/22/z1vwSe.png)](https://imgse.com/i/z1vwSe)

## 总体代码

### index.py

```py
# import request
from common import read_csv,get_html,json_parse,initial_csv,append_csv
import time

BASE_URL='https://xueqiu.com/service/screener/screen'

#读取筛选参数
def read_input(path):
  df=read_csv(path)
  params={}
  for i in range(len(df.index)):
    key=df['key'][i]
    max_num=df['max'][i]
    min_num=df['min'][i]
    if max_num>min_num:
      value=str(min_num)+'_'+str(max_num)
      params[key]=value
  return params

#拼接url
def concat_url(params,base_params={}):
  #序列化
  url=BASE_URL+'?'
  for key in base_params.keys():
    url+=key+'='+base_params[key]+'&'
  for key in params.keys():
    url+=key+'='+params[key]+'&'

  return url[:-1] #去除最后一个&

#获取响应数据
def handle_response_data(url):
  print('请求地址为：'+url+'\n')
  print('【请求中...请稍后】\n')
  res=get_html(url)
  if res!=False:
    print('已获取到数据，处理中...\n')
    data=json_parse(res)['data']
    list=data['list']
    return list
  return False


def save_data(path,rows):
  if rows!=False:
    #制作header
    header=[]
    for key in rows[0].keys():
      header.append(key)
    initial_csv(path,header)
    append_csv(rows,path,header)
    print('写入完毕!')


def main():
  input_csv_path='./input.csv'
  output_csv_path='./output.csv'
  #基础的参数，如分页信息、排序等
  base_params={
    'only_count':'0',
    'current':'',
    'page':'1',
    'size':'30',
    'exchange':'sh_sz',
    'category':'CN',
    'order_by':'symbol',
    'order':'desc',
    'indcode':'',
    'areacode':'',
    '_':str(int(time.time()*1000))
  }

  params=read_input(input_csv_path)
  entry_url=concat_url(params,base_params)
  rows=handle_response_data(entry_url)
  save_data(output_csv_path,rows)

main()
```

common.py

```py
import urllib3
import pandas as pd
import csv
import json


def get_html(url):
  http = urllib3.PoolManager()
  header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) `App`leWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  }
  r = http.request('GET', url,None, header)
  if r.status==200:
    return r.data.decode('utf-8')
  return False

# 字符串转json
def json_parse(str):
  return json.loads(str)


def initial_csv(csv_path,header):
  with open(csv_path, 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    f.close()

def append_csv(rows,csv_path,header):
   with open(csv_path, 'a+', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f,fieldnames=header)
    writer.writerows(rows)
    f.close()

def read_csv(path):
 df=pd.read_csv(path)
 return df
```
