# coding=utf8
# letv_series.py

from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader.processor import MapCompose, Compose
import urlparse
import oursql
from feiying.items import FySeriesItem, FyEpisodeItem

class LetvSeriesSpider(CrawlSpider):
    name = 'letv_series'
    allowed_domains = ['m.letv.com']

    episode_list_url = 'http://m.letv.com/ajax/getPlist.php?act=plist&id='

    rules = (
        Rule(
                SgmlLinkExtractor(restrict_xpaths='//div[@class="iphone"]/div[@class="ph"]/div[@class="detail"]/dl[@class="dl02"]/dd'),
                'parse_series_item'
            ),
        )

    def start_requests(self):
#        yield Request('http://m.letv.com/play.php?type=2&id=71937',
#                callback=self.parse_series_item)
#        return

        base_url = "http://m.letv.com/video/v_list.php?cid=5&page="
        for p in range(1,2):
            url = base_url + str(p)
            yield Request(url)

        ul = self._get_update_series()
        for sid in ul:
            yield Request('http://m.letv.com/play.php?type=2&id='+sid,
                    callback=self.parse_series_item)

    def _get_update_series(self):
        sql = "SELECT source_id FROM fy_tv_series WHERE episode_all=0"
        db = oursql.connect(
            host = 'mysql-server',
            user = 'feiying',
            passwd = 'feiying123',
            db = 'feiying'
            )
        rl = []
        with db.cursor() as cursor:
            cursor.execute(sql)
            ls = cursor.fetchall()
            for s in ls:
                rl.append(s[0].strip('letv_series'))
        return rl

    def parse_series_item(self, response):
        hxs = HtmlXPathSelector(response)
        videos = hxs.select('//div[@class="vo1"]')
        for v in videos:
            l = XPathItemLoader(FySeriesItem(), v)
            series_id = self._get_series_id(response.url)
            text = v.select('dl[@class="vd1"]/dt[5]/text()').extract()
            episode_all = self._get_episode_all(text[0])
            l.add_xpath('title', 'div[@class="vd"]/text()[2]', MapCompose(unicode.strip),
                    re='](.+)')
            l.add_xpath('image_url', 'dl[@class="vd1"]/dd/img/@src')
            l.add_xpath('director', 'dl[@class="vd1"]/dt[1]/text()', self._get_default,
                    re='...(.+)')
            l.add_xpath('actor', 'dl[@class="vd1"]/dt[2]/text()', self._get_default, re='...(.+)')
            l.add_xpath('origin', 'dl[@class="vd1"]/dt[4]/text()', self._get_default, re='...(.+)')
            l.add_xpath('episode_count', 'dl[@class="vd1"]/dt[5]/text()', self._get_default,
                    re='\d+')
            l.add_xpath('release_date', 'dl[@class="vd1"]/dt[6]/text()', self._get_default,
                    re='...(.+)')
            l.add_xpath('description', 'dl[@class="vd4"][2]/dd/text()', MapCompose(unicode.strip,
                    self._get_default))
            l.add_value('source_id', self.name+'_'+series_id)
            l.add_value('episode_all', episode_all)
            l.add_value('channel', 2)
            series = l.load_item()
            request = Request(self.episode_list_url + series_id, callback=self.parse_episode_list)
            request.meta['series'] = series
            yield request

    def parse_episode_list(self, response):
        series = response.meta['series']
        series['episode_list'] = []
        hxs = HtmlXPathSelector(response)
        episodes = hxs.select('//div[@class="detail"]')
        i = 0
        for e in episodes:
            i += 1
            l = XPathItemLoader(FyEpisodeItem(), e)
            series_id = self._get_series_id(response.url)
            l.add_value('source_id', self.name+'_'+series_id)
            l.add_value('episode_index', i)
            l.add_xpath('image_url', 'dl[@class="dl01"]/dt/a/img/@src')
            l.add_xpath('video_url', 'dl[@class="dl01"]/dt/a/@href')
            l.add_xpath('time', 'dl[@class="dl01"]/dd/p/span/text()', re='...(\d+)')
            l.add_value('size', 0)
            item = l.load_item()
            series['episode_list'].append(item)
        yield series

    def _get_series_id(self, url):
        p =urlparse.urlparse(url)
        qs = urlparse.parse_qs(p.query)
        return qs['id'][0]

    def _get_episode_all(self, text):
        update_str = u'更新'
        if text.find(update_str) > -1:
            return 0
        return 1

    def _get_default(self, value):
        if isinstance(value, str):
            return value[0:512].strip()
        if isinstance(value, unicode):
            return value[0:512].strip()

        return value if value else 0
