# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.item import Item
import gearman
import oursql

class FeiyingPipeline(object):

    def __init__(self):
        self.db_conn = oursql.connect(
            host = '192.168.1.233',
            user = 'futuom',
            passwd = 'ivyinfo123',
            db = 'feiying'
            )

        self.gearman_client = gearman.GearmanClient(['192.168.1.233:4730'])

    def process_item(self, item, spider):
        r = item.process(self, spider)
        if isinstance(r, Item):
            return r
        elif isinstance(r, DropItem):
            raise r
        else:
            raise DropItem('Unknown error')

