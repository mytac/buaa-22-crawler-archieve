## 主题相关度计算

### 1. 先正确爬取链接

我爬的是[北航新闻网](http://news.buaa.edu.cn/zhxw.htm)，可以看到上面 tab 有多个分区，观察后发现，这些 tab 下的媒体类型分为两种：文章和视频，但点开发现都是多媒体文章，所以我们获得的数据的字段为

```
type: 综合信息|专题新闻 ...
url: 链接
title: 文章标题
create_time: 发布时间
```

#### 翻页

观察翻页时发现，每往后翻一页 url 会变化为 baseurl+页码 OVO，如：

```
http://news.buaa.edu.cn/zhxw/1108.htm
http://news.buaa.edu.cn/zhxw/1107.htm
```

这样获取到总页码之后倒着爬就 ok 啦！
最终把 url 链接存入到 csv 链接中就 ok 了

### 2. 分词分析

#### 主题词

自定义主题词

```
topicwords={'校长','王云鹏'}
```

#### 停用词

从网上搜的[中文停用词](https://www.cnblogs.com/mfmdaoyou/p/6848772.html)，存入为 txt 文件，使用时转成数组放到内存中。

#### 分词

jieba 分词分不出来人名，所以要导入用户自定义的词库

```
jieba.load_userdict('./jieba_user_load.txt')
jieba.cut(p,cut_all=False) # 精确模式
```

分后的词，存进`docwords`

### 3. 计算相关度

先算 docwords 和 topicwords 的交集，记为 commwords ，然后拿该交集除以并集减去交集的差，最终计算结果即为计算相关度。

```
相关度=(交集)/(并集-交集)
sim=len(commwords)/(len(self.topicwords)+len(docwords)-len(commwords))
```
