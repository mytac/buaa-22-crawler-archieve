import urllib3
from bs4 import BeautifulSoup 

class common:
  "common use"
  def __init__(self) -> None:
      pass
  def get_html(self,url):
    http = urllib3.PoolManager()
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }
    r = http.request('GET', url,None, header)
    if r.status==200:
      return r.data.decode('utf-8')
    return False
  def getBS(self,url):
    html=self.get_html(url)
    bs = BeautifulSoup(html,"html.parser")
    return bs