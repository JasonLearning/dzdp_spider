# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/16 下午2:01
# @Author   : Jason
# @File     : shop_list_spider_driver.py

from __future__ import absolute_import, unicode_literals

from celery import group
from celery.contrib import rdb
from celery.utils.log import get_task_logger
from celery import chain

from mx_celery import app
from spider_tasks.dzdp.shop_list_spider import ShopListSpider
from tools.config.dzdp_shop_category_info import DzdpShopCategoryInfo
from tools.collections.shop_list_job_collection import ShopListJobCollectionClass
from drivers.dzdp.shop_details_spider_driver import ShopDetailsSpiderDriver
from drivers.dzdp.area_clean_driver import AreaCleanDriver

logger = get_task_logger(__name__)


class ShopListSpiderDriver:
    def __init__(self):
        pass

    @staticmethod
    @app.task(name='periodic_shop_list_spider_driver')
    def periodic_driver():
        ShopListSpiderDriver.periodic_driver_inner()

    @staticmethod
    def periodic_driver_inner():
        # [zara]
        area = DzdpShopCategoryInfo.area
        zara = DzdpShopCategoryInfo.brand
        zara_shop_list_task = group(ShopListSpiderDriver.driver.si(category_meta['name'], category_meta['url'])
                                    for category_meta in zara)
        print("ooo_driver fire!")
        zara_shop_list_task.apply_async()
        zara_area_task = group(AreaCleanDriver.driver.si(url_list['name'], url_list['url'])
                               for url_list in area)

        print("[periodic driver]fire!")
        zara_area_task.apply_async()

    @staticmethod
    @app.task(name='drivers.dzdp.shop_list_spider_driver.driver')
    def driver(brand, category_url):
        print("brand:%s,category_url:%s" % (brand, category_url))
        ShopListSpiderDriver.driver_inner(brand, category_url)

    @staticmethod
    def driver_inner(brand, category_url):
        """
        [目录url爬虫驱动]
        爬取商品分类分页url列表
        :return:
        """
        # [构建作业]
        c = ShopListJobCollectionClass()
        job_id = c.create_job(brand, category_url)

        # [目录url爬虫&&目录爬虫]
        task_chain = chain(
            ShopListSpider().s(job_id=job_id),
            ShopListSpiderDriver.category_crawl_task.si(job_id)
        )
        task_chain()

    @staticmethod
    @app.task(name='drivers.dzdp.shop_list_spider_driver.category_crawl_task')
    def category_crawl_task(job_id):
        """
        [目录商品爬取作业驱动]
        :return:
        """
        print("[category_crawl_task]create ")
        ShopListSpiderDriver.category_crawl_task_inner(job_id)

    @staticmethod
    def category_crawl_task_inner(job_id):
        """
        [更具目录分页url爬虫结果切分目录爬虫task]
        :param job_id:
        :return:
        """
        # [获取job info]
        c = ShopListJobCollectionClass()
        shop_url_list = c.get_shop_url_list(job_id)
        # [构建并行目录爬虫task]
        task_group = group(ShopDetailsSpiderDriver.driver.s(shop_rul, job_id)
                           for shop_rul in shop_url_list)
        task_group.apply_async()


if __name__ == '__main__':
    pass
