# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/20 下午5:26
# @Author   : Jason
# @File     : area_clean_driver.py

from __future__ import absolute_import, unicode_literals

from celery import group
from celery.contrib import rdb
from celery.utils.log import get_task_logger
from celery import chain

from mx_celery import app
from spider_tasks.dzdp.area_spider import AreaSpider
from tools.collections.area_collection import AreaCollectionClass


logger = get_task_logger(__name__)


class AreaCleanDriver:
    def __init__(self):
        pass

    @staticmethod
    @app.task(name='drivers.dzdp.area_clean.driver')
    def driver(name, url):
        print("[drivers.dzdp.area_clean.driver] begin!!!!")
        c = AreaCollectionClass()
        job_id = c.create_job(name, url)
        crawl_chain = chain(
            AreaSpider().s(job_id, job_id=job_id),
        )
        crawl_chain()

