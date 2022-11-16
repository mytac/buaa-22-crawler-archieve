import pandas as pd
from bs4 import BeautifulSoup
from common import getBS,initial_csv,append_csv
import jieba
from gensim.corpora.dictionary import Dictionary

jieba.load_userdict('./jieba_user_load.txt')
# default_mode = jieba.lcut(file, cut_all=False) # 精确模式

csv_output='./output.csv'
header=['sim','url']
class urlreader:
  "csv"
  request_list=[]
  def __init__(self,csv_url,base_path,stoplist=[],topicwords={}):
      self.url=csv_url
      self.base=base_path
      self.stoplist=stoplist
      self.topicwords=topicwords
  #拿文章链接
  def get_requests(self):
    df=pd.read_csv(self.url)
    list=df['url']
    for (i,obj) in enumerate(list):
      url=self.base+obj
      self.request_list.append(url)
  #计算单个文章的相关度
  def calculate_single_url(self,url):
    try :
        bs=getBS(url)
        ps=bs.select('.v_news_content>p')
        doc=[]
        for p in ps:
          p=p.text.strip('\n')
          if p!= '':
            d=[]
            for w in list(jieba.cut(p,cut_all=False)):
              if len(w)>1 and w not in self.stoplist:
                d.append(w)
            doc.append(d)
        dictionary=Dictionary(doc)
        dictionary.filter_extremes(no_below=0.1,no_above=1,keep_n=20)
        d=dict(dictionary.items())
        docwords=set(d.values())
        # 相关度计算： topicwords 和 docwords 集合的相似度
        commwords=self.topicwords.intersection(docwords)
        sim=len(commwords)/(len(self.topicwords)+len(docwords)-len(commwords))
        return [sim,url]
    except Exception as e :
        return [0,url]
   

  # 批量计算文章复杂度
  def batch_calculate(self):
    relation=0.01
    for (i,url) in enumerate(self.request_list):
      [sim,url]=self.calculate_single_url(url)
      if sim>0.01:
        #写入到csv中
        obj={'sim':sim,'url':url}
        append_csv([obj],csv_output,header)
    print('相关度>'+str(relation)+'的数据已存入:'+csv_output)
  def run(self):
    initial_csv(csv_output,header)
    self.get_requests()
    # self.calculate_single_url('http://news.buaa.edu.cn/info/1002/56903.htm')
    self.batch_calculate()
