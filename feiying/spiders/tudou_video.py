# coding=utf8
# tudou_video.py

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader.processor import MapCompose
from feiying.items import FyVideoItem

class TudouVideoSpider(CrawlSpider):
    name = 'tudou_video'
    allowed_domains = ['m.tudou.com']

    source = 'tudou'
    category_map = {
        '29':'zixun',
        '14':'yinyue',
        '1':'yule',
        '15':'tiyu',
        '26':'shishang',
        '5':'gaoxiao',
        '31':'zongyi'
        }

    rules = (
            Rule(
                SgmlLinkExtractor(allow=('(http://m\.tudou\.com/view\.do\?)(.)+')),
                'parse_item',
            ),
        )

    def start_requests(self):
        base_url = "http://m.tudou.com/category.do?v=3&cp=&method=channelindex&pageId=1&channelId="
        for cid in self.category_map.keys():
            url = base_url + cid
            yield Request(url)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        videos = hxs.select('//div[@class="viewTitle"]')
        for v in videos:
            l = XPathItemLoader(FyVideoItem(), v)
            l.add_xpath('title', 'div[@class="listtitle"]/div[@class="listtitle_inn"]/font/text()',
                    MapCompose(unicode.strip))
            l.add_xpath('time', 'div[5]/span/text()', re='\d{0,2}:?\d(2):\d{2}')
            l.add_xpath('image_url', 'div[@class="box1"]/div[@class="expdiv"]/a/img/@src')
            l.add_xpath('video_url', 'div[7]/span/a/@href', MapCompose(lambda
            x:'http://m.tudou.com/'+x))
            l.add_xpath('size', 'div[7]/span/a/span/text()', re='(?:\d*\.*\d*)(?:KB|MB)')
            l.add_xpath('source_id', 'div[7]/span/a/@href', MapCompose(lambda x:self.source+'_'+x),
                    re='code=(\d+)&')
            l.add_value('source', self.source)
            l.add_value('category', response.url, MapCompose(lambda x : self.category_map[x]),
                    re='channelId=(\d+)')
            yield l.load_item()

