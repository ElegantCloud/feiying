# coding=utf8
# letv_movie.py

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader.processor import MapCompose
from feiying.items import FyMovieItem

class LetvMovieSpider(CrawlSpider):
    name = 'letv_movie'
    allowed_domains = ['m.letv.com']

    rules = (
        Rule(
                SgmlLinkExtractor(restrict_xpaths='//div[@class="iphone"]/div[@class="ph"]/div[@class="detail"]/dl[@class="dl02"]/dd'),
                'parse_item'
            ),
        )

    def start_requests(self):
        base_url = "http://m.letv.com/video/v_list.php?cid=4&page="
        for p in range(1,2):
            url = base_url + str(p)
            yield Request(url)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        videos = hxs.select('//div[@class="vo1"]')
        for v in videos:
            l = XPathItemLoader(FyMovieItem(), v)
            l.add_xpath('title', 'div[@class="vd"]/text()[2]', MapCompose(unicode.strip),
                    re='](.+)')
            l.add_xpath('time', 'dl[@class="vd1"]/dt[5]/text()', re='...(.+)')
            l.add_xpath('image_url', 'dl[@class="vd1"]/dd/img/@src')
            l.add_xpath('video_url',
                    'div[@class="vd2"]/div[@class="play_row_btn"][3]/span/a/@href')
            l.add_xpath('director', 'dl[@class="vd1"]/dt[1]/text()', re='...(.+)')
            l.add_xpath('actor', 'dl[@class="vd1"]/dt[2]/text()', re='...(.+)')
            l.add_xpath('origin', 'dl[@class="vd1"]/dt[4]/text()', re='...(.+)')
            l.add_xpath('release_date', 'dl[@class="vd1"]/dt[6]/text()', re='...(.+)')
            l.add_xpath('description', 'dl[@class="vd4"][2]/dd/text()', MapCompose(unicode.strip,
                lambda x : x[0:512] if x else '')
            l.add_value('size', 0)
            l.add_value('source_id', response.url, MapCompose(lambda x:self.name+'_'+x),
                    re='id=(.+)&')
            l.add_value('channel', 1)
            yield l.load_item()

