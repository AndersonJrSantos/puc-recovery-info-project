# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os

class TrendsPipeline:
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item

    def open_spider(self, spider):
        self.file = open('trends_br_coletados.json', 'w')
        self.file.write('[')
    
    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()
