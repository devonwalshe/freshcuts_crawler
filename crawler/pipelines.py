# -*- coding: utf-8 -*-
import logging


class OmniProductPipeline(object):
    def process_item(self, item, spider):
        logging.info("Made it to the pipeline")
        return item
