import urllib3
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
 #子标签通过 > 定义
  content = bs.select('.col_l .lf_comment_lists > li p ')  #一个数组，每个子项是p节点，之后提取里面的文本就ok啦
  contentstr=''
  for i in range(len(content)):
    contentstr += content[i].text+'\n'
  return contentstr


def main():
  url='https://tech.163.com/game/'
  html=getHtml(url)
  content=getContent(html)
  print(content)

main()
