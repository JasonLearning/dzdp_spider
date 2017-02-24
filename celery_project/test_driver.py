# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/21 上午11:14
# @Author   : Jason
# @File     : test_driver.py

from drivers.dzdp.shop_list_spider_driver import ShopListSpiderDriver

if __name__ == '__main__':
    print("test")
    task = ShopListSpiderDriver.periodic_driver.s()
    task.apply_async()
