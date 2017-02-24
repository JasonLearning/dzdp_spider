# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/16 上午11:39
# @Author   : Jason
# @File     : category_url_spider.py

from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import Task
from celery.exceptions import Reject, Retry
from celery.utils.log import get_task_logger

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSelectorException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tools.collections.shop_list_job_collection import ShopListJobCollectionClass

logger = get_task_logger(__name__)


class ShopListSpider(Task):
    name = 'dzdp.category_url_spider'

    def run(self, *args, **kwargs):
        self.run_inner(args, kwargs)

    def run_inner(self, args, kwargs):
        """
        [run的实现便于测试]
        :param args:
        :param kwargs:
        :return:
        """
        logger.info("[{m_name}]run function!".format(m_name=__name__, ))

        # logging
        logger.info("[args]%s" % (args,))
        logger.info("[kwargs]%s" % (kwargs,))

        # [查询job信息]
        job_id = kwargs['job_id']

        collection = ShopListJobCollectionClass()
        category_url = collection.get_url(job_id)

        driver = self.init_web_driver()
        try:
            driver.get(category_url)
            shop_url_list = self.parse(driver)
            collection.insert_shop_id_list(job_id, shop_url_list)
        except TimeoutException as e:
            print("can not wait xpath div find!")
            raise self.retry(args, kwargs, exc=e)

        finally:
            print("quit web driver！")
            driver.quit()

            print("[category_url_spider]sleep 5s")
            sleep(5)

    def init_web_driver(self):
        # [init chrome]
        # [close image]
        # opt = Options()
        # opt.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
        # driver = webdriver.Chrome(chrome_options=opt)

        # PhantomJS ssl https 代理配置参数
        service_args = [
            '--ssl-protocol=any',
            '--load-images=no'
        ]
        # 关闭cookies貌似没起效
        desired_capabilities = {
            "browserName": "android",
            "version": "",
            "platform": "ANDROID",
            "javascriptEnabled": True,
            'cookiesEnabled': False
        }
        print("[爬虫代理中间件]init web driver!!!!!!!!!!!!!")
        # driver = webdriver.PhantomJS(service_args=service_args, desired_capabilities=desired_capabilities,
        #                              service_log_path='/var/log/celery/category_spider.log')
        driver = webdriver.PhantomJS(executable_path="/Users/simon/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")

        return driver

    def parse(self, driver):
        # [分页url_list]
        shop_list = []
        num = 0
        t = True
        while t:
            try:
                elem = driver.find_elements_by_xpath("//*[@id='shop-all-list']/ul/li/div[2]/div[1]/a")
                for a in elem:
                    uurl = a.get_attribute('href')
                    if "shop" in uurl:
                        num += 1
                        shop_list.append(uurl)
                driver.find_element_by_xpath(".//*[@class='next']").click()
            except NoSuchElementException as N:
                t = False
        return shop_list

