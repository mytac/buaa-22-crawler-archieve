import pandas as pd
from bs4 import BeautifulSoup
import common

class urlreader:
  "csv"
  request_list=[]
  def __init__(self,csv_url,base_path):
      self.url=csv_url
      self.base=base_path
  #拿文章链接
  def get_requests(self):
    df=pd.read_csv(self.url)
    list=df['url']
    for (i,obj) in enumerate(list):
      url=self.base+obj
      self.request_list.append(url)
    print(self.request)
  #读取文章链接下的内容
  def read_url(self):
    bs=common.getBS(self.request_list[0])
    url=bs.select('.v_news_content')[0]