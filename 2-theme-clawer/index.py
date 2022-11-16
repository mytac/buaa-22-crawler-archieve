import urllib3
import csv
import json
from bs4 import BeautifulSoup 
import pandas as pd
from Urlreader import urlreader
from common import getBS,get_stoplist,initial_csv,append_csv

# 历任校长
topicwords={'校长','王云鹏'} # 定义主题
crawl_base_path='http://news.buaa.edu.cn/zhxw'
csv_path='./url.csv'
header = ['title', 'url', 'create_time', 'type']




# 先爬单个tab
def spide_single_tab(url):
  bs=getBS(url)
  rows=dom_parser(bs,'综合信息')
  # print('rows',rows)
  append_csv(rows,csv_path,header)

def spide_all_page():
  bs=getBS(crawl_base_path+'.htm')
  # 获取总页码
  pagination=bs.select('#fanye50834')[0].text
  [ignore,total]=pagination.split('/')
  total=int(total)
  # 倒着爬，插入到csv中
  for i in range(1,total-1):
    # 爬前100页
    if i<10:
      page_num=total-i
      url=crawl_base_path+'/'+str(page_num)+'.htm'
      spide_single_tab(url)
  print('链接已写入到csv中：',total,'条')


# 解析dom，拿到需要的信息
def dom_parser(bs,type):
  list=[]
  nodes = bs.select('.listleftop1>h2')
  for (i,obj) in enumerate(nodes):
    node=obj.select('a')[0]
    url=node.get('href')
    title=node.text
    date=obj.select('em')[0].text[1:-1]
    list.append({'create_time':date,'title':title,'url':url,'type':type})
  return list


def main():
  url='http://news.buaa.edu.cn/zhxw.htm'
  stoplist=get_stoplist()
  initial_csv(csv_path,header)
  # spide_single_tab(url)
  spide_all_page()
  reader=urlreader(csv_path,'http://news.buaa.edu.cn/',stoplist,topicwords)
  reader.run()
  print('all done!')

main()