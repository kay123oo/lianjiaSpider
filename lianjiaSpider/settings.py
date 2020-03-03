# -*- coding: utf-8 -*-

# Scrapy settings for lianjiaSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjiaSpider'

SPIDER_MODULES = ['lianjiaSpider.spiders']
NEWSPIDER_MODULE = 'lianjiaSpider.spiders'

DOWNLOAD_TIMEOUT = 10

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lianjiaSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default) 禁用cookie
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lianjiaSpider.middlewares.LianjiaspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'lianjiaSpider.middlewares.LianjiaspiderDownloaderMiddleware': 543,
    'scrapy_redis.pipelines.RedisPipeline': 400 , # 分布式爬虫指定管道
   'lianjiaSpider.RetryMiddleware.Process_Proxies' :300,
    'lianjiaSpider.Proxy_Middleware.ProxyMiddleware':100 ,
    'lianjiaSpider.rotate_useragent_downloadmiddleware.RotateUserAgentMiddleware':200  #模拟不同浏览器行为
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 指定redisPipeline用以在redis中保存item
ITEM_PIPELINES = {
    #'scrapy_redis.pipelines.RedisPipeline': 200,
    'lianjiaSpider.pipelines.LianjiaspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling DOWNLOAD_DELAY stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

""" scrapy-redis配置"""
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
SCHEDULER_PERSIST = True

# 只在使用SpiderQueue或者SpiderStack是有效的参数,，指定爬虫关闭的最大空闲时间
#SCHEDULER_IDLE_BEFORE_CLOSE = 10

# 指定redis数据库的连接参数
#REDIS_HOST = '127.0.0.1'
#REDIS_PORT = 6379
#REDIS_DB = 1
REDIS_URL = 'redis://127.0.0.1:6379/1'

DEFAULT_REQUEST_HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

""" 连接MongoDB参数设置"""
MONGODB_HOST = '127.0.0.1' # 默认主机IP
MONGODB_PORT = 27017       # 默认端口号
MONGODB_DBNAME = 'lianjia' # 数据库名
MONGODB_DOCNAME = 'Test4'   # 表名


""" 重试请求次数 """
RETRY_ENABLED = True
RETRY_TIMES = 20