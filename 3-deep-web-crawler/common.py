import urllib3
from bs4 import BeautifulSoup 
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

def getBS(url):
  html=get_html(url)
  if html != False:
    bs = BeautifulSoup(html,"html.parser")
    return bs



def get_stoplist():
  path='./stoplist.txt'
  stoplist=[]
  f=open(path,encoding='utf-8')
  words=f.read()
  word_list=str.split(words)
  f.close()
  return word_list

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