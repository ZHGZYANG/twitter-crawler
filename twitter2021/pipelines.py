# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os, logging, json
from scrapy.utils.project import get_project_settings
import pymongo
from twitter2021.items import Tweet, Metadata, User
from twitter2021.utils import mkdirs

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)
SETTINGS = get_project_settings()


class SaveToMongoPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(SETTINGS['MONGODB_SERVER'], SETTINGS['MONGODB_PORT'])
        db = connection[SETTINGS['MONGODB_DB']]
        self.tweetCollection = db[SETTINGS['MONGODB_TWEET_COLLECTION']]
        self.metaCollection = db[SETTINGS['MONGODB_META_COLLECTION']]
        self.userCollection = db[SETTINGS['MONGODB_USER_COLLECTION']]
        self.tweetCollection.ensure_index([('ID', pymongo.ASCENDING)], unique=True, dropDups=True)
        self.userCollection.ensure_index([('ID', pymongo.ASCENDING)], unique=True, dropDups=True)
        self.metaCollection.ensure_index([('ID', pymongo.ASCENDING)], unique=True, dropDups=True)

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            dbItem = self.tweetCollection.find_one({'ID': item['ID']})
            if dbItem:
                pass  # simply skip existing items
                ### or you can update the tweet, if you don't want to skip:
                # dbItem.update(dict(item))
                # self.tweetCollection.save(dbItem)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                self.tweetCollection.insert_one(dict(item))
                logger.debug("Add tweet:%s" % item['ID'])

        # elif isinstance(item, User):
        #     dbItem = self.userCollection.find_one({'ID': item['ID']})
        #     if dbItem:
        #         pass # simply skip existing items
        #         ### or you can update the user, if you don't want to skip:
        #         # dbItem.update(dict(item))
        #         # self.userCollection.save(dbItem)
        #         # logger.info("Update user:%s"%dbItem['screen_name'])
        #     else:
        #         self.userCollection.insert_one(dict(item))
        #         logger.debug("Add user:%s" %item['screen_name'])
        elif isinstance(item, Metadata):
            dbItem = self.metaCollection.find_one({'ID': item['ID']})
            if dbItem:
                pass
            else:
                self.metaCollection.insert_one(dict(item))
                logger.debug("Add metadata with newest ID:%s" % item['ID'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))
