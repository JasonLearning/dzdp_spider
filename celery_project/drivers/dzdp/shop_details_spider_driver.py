# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 上午10:01
# @Author   : Jason
# @File     : shop_details_spider_driver.py

from __future__ import absolute_import, unicode_literals

from celery import group
from celery.contrib import rdb
from celery.utils.log import get_task_logger
from celery import chain

from mx_celery import app
from spider_tasks.dzdp.shop_details_spider import ShopDetailsSpider
from tools.collections.shop_details_job_collection import ShopDetailsJobCollectionClass
from drivers.dzdp.data_clean_driver import DataCleanDriver

logger = get_task_logger(__name__)


class ShopDetailsSpiderDriver:
    def __init__(self):
        pass

    @staticmethod
    @app.task(name='drivers.dzdp.shop_details_spider.driver')
    def driver(category_url, parent_job_id):
        print("[drivers.tmall.category_spider.zara]begin!!!!")
        c = ShopDetailsJobCollectionClass()
        job_id = c.create_job(category_url, parent_job_id)
        crawl_chain = chain(
            ShopDetailsSpider().s(job_id, job_id=job_id),  # 目录爬虫
            DataCleanDriver.driver.si(job_id),
        )
        crawl_chain()
