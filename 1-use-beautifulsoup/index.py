import urllib3
import json
from bs4 import BeautifulSoup 


def getHtml(url):
  http = urllib3.PoolManager()
  header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }
  r = http.request('GET', url,None, header)
  if r.status==200:
    return r.data.decode('utf-8')
  return False

def getContent(html):
  bs = BeautifulSoup(html,"html.parser") # 缩进格式
  list=[]
 #子标签通过 > 定义
  content = bs.select('.col_l .lf_comment_lists > li')  #一个数组，每个子项是p节点，之后提取里面的文本就ok啦
  for (i,obj) in enumerate(content):
    node=obj.select('a')[0]
    url=node.get('href')
    rank=node.select('em')[0].text
    title=node.select('p')[0].text
    # obj.select
    # url=obj.href
    # child=bs.select(obj)
    # print(node)
    list.append({'rank':rank,'title':title,'url':url})
  return list

def toJSON(kv,path):
  with open(path,"w",encoding='utf-8') as write_f:
    json_str = json.dumps(kv,ensure_ascii=False,indent=4,)
    write_f.write(json_str)
  print("写入json文件到:",path)
  return;


def main():
  url='https://tech.163.com/game/'
  path='./data.json'
  html=getHtml(url)
  content=getContent(html)
  json=toJSON(content,path)

main()
