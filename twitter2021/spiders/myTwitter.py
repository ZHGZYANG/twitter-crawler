import re, json, logging
import time
import datetime
from dateutil import parser as dateparser
from dateutil import relativedelta
import pymongo
import sys
from urllib.parse import quote
import scrapy
from scrapy.exceptions import DontCloseSpider, CloseSpider
from scrapy import http
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.spiders import CrawlSpider
from scrapy.shell import inspect_response
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from twitter2021.items import Tweet, User, Metadata

# *File mode does not support until_id

# CONFIG
ENABLE_TIME = True
ENABLE_NEXT_TOKEN = True
ENABLE_SAVE_TO_FILE = False  # *File mode is deprecated
ENABLE_SINCE_ID = False
# By default, a request will return Tweets from up to seven days ago if you do not include this parameter.
REQUEST_START_TIME = '2020-12-01T00:00:00.000Z'
# By default, a request will return Tweets from as recent as 30 seconds ago if you do not include this parameter.
REQUEST_END_TIME = '2021-11-15T00:00:00.000Z'
HEADER = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAALuqVgEAAAAA0o%2FmLGghMjtceO31FjcYcx1ZlF8%3DPblTZo9qr31SCBdbZ5cXJtHwiHnUSIqBIARB3RwQupgRqYjuvX'
}

SETTINGS = get_project_settings()
logger = logging.getLogger(__name__)
base_url = (
    f'https://api.twitter.com/2/tweets/search/all?'
    f'tweet.fields=author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld'
    # f'&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type'
    # f'&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
    f'&max_results=500'
    f'&query='
)
next_token_pre = '&next_token='
until_id_pre = '&until_id='
start_time_pre = '&start_time='
end_time_pre = '&end_time='
current_token = ''
count = 0


def get_tomorrow(current_time):
    tomorrow = dateparser.parse(current_time) + relativedelta.relativedelta(days=1)
    return tomorrow.strftime('%Y-%m-%dT%H:%M:%S.000Z')


