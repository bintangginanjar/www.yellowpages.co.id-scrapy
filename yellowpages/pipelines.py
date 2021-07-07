# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import re

from itemadapter import ItemAdapter

class DataCleanPipeline(object):
    def __init__(self):		
        logging.info("****Data cleaning****")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        def getCleanPhone(text):
            text = text.replace('\n', '').replace('\t', '').replace(' ', '')

            return text

        def getCleanEmail(text):
            text = text.replace('mailto:', '')

            return text

        def getCleanUrl(text):
            text = text.replace('?utm_campaign=yellowpagesutm_source=yellowpages&utm_medium=sponsored-listing', '')

            return text

        item['noTelp'] = getCleanPhone(item['noTelp'][0])
        
        if adapter.get('email'):
            item['email'] = getCleanEmail(item['email'][0])

        if adapter.get('site'):
            item['site'] = getCleanUrl(item['site'][0])

        return item