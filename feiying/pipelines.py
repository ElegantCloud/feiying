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
            host = 'mysql-server',
            user = 'feiying',
            passwd = 'feiying123',
            db = 'feiying'
            )

        self.gearman_client = gearman.GearmanClient(['gearman-server-1', 'gearman-server-2'])

    def process_item(self, item, spider):
        try:
            r = item.process(self, spider)
            if not isinstance(r, Item):
                raise DropItem(r)
        except oursql.Error as e:
            raise DropItem(e)
        else:
            return r

