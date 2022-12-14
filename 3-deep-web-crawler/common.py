import urllib3
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