import urllib3
from bs4 import BeautifulSoup 


def get_html(url):
  http = urllib3.PoolManager()
  header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
  }
  r = http.request('GET', url,None, header)
  if r.status==200:
    return r.data.decode('utf-8')
  return False

def getBS(url):
  html=get_html(url)
  print(url)
  if html != False:
    print(html)
    bs = BeautifulSoup(html,"html.parser")
    return bs
  