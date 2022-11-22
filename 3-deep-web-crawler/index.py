# import request
from common import read_csv,get_html,json_parse,initial_csv,append_csv
import time

BASE_URL='https://xueqiu.com/service/screener/screen'

#读取筛选参数
def read_input(path):
  df=read_csv(path)
  params={}
  for i in range(len(df.index)):
    key=df['key'][i]
    max_num=df['max'][i]
    min_num=df['min'][i]
    if max_num>min_num:
      value=str(min_num)+'_'+str(max_num)
      params[key]=value
  return params

#拼接url
def concat_url(params,base_params={}):
  #序列化
  url=BASE_URL+'?'
  for key in base_params.keys():
    url+=key+'='+base_params[key]+'&'
  for key in params.keys():
    url+=key+'='+params[key]+'&'
 
  return url[:-1] #去除最后一个&

#获取响应数据
def handle_response_data(url):
  print('请求地址为：'+url+'\n')
  print('【请求中...请稍后】\n')
  res=get_html(url)
  if res!=False:
    print('已获取到数据，处理中...\n')
    data=json_parse(res)['data']
    list=data['list']
    return list
  return False


def save_data(path,rows):
  if rows!=False:
    #制作header
    header=[]
    for key in rows[0].keys():
      header.append(key)
    initial_csv(path,header)
    append_csv(rows,path,header)
    print('写入完毕!')


def main():
  input_csv_path='./input.csv'
  output_csv_path='./out_put.csv'
  #基础的参数，如分页信息、排序等
  base_params={
    'only_count':'0',
    'current':'',
    'page':'1',
    'size':'30',
    'exchange':'sh_sz',
    'category':'CN',
    'order_by':'symbol',
    'order':'desc',
    'indcode':'',
    'areacode':'',
    '_':str(int(time.time()*1000))
  }

  params=read_input(input_csv_path)
  entry_url=concat_url(params,base_params)
  rows=handle_response_data(entry_url)
  save_data(output_csv_path,rows)

main()
