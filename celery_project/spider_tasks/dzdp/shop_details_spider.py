# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/16 上午11:39
# @Author   : Jason
# @File     : shop_details_spider.py

from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import Task
from celery.utils.log import get_task_logger

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSelectorException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tools.collections.shop_details_job_collection import ShopDetailsJobCollectionClass
from tools.collections.documents.shop_details_job_collection_documents import Comment

logger = get_task_logger(__name__)


class ShopDetailsSpider(Task):
    name = 'dzdp.shop_details_spider'

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

        collection = ShopDetailsJobCollectionClass()
        shop_url = collection.get_url(job_id)

        driver = self.init_web_driver()
        try:
            driver.get(shop_url)
            job_status, location, name, area, address, telephone, shop_info, img_url, environment, comment_list = self.parse(driver)
            collection.insert_shop_details(job_id, job_status, location, name, address, telephone,
                                           shop_info, img_url, environment, comment_list)
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

    def get_big_img(self, small_img_url):
        driver = webdriver.PhantomJS(executable_path="/Users/simon/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
        driver.get(small_img_url)
        url = "Failed"
        try:
            big_img_url = driver.find_element_by_xpath("//*[@id='J_pic-wrap']/div[2]/img").get_attribute("src")
            url = big_img_url
        except NoSuchElementException:
            pass
        driver.quit()
        sleep(5)
        return url

    def analysis(self, driver):
        """
        解析页面信息函数
        """
        location = driver.find_element_by_xpath("//*[@id='page-header']/div[1]/a[2]").text
        name = driver.find_element_by_class_name("shop-name")
        name = str(name.text).split('\n')[0]
        area = driver.find_element_by_xpath("//*[@id='body']/div[2]/div[1]/a[2]")
        try:
            address = driver.find_element_by_xpath("//*[@id='basic-info']/div[2]/span[2]").text
        except NoSuchElementException:
            address = ""
        try:
            telephone = driver.find_element_by_xpath("//*[@id='basic-info']/p/span[2]").text
            # //*[@id="basic-info"]/div[4]/p[1]/span[2]
        except NoSuchElementException:
            telephone = ""
        shop_info = {}
        try:
            all_info = driver.find_element_by_xpath("//*[@id='basic-info']/div[4]")
            items = all_info.find_elements_by_xpath(".//*[@class='info info-indent']")
            for item in items:
                item_name = item.find_element_by_xpath(".//*[@class='info-name']").get_attribute('innerHTML')
                item_name = item_name.strip().replace('&nbsp;', '')
                info = item.find_element_by_xpath(".//*[@class='item']").get_attribute('innerHTML').strip()
                if "别名：" in item_name:
                    item_name = "nickname"
                if "营业时间：" in item_name:
                    item_name = "time"
                shop_info[item_name] = info
        except NoSuchElementException:
            pass
        imgUrl = driver.find_element_by_xpath("//*[@id='aside']/div[1]/div/a/img").get_attribute('src')
        environment = []
        # //*[@id="shop-tabs"]/div/div/a[1]/img
        img_list = driver.find_elements_by_xpath("//*[@id='shop-tabs']/div/div/a/img")
        for img in img_list:
            environment.append(img.get_attribute('src'))
        return location, name, area.text, address, telephone, shop_info, imgUrl, environment

    def commentAnalysis(self, comment):
        """
        解析评论函数
        """
        id = comment.get_attribute("id")
        person = comment.find_element_by_class_name("user-info")
        stars = comment.find_element_by_xpath("//*[@id='%s']/div/p[1]/span[1]" % id).get_attribute('class')
        star = stars[-2]
        scores = comment.find_element_by_class_name("shop-info")
        # 折叠时分为完整评论与简短评论，非折叠时仅有普通评论
        # 异常处理， 当有完整评论时抓取完整评论，否则抓取普通评论
        try:
            desc = comment.find_element_by_xpath(".//*[@class='desc J-desc']")
        except (NoSuchElementException, InvalidSelectorException) as I:
            desc = comment.find_element_by_class_name("desc")
        pic = []
        picture = comment.find_elements_by_xpath(".//*[@class='item J-photo']")
        for p in picture:
            big_img = self.get_big_img(p.get_attribute('href'))
            pic.append(big_img)
        return person.text, star, scores.text, desc.get_attribute("innerHTML").strip(), pic

    def parse(self, driver):
        """
        抓取详细页面信息
        """
        job_status = "Finished"
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "comment"))
            )
        except TimeoutException:
            print("time out")
            driver.quit()
            job_status = "Failed"
            return job_status

        (location, name, area, address, telephone, shop_info, imgUrl, environment) = self.analysis(driver)
        comment_list = []
        comments = driver.find_elements_by_xpath("//*[@id='comment']/ul/li")
        for comment in comments:
            (person, star, scores, desc, pic) = self.commentAnalysis(comment)
            temp_comment = Comment(person=person, star=star, scores=scores, desc=desc, pic=pic)
            comment_list.append(temp_comment)

        return job_status, location, name, area, address, telephone, shop_info, imgUrl, environment, comment_list

# s = ShopDetailsSpider()
# s.run_inner(job_id="d2cf31f4-f806-11e6-b105-f079600aae50")
