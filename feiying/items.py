# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import time
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.item import Item, Field


class ItemProcessor:
    def _func_list(self):
        return []
    
    def process(self, pipe, spider):
        r = None
        for f in self._func_list():
            r = f(pipe, spider)
            if isinstance(r, Item):
                continue
            else:
                break
        return r

class FeiyingItem(Item, ItemProcessor):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    source = Field()
    source_id = Field()
    image_url = Field()
    category = Field()


class FyVideoItem(FeiyingItem):
    time = Field()
    size = Field()
    video_url = Field()

class FyMovieItem(FyVideoItem):
    director = Field()
    actor = Field()
    release_date = Field()
    origin = Field()
    description = Field()

class FySeriesItem(FeiyingItem):
    director = Field()
    actor = Field()
    release_date = Field()
    origin = Field()
    description = Field()
    episode_count = Field()
    episode_all = Field()

    def _func_list(self):
        return [self._save_db]

    def _save_db(self, pipe, spider):
        status = self._check_db(pipe, spider)
        if status == 0:
            self._insert(pipe, spider)
            return self
        elif status == 2:
            self._update(pipe, spider)
            return self
        else:
            return DropItem('This item is already in database.')

    def _check_db(self, pipe, spider):
        sql = "SELECT id, episode_count, episode_all FROM fy_tv_series WHERE source_id = ?"
        param = (self['source_id'][0],)
        r = None
        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)
            r = cursor.fetchone()

        if None == r:
            return 0 #this item is not found in db, just insert it into db.
        elif r[2] == 1:
            return 1 #this item is already in db and all episodes are crawled.
        elif self['episode_all'][0] != r[2] and self['episode_count'][0] == r[1]:
            return 2 #this item is already in db but it's status changed, need to be update.
        else:
            return 3 #this item is already in db but not all episodes are crawled.

    def _insert(self, pipe, spider):
        if self['episode_all'][0] == 0:
            self['episode_count'][0] = 0

        sql = """
            INSERT INTO fy_tv_series (title, image_url, category, source, source_id,
            created_time, director, actor, release_date, origin, description,
            episode_count, episode_all) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        param = (
            self['title'][0],
            self['image_url'][0],
            self['category'][0],
            self['source'][0],
            self['source_id'][0],
            str(time.time()),
            self['director'][0],
            self['actor'][0],
            self['release_date'][0],
            self['origin'][0],
            self['description'][0],
            self['episode_count'][0],
            self['episode_all'][0])

        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)


    def _update(self, pipe, spider):
        sql = "UPDATE fy_tv_series SET episode_all=? WHERE source_id=?"
        param = (self['episode_all'][0], self['source_id'][0])

        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)
               

class FyEpisodeItem(Item, ItemProcessor):
    source_id = Field()
    episode_index = Field()
    image_url = Field()
    video_url = Field()
    size = Field()
    time = Field()

    def _func_list(self):
        return [self._save_db]

    def _save_db(self, pipe, spider):
        r = self._check_db(pipe, spider)
        if r == 0:
            self._insert(pipe, spider)
            return self
        else:
            return DropItem('This item is already in database')

    def _check_db(self, pipe, spider):
        sql = "SELECT id FROM fy_tv_episode WHERE source_id=? AND episode_index=?"
        param = (self['source_id'][0], self['episode_index'][0])
        r = None
        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)
            r = cursor.fetchone()

        if r==None:
            return 0 # this episode is not in db
        else:
            return 1 # this episode is already in db

    def _insert(self, pipe, spider):
        sql = """
            INSERT INTO fy_tv_episode (time, size, source_id, episode_index, image_url,
            video_url) VALUES (?,?,?,?,?,?)"""
        param = (
            self['time'][0],
            self['size'][0],
            self['source_id'][0],
            self['episode_index'][0],
            self['image_url'][0],
            self['video_url'][0])

        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)


