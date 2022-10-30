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
  
  return ''


def main():
  url='https://tech.163.com/game/'
  html=getHtml(url)
  content=getContent(html)
  print(content)

main()
