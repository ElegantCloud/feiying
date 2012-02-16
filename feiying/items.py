# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class FeiyingItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    source = Field()
    source_id = Field()
    image_url = Field()
    category = Field()

class FyFormalVideoItem():
    director = Field()
    actor = Field()
    release_date = Field()
    origin = Field()
    description = Field()

class FyVideoItem(FeiyingItem):
    time = Field()
    size = Field()
    video_url = Field()

class FyMovieItem(FyVideoItem, FyFormalVideoItem):
    pass

class FySeriesItem(FeiyingItem, FyFormalVideoItem):
    episode_count = Field()
    episode_all = Field()

class FyEpisodeItem(Item):
    source_id = Field()
    episode_index = Field()
    image_url = Field()
    video_url = Field()
    size = Field()
    time = Field()

