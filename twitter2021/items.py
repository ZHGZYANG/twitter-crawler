from scrapy import Item, Field


class Tweet(Item):
    ID = Field()       # tweet id DONE
    url = Field()      # tweet url done
    created_at = Field() # post time DONE
    text = Field()     # text content DONE
    author_id = Field()  # user id DONE
    # usernameTweet = Field() # username of tweet MAY BE NO NEED

    retweet_count = Field()  # nbr of retweet
    like_count = Field() # nbr of favorite
    reply_count = Field()    # nbr of reply
    quote_count = Field()

    lang = Field()
    source= Field()
    possibly_sensitive=Field()
    conversation_id=Field()

    geo=Field()

    is_reply = Field()   # boolean if the tweet is a reply or not
    is_retweet = Field() # boolean if the tweet is just a retweet of another tweet

class User(Item):
    ID = Field()            # user id
    name = Field()          # user name
    screen_name = Field()   # user screen name
    avatar = Field()        # avator url

class Metadata(Item):
    ID=Field()
    newest_id=Field()
    oldest_id=Field()
    next_token=Field()
    used=Field() # marked flase at start, if the token has been used, mark to ture