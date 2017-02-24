# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/16 上午11:29
# @Author   : Jason
# @File     : mx_celery.py

from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.contrib import rdb
from celery.schedules import crontab

from spider_tasks.dzdp.shop_list_spider import ShopListSpider
from spider_tasks.dzdp.shop_details_spider import ShopDetailsSpider

import celeryconfig

"""
分布式作业队列系统：
主要使用定时任务特性来投递作业给爬虫
使用方法:在celery_proj父级目录下执行
[worker]
celery -A celery_proj.mx_celery:app worker
[flower-monitor]
flower -A celery_proj.mx_celery --port=55555
[beat]
celery -A celery_proj.mx_celery:app beat --loglevel=info --logfile=
"""

app_name = str("spider")
app = Celery(app_name, include=[
    'drivers.dzdp.shop_details_spider_driver',
    'drivers.dzdp.shop_list_spider_driver',
    'drivers.dzdp.area_clean_driver',
    'drivers.dzdp.data_clean_driver'
])

# [注册]class task
app.register_task(ShopListSpider())
app.register_task(ShopDetailsSpider())

# config = {
#     "timezone ": 'Asia/Shanghai',
#     "enable_utc": True,
#     "broker_url": 'redis://localhost:6379/0',
#     "result_backend": 'redis://localhost:6379/0',
# }
# app.config_from_object(config)

app.config_from_object(celeryconfig)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
    # 关键字搜索页爬虫驱动
    # from celery_proj.periodic_tasks.key_word_search_spider_task import Driver
    # sender.add_periodic_task(10.0, Driver.task_create_sub_job.s(), name='task_create_sub_job every 10s')

    # 爬虫详情页爬虫驱动
    # from celery_proj.periodic_tasks.good_detail_spider_task import Driver
    # sender.add_periodic_task(10.0, Driver.driver.s(), name='good_detail_spider_task every 10s')

    # test for fan
    # from celery_proj.periodic_tasks.key_word_search_spider_task import add
    # sender.add_periodic_task(1, add.s(), name="add task periodic")

    # 同步sku任务驱动
    # from celery_proj.periodic_tasks.sync_sku_task import SyncSkuDriver
    # sender.add_periodic_task(
    #     # crontab(hour=23, minute=30),
    #     # crontab(minute='*/1'),
    #     # 10.0,
    #     # SyncSkuDriver.dummy.s(),
    #     # name='sync_sku_driver_task'
    # )

    # [tmall]zara爬取任务
    # from celery_proj.drivers.tmall.category_spider_driver import Driver
    # sender.add_periodic_task(
    #     # crontab(minute=0, hour=4),
    #     crontab(minute='*/1'),
    #     Driver.periodic_driver.s(),
    #     name='category tmall spider every day 4:00'
    # )

# if __name__ == '__main__':
#     app.start()
