# coding=utf8
# youku_video.py

from scrapy.http import Request
from scrapy.spider import BaseSpider 
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.spiders import CrawlSpider, Rule
from feiying.items import FyVideoItem

class YoukuVideoSpider(CrawlSpider):
    name = 'youku_video'
    allowd_domains = ['3g.youku.com']

    source = 'youku'
    channel_map = {
        '91':3, #news
        '95':5, #music
        '86':8, #entertainment
        '98':6, #sports
        '89':7, #fashion
        '94':4 #fun
        }

    rules = ( 
        Rule(
                SgmlLinkExtractor(restrict_xpaths='//div[@class="video"]'),
                'parse_item',
            ),
        )

    def start_requests(self):
        base_url = "http://3g.youku.com/wap2/channeldetail.jsp?ob=1&pg=1&cid="
        for cid in self.channel_map.keys():
            url = base_url + cid
            yield Request(url)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        videos = hxs.select('//div[@class="videodetail"]')
        for v in videos:
            l = XPathItemLoader(FyVideoItem(), v)
            l.add_xpath('title', 'div[@class="videotitle"]/text()', MapCompose(unicode.strip))
            l.add_xpath('time', 'div[@class="videotext"]/text()[1]', re='\d{0,2}:?\d{1,2}:\d{1,2}')
            l.add_xpath('image_url', 'div[@class="videoimg"]/img/@src')
            l.add_xpath('video_url', 'div[@class="playlink"][1]/a[2]/@href', MapCompose(lambda x :
                'http://3g.youku.com' + x))
            l.add_xpath('size', 'div[@class="playlink"][1]/text()[last()]',
                re='(?:[\d,\.]+)(?:M|K)')
            l.add_xpath('source_id', 'div[@class="playlink"][1]/a[2]/@href', MapCompose(lambda x:
                self.source + '_' +x), re='id=(.+)&')
            l.add_value('channel', response.url, MapCompose(lambda x : self.channel_map[x]),
                re='cid=(\d{2})')
            yield l.load_item()