class MytwitterSpider(CrawlSpider):
    name = 'MytwitterSpider'
    allowed_domains = ['twitter.com']
    handle_httpstatus_list = [400, 404, 401, 429]

    def __init__(self, query='covid positive -is:retweet'):
        self.query = query.replace(' ', '%20').replace(':', '%3A')
        self.pure_start_time = REQUEST_START_TIME
        self.pure_end_time = get_tomorrow(REQUEST_START_TIME)
        self.start_time = ''
        self.end_time = ''
        self.url = ''
        self.next_token = ''

    def get_next_token_db(self):
        global count
        count += 1
        try:
            connection = pymongo.MongoClient(SETTINGS['MONGODB_SERVER'], SETTINGS['MONGODB_PORT'])
            db = connection[SETTINGS['MONGODB_DB']]
            collection = db[SETTINGS['MONGODB_META_COLLECTION']]
            res = collection.find().sort('_id', -1).limit(1)
            if res[0]['used'] == bool(True):  # this token has been requested
                if ENABLE_SINCE_ID:
                    self.logger.info('================TOKEN USED================')
                    self.logger.info(res[0]['next_token'])
                    self.logger.info('Current request count: ' + str(count))
                    return until_id_pre + res[0]['newest_id']
                else:
                    return ''
            else:
                token = res[0]['next_token']
                new_value = {"$set": {"used": True}}
                collection.update_one(res[0], new_value)
                self.logger.info('================TOKEN=====================')
                self.logger.info(token)
                self.logger.info('Current request count: ' + str(count))
                if token == '':
                    if ENABLE_SINCE_ID:
                        return until_id_pre + res[0]['newest_id']
                    else:
                        return ''
                return next_token_pre + token
        except:
            self.logger.info('==============GET TOKEN ERROR=============')
            self.logger.info('Current request count: ' + str(count))
            return ''

    def get_next_token(self):
        global count, current_token
        count += 1
        if current_token == '':
            self.logger.info('===========TOKEN USED OR NULL=============')
            self.logger.info('Current request count: ' + str(count))
            return ''
        else:
            self.logger.info('================TOKEN=====================')
            self.logger.info(current_token)
            self.logger.info('Current request count: ' + str(count))
            tmp = current_token
            current_token = ''
            return next_token_pre + tmp

    def set_url(self):
        self.url = base_url + self.query
        if ENABLE_TIME:
            self.start_time = start_time_pre + self.pure_start_time.replace(':', '%3A')
            self.end_time = end_time_pre + self.pure_end_time.replace(':', '%3A')
            self.url += self.start_time + self.end_time
            self.pure_start_time = self.pure_end_time
            self.pure_end_time = get_tomorrow(self.pure_end_time)
        if ENABLE_SAVE_TO_FILE:
            if ENABLE_NEXT_TOKEN:
                self.next_token = self.get_next_token()
                self.url += self.next_token
        else:
            if ENABLE_NEXT_TOKEN:
                self.next_token = self.get_next_token_db()
                self.url += self.next_token
        return self.url

    def start_requests(self):
        # self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        for r in self.start_query_request():
            yield r

    def start_query_request(self, cursor=None):
        if ENABLE_SAVE_TO_FILE:
            yield http.Request(self.set_url(), callback=self.parse_result_page_file, headers=HEADER, dont_filter=True)
        else:
            yield http.Request(self.set_url(), callback=self.parse_result_page_db, headers=HEADER, dont_filter=True)

    def parse_result_page_file(self, response):
        if response.status == 200:
            global current_token
            res = response.json()
            path = SETTINGS['SAVE_PATH'] + res['meta']['oldest_id'] + '.csv'
            with open(path, 'w', encoding='utf8') as file:
                file.write(str(res))
            with open('next_token.txt', 'w') as token_file:
                try:
                    current_token = res['meta']['next_token']
                    token_file.write(res['meta']['next_token'])
                except:
                    token_file.write('')
                    current_token = ''
            # time.sleep(5)
        elif response.status == 400:
            self.logger.info('===========ERROR 400=============')
            self.logger.info(response.text)
            time.sleep(60)
        elif response.status == 401:
            self.logger.info('===========ERROR 401=============')
            self.logger.info(response.text)
            time.sleep(60)
        elif response.status == 429:
            self.logger.info('===========ERROR 429=============')
            self.logger.info(response.text)
            raise CloseSpider('ERROR 429')
        else:
            self.logger.info('===========UNKNOWN ERROR=============')
            self.logger.info('ERROR CODE: ' + response.status)
            self.logger.info(response.text)
            time.sleep(60)
        if self.pure_start_time != REQUEST_END_TIME:
            yield http.Request(self.set_url(), callback=self.parse_result_page_file, headers=HEADER, dont_filter=True)

    def parse_result_page_db(self, response):
        # try:
        if response.status == 200:
            global current_token
            meta_res = response.json()['meta']
            if meta_res['result_count'] != 0:
                meta = Metadata()
                try:
                    meta['used'] = False
                    meta['ID'] = meta_res['oldest_id']
                    meta['oldest_id'] = meta_res['oldest_id']
                    meta['newest_id'] = meta_res['newest_id']
                    current_token = meta_res['next_token']
                    meta['next_token'] = meta_res['next_token']
                except:
                    meta['newest_id'] = ''
                    meta['next_token'] = ''
                    current_token = ''
                yield meta

                for item in self.parse_tweet_item(response.json()['data']):
                    yield item
        elif response.status == 400:
            self.logger.info('===========ERROR 400=============')
            self.logger.info(response.text)
        elif response.status == 401:
            self.logger.info('===========ERROR 401=============')
            self.logger.info(response.text)
        elif response.status == 429:
            self.logger.info('===========ERROR 429=============')
            self.logger.info(response.text)
            raise CloseSpider('ERROR 429')
        else:
            self.logger.info('===========UNKNOWN ERROR=============')
            self.logger.info('ERROR CODE: ' + response.status)
            self.logger.info(response.text)
            time.sleep(60)
        # except:
        #     time.sleep(600)
        if self.pure_start_time != REQUEST_END_TIME:
            time.sleep(5)
            yield http.Request(self.set_url(), callback=self.parse_result_page_db, headers=HEADER, dont_filter=True)

    def parse_tweet_item(self, items):
        for item in items:
            tweet = Tweet()
            tweet['ID'] = item['id']
            tweet['url'] = "https://twitter.com/" + item["author_id"] + "/status/" + item['id']
            tweet['created_at'] = item['created_at']
            tweet['text'] = item['text']
            tweet['lang'] = item['lang']
            tweet['author_id'] = item['author_id']
            tweet['retweet_count'] = item['public_metrics']['retweet_count']
            tweet['like_count'] = item['public_metrics']['like_count']
            tweet['reply_count'] = item['public_metrics']['reply_count']
            tweet['quote_count']=item['public_metrics']['quote_count']
            tweet['source']=item['source']
            tweet['possibly_sensitive']=item['possibly_sensitive']
            tweet['conversation_id']=item['conversation_id']
            if 'geo' in item:
                tweet['geo']=item['geo']
            else:
                tweet['geo'] = 'N/A'
            if (item['text'][0:4] == 'RT @'):
                tweet['is_retweet'] = True
            else:
                tweet['is_retweet'] = False
            tweet['is_reply'] = False
            yield tweet

    # def spider_idle(self, spider):
    #     time.sleep(3)
    #     for r in self.start_requests():
    #         yield r
    #     self.logger.info('Spider idled. Continue to next request...')
    #     raise DontCloseSpider
