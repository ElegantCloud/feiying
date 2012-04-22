# coding=utf8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import json
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
    source_id = Field()
    image_url = Field()
    channel = Field()

    def _check_attribute(self, pipe, spider):
        if len(self['image_url'][0])==0 or len(self['source_id'][0])==0 or len(self['title'][0])==0:
               return 'Invalid Attribute!'
        else:
            return self

    def _check_duplicated(self, pipe, spider):
        sql = "SELECT image_url, source_id FROM fy_video WHERE image_url = ?"
        param = (self['image_url'][0],)
        r = None
        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)
            r = cursor.fetchone()

        if None == r:
            return self
        else:
            return 'Find item with duplicated image_url'

class FyVideoItem(FeiyingItem):
    time = Field()
    size = Field()
    video_url = Field()

    def _func_list(self):
        return [self._check_attribute, 
                self._check_video_url, 
                self._check_words, 
                self._check_duplicated, 
                self._save_db, 
                self._gearman]

    def _check_video_url(self, pipe, spider):
	if len(self['video_url'][0]) == 0:
	    return 'Invalid Attribute: video_url'
        else:
	    return self

    def _check_words(self, pipe, spider):
        invalid_words = [u'文凭', u'身份证', u'发票', u'發票', u'办假', u'办理', u'koolmo', u'自慰', u'成人视频']
        for w in invalid_words:
            if self['title'][0].rfind(w)>=0:
                return 'Invalid word in title: %s' % w
        return self

    def _gearman(self, pipe, spider):
        data = {
                'source_id':self['source_id'][0],
                'title':self['title'][0],
                'video_url':self['video_url'][0],
                'image_url':self['image_url'][0],
                'time':self['time'][0],
                'size':self['size'][0],
                'channel':self['channel'][0]
            }
        job = pipe.gearman_client.submit_job('fy_video_download', json.dumps(data),
                background = True, wait_until_complete = False)
        pipe.gearman_client.wait_until_jobs_accepted([job])
        return self

    def _save_db(self, pipe, spider):
        fy_video_sql = """
            INSERT INTO fy_video (source_id, title, image_url, channel) VALUES (?,?,?,?)"""
        fy_video_param = (
            self['source_id'][0],
            self['title'][0],
            self['image_url'][0],
            self['channel'][0])

        fy_short_video_sql = """
            INSERT INTO fy_short_video (source_id, time, size, video_url) VALUES (?,?,?,?)"""
        fy_short_video_param = (
            self['source_id'][0],
            self['time'][0],
            self['size'][0],
            self['video_url'][0])

        with pipe.db_conn.cursor() as cursor:
            cursor.execute('SET AUTOCOMMIT=0')
            cursor.execute(fy_video_sql, fy_video_param)
            cursor.execute(fy_short_video_sql, fy_short_video_param)

        return self


class FyMovieItem(FyVideoItem):
    director = Field()
    actor = Field()
    release_date = Field()
    origin = Field()
    description = Field()

    def _func_list(self):
        return [self._check_attribute, self._check_video_url, self._check_yueyu, self._save_db]

    def _check_yueyu(self, pipe, spider):
        yueyu = u'粤语'
        if self['title'][0].rfind(yueyu)>=0:
            return 'Yueyu movie'
        else:
            return self

    def _save_db(self, pipe, spider):
        fy_video_sql = """
            INSERT INTO fy_video (source_id, title, image_url, channel) VALUES (?,?,?,?)"""
        fy_video_param = (
            self['source_id'][0],
            self['title'][0],
            self['image_url'][0],
            self['channel'][0])

        fy_movie_sql = """
            INSERT INTO fy_movie (source_id, time, size, video_url, director, 
            actor, release_date, origin, description) VALUES (?,?,?,?,?,?,?,?,?)"""
        fy_movie_param = (
            self['source_id'][0],
            self['time'][0],
            self['size'][0],
            self['video_url'][0],
            self['director'][0],
            self['actor'][0],
            self['release_date'][0],
            self['origin'][0],
            self['description'][0])

        with pipe.db_conn.cursor() as cursor:
            cursor.execute('SET AUTOCOMMIT=0')
            cursor.execute(fy_video_sql, fy_video_param)
            cursor.execute(fy_movie_sql, fy_movie_param)

        return self

