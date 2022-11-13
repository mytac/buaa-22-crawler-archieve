import urllib3
import csv
import json
from bs4 import BeautifulSoup 


topics=['王云鹏','校长'] # 定义主题
csv_path='./url.csv'
header = ['title', 'url', 'create_time', 'type']

def initial_csv():
  with open(csv_path, 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    f.close()

def append_csv(rows):
   with open(csv_path, 'a+', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f,fieldnames=header)
    writer.writerows(rows)
    f.close()

def get_html(url):
  http = urllib3.PoolManager()
  header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }
  r = http.request('GET', url,None, header)
  if r.status==200:
    return r.data.decode('utf-8')
  return False

# 先爬单个tab
def spide_single_tab(url):
  html=get_html(url)
  bs = BeautifulSoup(html,"html.parser")
  rows=dom_parser(bs,'综合信息')
  append_csv(rows)
  print('already saved!')


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
  initial_csv()
  spide_single_tab(url)

main()