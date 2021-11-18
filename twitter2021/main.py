import pymongo
from scrapy import cmdline
# cmdline.execute("scrapy crawl MytwitterSpider -a query=\"covid I test positive lang:en\"".split())

cmdline.execute("scrapy crawl MytwitterSpider".split())

#scrapy crawl MytwitterSpider -a query="covid I test positive lang:en"

# connection = pymongo.MongoClient("127.0.0.1", 27017)
# db = connection["TweetScraper"]
# collection = db["meta"]
# res = collection.find().sort('_id', -1).limit(1)
# # query = {'_id': res[0]['_id']}
# new_value = {"$set": {"used": "true"}}
# collection.update_one(res[0], new_value)
