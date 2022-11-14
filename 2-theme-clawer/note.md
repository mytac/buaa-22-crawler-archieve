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

### 2. 进入到链接中获取内容

### 3. 计算相关度
