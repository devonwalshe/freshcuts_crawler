# -*- coding: utf-8 -*-
import logging, traceback
from orm.orm import db_connect, create_tables, Base
from orm.models import *
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

class OmniProductPipeline(object):
    '''
    Pipeline for processing affiliate product data
    '''
    def __init__(self):
        '''
        Initialize db connection and session
        '''
        engine = db_connect()
        create_tables(engine, Base)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.close()
        logging.info("Closing Spider now")
        #print(spider.crawler.stats.get_stats())
        ### TODO send rails app signal to update image from scraped url
        ### TODO sort out logging somehow
    
    def item_unchanged(self, item):
        '''
        Starts a new session, gets or creates db item
        Checks to see if any of its attributes are missing or different
        if they are, returns True, False otherwise
        Also returns False if there isn't a URL
        '''
        session = self.Session()
        if item['url'] == '':
            session.close()
            raise DropItem("This item doesn't have a url and can't be consistency checked")
        # Retrieve or create db item
        db_item = get_or_create(session, AffiliateProduct, affiliate_product_url=item['url'] )
        # Consistency check
        discount = round(float(item['discount']),2) if item['discount'] else None
        price = round(float(item['price']),2) if item['price'] else None
        weight = round(float(item['price']),2) if item['weight'] else None
        if (    db_item.affiliate_product_title == item['title']
            and db_item.affiliate_product_id == item['product_id']
            and round(db_item.price,2) == price
            and round(db_item.discount,2) if db_item.discount else None == discount
            and round(db_item.weight, 2) if db_item.weight else None == weight 
            ):
            return(True)
        else:
            return(False)


    def process_item(self, item, spider):
        logging.info("Made it to the pipeline")
        session = self.Session()
        # presense & consistency validations
        itemfield_presence =[ itemfield in ['', None] for itemfield in [item['title'], item['url'], item['price']]]
        if True in itemfield_presence:
            session.close()
            raise DropItem("Item doesn't have either a title, url or price and can't be processed")
        if self.item_unchanged(item):
            session.close()
            raise DropItem("Nothing has changed with this item")
        # Parse and save item
        affiliate = get_or_create(session, Affiliate, reference=spider.affiliate_reference)
        ap = get_or_create(session, AffiliateProduct, affiliate_product_url=item['url'])
        ap.affiliate_product_title = item['title']
        ap.affiliate_product_description = item['description']
        ap.affiliate_product_url = item['url']
        ap.affiliate_product_image_url = item['image_url']
        ap.affiliate_product_id = item['product_id']
        ap.crawled_at = item['crawled_at']
        ap.in_stock = item['in_stock']
        ap.weight = float(item['weight']) if item['weight'] else None
        ap.price = float(item['price']) 
        ap.discount = float(item['discount']) if item['discount'] else None
        ap.affiliate = affiliate
        
        try:
            session.add(ap)
            session.commit()
            logging.info("Item saved in the database")
        except Exception as e: #FIXME catch actual exceptions
            logging.error(traceback.format_exc())
            session.rollback()
        finally:
            session.close()
        return(item)
