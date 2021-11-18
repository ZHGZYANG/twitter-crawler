# Scrapy settings for twitter2021 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'twitter2021'

LOG_LEVEL = 'DEBUG'
import datetime
# LOG_FILE = 'log/scrapy_{}_{}_{}.log'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

SPIDER_MODULES = ['twitter2021.spiders']
NEWSPIDER_MODULE = 'twitter2021.spiders'

TELNETCONSOLE_PORT = None

SAVE_PATH = 'Data/'

# settings for mongodb
MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "TweetScraper"  # database name to save the crawled data
# MONGODB_TWEET_COLLECTION = "tweet"  # collection name to save tweets
# MONGODB_USER_COLLECTION = "user"  # collection name to save users
# MONGODB_META_COLLECTION = 'meta'
MONGODB_TWEET_COLLECTION = "tweetday"  # collection name to save tweets
MONGODB_USER_COLLECTION = "userday"  # collection name to save users
MONGODB_META_COLLECTION = 'metaday'
# settings for mysql
# MYSQL_SERVER = "127.0.0.1"
# MYSQL_DB     = "TweetScraper"
# MYSQL_TABLE  = "scraper" # the table will be created automatically
# MYSQL_USER   = ""        # MySQL user to use (should have INSERT access granted to the Database/Table
# MYSQL_PWD    = ""        # MySQL user's password


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'twitter2021 (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'twitter2021.middlewares.Twitter2021SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'twitter2021.middlewares.Twitter2021DownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'twitter2021.pipelines.SaveToFilePipeline': 300,
    'twitter2021.pipelines.SaveToMongoPipeline': 100,  # replace `SaveToFilePipeline` with this to use MongoDB
    # 'twitter2021.pipelines.SavetoMySQLPipeline':100, # replace `SaveToFilePipeline` with this to use MySQL

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
