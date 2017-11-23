# scrap-redis使用手册

## settings.py 设置
```
# -*- coding: utf-8 -*-

# Scrapy settings for Qiji_Project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
```
### 项目名称
```
BOT_NAME = 'Qiji_Project'

SPIDER_MODULES = ['Qiji_Project.spiders']
NEWSPIDER_MODULE = 'Qiji_Project.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Qiji_Project (+http://www.yourdomain.com)'

# Obey robots.txt rules 不遵守爬虫协议

ROBOTSTXT_OBEY = False
```
### 并发设置默认16 Configure maximum concurrent requests performed by Scrapy (default: 16)
```
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
```
#### 下载间隔时间设置 See also autothrottle settings and docs
```
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
```
## 禁止使用cookies Disable cookies (enabled by default)
```
#COOKIES_ENABLED = False

#  Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
```
## 设置Headers Override the default request headers:
```
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
    'Cookie':'DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DLdxs2ekDgnCDsXgB0L72LBmMD9fW8WUkcdJyRaPe6RC%26wd%3D%26eqid%3Da72873e90004762d000000035a13887d; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; DJ_UVID=MTUxMTIyOTU2OTQ4OTM0MDM3; dj_cap=90c35250b8beb11cdba19576492562a3; DJ_DNS_PREFETECH=1; dj_nav=1; SO_COOKIE_V2=b968jCm+qrn4+bo0NdCEz90eQTn7Mwun9aZSG9n5PYsQjajj8JWALS+tQta6BHZGUIwFB6ksg6ibYt02UR52GnkFFVxy68xV1amn; dj_auth_v3=MTHt7vw9VBtjWkTqjz0ArD2qgRvAZUQs1qqAhcAzIYh45mL9ndGqCwKt4vRTMr8*; dj_auth_v4=81b5b77c2d3b7b84c586542655fde9a5_pc; uchome_loginuser=38870823; _check_isqd=no; USER_ACTION=request^AProfessional^AAUTO^A-^A-',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
```
## spider中间件
```
#SPIDER_MIDDLEWARES = {
#    'Qiji_Project.middlewares.QijiProjectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
```
## 下载中间件
```
DOWNLOADER_MIDDLEWARES = {
   # 'Qiji_Project.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    #User-Agent
    'Qiji_Project.mymiddlewares.RandomUserAgent':1,
    #免费代理的使用
    # 'Qiji_Project.mymiddlewares.FreeRandomProxy': 2,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
```
## 管道文件
```
ITEM_PIPELINES = {
   # 'Qiji_Project.pipelines.QijiProjectPipeline': 300,
   #  'scrapy_redis.pipelines.RedisPipeline':999,
    # 配置redis管道文件，权重数字相对最大
    'scrapy_redis.pipelines.RedisPipeline': 999, # redis管道文件，自动把数据加载到redis
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
```

## 分布式爬取
### 下载超时 下载的时间超过3s就丢弃
```
# DOWNLOAD_TIMEOUT = 3
```
## url 指纹 过滤器,使用scrapy-redis的去重组件,不使用scapy的默认去重.
```
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
```
## 使用scrapy-redis调度器
```
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
```
## 允许暂停redis请求记录不丢失 设置爬虫是否可以中断
```
SCHEDULER_PERSIST = True
```
## 默认的scrapy-redis请求 (按优先级顺序)队列形式
```
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue" 
```
## 队列形式 先进的先出
```
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"  # 按照队列模式
```
## 栈形式,请求先进后出
```
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack" # 按照栈进行请求的调度
```
## redis 连接配置 主机
```
REDIS_HOST = '106.14.159.206'
```
## 端口
```
REDIS_PORT = 6000
```

## 免费代理的使用(没有从数据库中获取)
```
# PROXIES = [
#     {'host' : '114.227.97.50:9000'},
#     {'host' : '115.148.27.10:9000'},
#     {'host': '117.139.45.248:8123'},
#     {'host': '117.90.0.155:9000'},
#     {'host': '120.27.10.38:8090'},
#     {'host': '121.232.147.38:9000'},
#     {'host': '121.232.148.150:9000'},
#     {'host': '223.151.209.189:9000'},

# ]
```
## 付费代理的使用
```
# AUTH_PROXIES = [
#     {'host' : '120.78.166.84:6666', 'auth' : 'alice:123456'}
# ]
```
