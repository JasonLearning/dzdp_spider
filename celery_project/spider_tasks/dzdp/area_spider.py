# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/20 上午10:00
# @Author   : Jason
# @File     : area_spider.py

from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import Task
from celery.utils.log import get_task_logger

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSelectorException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tools.collections.area_collection import AreaCollectionClass
from tools.collections.documents.area_collection_documents import Area

logger = get_task_logger(__name__)


class AreaSpider(Task):
    name = 'dzdp.area_spider'

    def run(self, *args, **kwargs):
        self.run_inner(args, kwargs)

    def run_inner(self, args, kwargs):
    # def run_inner(self, job_id):
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

        collection = AreaCollectionClass()
        area_url = collection.get_url(job_id)

        driver = self.init_web_driver()
        try:
            driver.get(area_url)
            business_area = self.area_spider(driver)
            collection.insert_areas(job_id, business_area)
        except TimeoutException as e:
            print("can not wait xpath div find!")
            # raise self.retry(args, kwargs, exc=e)

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

    def details_spider(self, item):
        item = item.text.replace('|', '')
        item = item.split()
        return item[0], item[1:]

    def area_spider(self, driver):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list"))
            )
        except TimeoutException:
            print("time out")
            driver.quit()
            return

        area_list = driver.find_elements_by_xpath("//*[@class='box shopallCate']")
        business_area = []
        for area in area_list:
            if area.find_element_by_xpath("./h2").text == '商区':
                all_area = area.find_elements_by_xpath(".//*[@class='list']")
                for item in all_area:
                    area_name, area_info = self.details_spider(item)
                    one_area = Area(area_name=area_name, area_info=area_info)
                    business_area.append(one_area)

        driver.close()
        return business_area