class FySeriesItem(FeiyingItem):
    director = Field()
    actor = Field()
    release_date = Field()
    origin = Field()
    description = Field()
    episode_count = Field()
    episode_all = Field()
    episode_list = Field()

    def _func_list(self):
        return [self._check_attribute, self._check_words, self._save_db]

    def _check_words(self, pipe, spider):
        invalid_word_list = [u'乐视制造']
        if self['actor'][0] in invalid_word_list or self['director'][0] in invalid_word_list:
            return 'Invalid Word'
        else:
            return self

    def _save_db(self, pipe, spider):
        status = self._check_db(pipe, spider)
        if status == 0:
            self._insert(pipe, spider)
            return self
        elif status == 2:
            self._update(pipe, spider)
            return self
        elif status == 3:
            self._insert_new_episode(pipe, spider)
            return self
        else:
            return 'This item is already in database.'

    def _check_db(self, pipe, spider):
        sql = "SELECT episode_count, episode_all FROM fy_tv_series WHERE source_id = ?"
        param = (self['source_id'][0],)
        r = None
        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)
            r = cursor.fetchone()

        if None == r:
            return 0 #this item is not found in db, just insert it into db.
        elif r[1] == 1:
            return 1 #this item is already in db and all episodes are crawled.
        elif self['episode_all'][0] != r[1] and self['episode_count'][0] == r[0]:
            return 2 #this item is already in db but it's status changed, need to be update.
        else:
            return 3 #this item is already in db but not all episodes are crawled.

    def _insert(self, pipe, spider):
        fy_video_sql = """
            INSERT INTO fy_video (source_id, title, image_url, channel) VALUES (?,?,?,?)"""
        fy_video_param = (
            self['source_id'][0],
            self['title'][0],
            self['image_url'][0],
            self['channel'][0])

#        if self['episode_all'][0] == 0:
#            self['episode_count'][0] = 0
        fy_series_sql = """
            INSERT INTO fy_tv_series (source_id, director, actor, release_date, origin, description,
            episode_count, episode_all) VALUES (?,?,?,?,?,?,?,?)"""
        fy_series_param = (
            self['source_id'][0],
            self['director'][0],
            self['actor'][0],
            self['release_date'][0],
            self['origin'][0],
            self['description'][0],
            self['episode_count'][0],
            self['episode_all'][0])

        fy_episode_sql = """
            INSERT INTO fy_tv_episode (source_id, time, size, episode_index, image_url,
            video_url) VALUES (?,?,?,?,?,?)"""
        fy_episode_param = None
        for e in self['episode_list']:
            p = ((e['source_id'][0],
                 e['time'][0],
                 e['size'][0],
                 e['episode_index'][0],
                 e['image_url'][0],
                 e['video_url'][0]),)
            if fy_episode_param == None:
                fy_episode_param = p
            else:
                fy_episode_param += p   

        with pipe.db_conn.cursor() as cursor:
            cursor.execute('SET AUTOCOMMIT=0')
            cursor.execute(fy_video_sql, fy_video_param)
            cursor.execute(fy_series_sql, fy_series_param)
            if fy_episode_param != None:
                cursor.executemany(fy_episode_sql, fy_episode_param)

    def _update(self, pipe, spider):
        sql = "UPDATE fy_tv_series SET episode_all=? WHERE source_id=?"
        param = (self['episode_all'][0], self['source_id'][0])

        with pipe.db_conn.cursor() as cursor:
            cursor.execute(sql, param)
               
    def _insert_new_episode(self, pipe, spider):
        select_sql = """
            SELECT episode_index FROM fy_tv_episode WHERE source_id=?"""
        select_param = (self['source_id'][0],)
        r = None
        with pipe.db_conn.cursor() as cursor:
            cursor.execute(select_sql, select_param)
            r = cursor.fetchall()

        if r == None:
            return
        else:
            cl = map(lambda x : x[0], r)
            fy_episode_sql = """
                INSERT INTO fy_tv_episode (source_id, time, size, episode_index, image_url,
                video_url) VALUES (?,?,?,?,?,?)"""
            for e in self['episode_list']:
                i = e['episode_index'][0]
                if not i in cl:
                    fy_episode_param = (
                        e['source_id'][0],
                        e['time'][0],
                        e['size'][0],
                        e['episode_index'][0],
                        e['image_url'][0],
                        e['video_url'][0],)
                    with pipe.db_conn.cursor() as cursor:
                        cursor.execute(fy_episode_sql, fy_episode_param)


class FyEpisodeItem(Item, ItemProcessor):
    source_id = Field()
    episode_index = Field()
    image_url = Field()
    video_url = Field()
    size = Field()
    time = Field()

