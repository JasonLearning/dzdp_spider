# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 上午10:52
# @Author   : Jason
# @File     : data_clean_driver.py

from __future__ import absolute_import, unicode_literals
import time

from celery import group
from celery.contrib import rdb
from celery.utils.log import get_task_logger
from celery import chain

from mx_celery import app
from tools.collections.shop_details_collection import ShopDetailsCollectionClass
from tools.collections.documents.shop_details_collection_documents import ShopDetailsCollection
from tools.collections.documents.shop_details_job_collection_documents import ShopDetailsJobCollection
from tools.collections.documents.shop_details_collection_documents import Comment
from tools.qcloud.image_cut.cut_helper import CutHelper

logger = get_task_logger(__name__)


class DataCleanDriver:
    def __init__(self):
        pass

    @staticmethod
    @app.task(name='drivers.dzdp.data_clean_driver.driver')
    def driver(parent_job_id):
        print("drivers.dzdp.data_clean.driver begin")
        c = ShopDetailsCollectionClass()
        job_id = c.create_job(parent_job_id)
        DataCleanDriver.clean_data(parent_job_id, job_id)

    @staticmethod
    def clean_data(parent_job_id, job_id):
        job = ShopDetailsJobCollection.objects(job_id=parent_job_id).first()
        new_job = ShopDetailsCollection.objects(job_id=job_id).first()
        job_status = "Finished"
        new_job.location, job_status = DataCleanDriver.clean_location(job.location, job_status)
        new_job.name, job_status = DataCleanDriver.clean_name(job.name, job_status)
        new_job.address, job_status = DataCleanDriver.clean_address(job.address, job_status)
        new_job.telephone, job_status = DataCleanDriver.clean_telephone(job.telephone, job_status)
        new_job.shop_info, job_status = DataCleanDriver.clean_shop_info(job.shop_info, job_status)
        new_job.imgUrl, job_status = DataCleanDriver.clean_imgUrl(job.imgUrl, job_status)
        new_job.environment, job_status = DataCleanDriver.clean_environment(job.environment, job_status)
        comment_list = []
        for comment in job.comment_list:
            comment_after, job_status = DataCleanDriver.clean_comment(comment, job_status)
            comment_list.append(comment_after)
        new_job.comment_list = comment_list
        new_job.job_status = job_status
        new_job.save()

    @staticmethod
    def clean_location(location, job_status):
        return location, job_status

    @staticmethod
    def clean_name(name, job_status):
        return name, job_status

    @staticmethod
    def clean_address(address, job_status):
        return address, job_status

    @staticmethod
    def clean_telephone(telephone, job_status):
        return telephone, job_status

    @staticmethod
    def clean_shop_info(shop_info, job_status):
        return shop_info, job_status

    @staticmethod
    def clean_imgUrl(imgUrl, job_status):
        return imgUrl, job_status

    @staticmethod
    def clean_environment(environment, job_status):
        return environment, job_status

    @staticmethod
    def clean_comment(comment, job_status):
        after_comment = Comment()
        pic_big = []
        pic_small = []
        pic_list = comment.pic
        for pic_url in pic_list:
            time_now = round(time.time()*1000)
            need_retry, big_img, small_img = CutHelper.cut_and_upload(pic_url, '%s.jpg' % time_now)
            if need_retry is not None:
                if isinstance(big_img, str):
                    pic_big.append(big_img)
                if isinstance(small_img, str):
                    pic_small.append(small_img)
        after_comment.person = comment.person
        after_comment.star = comment.star
        after_comment.scores = comment.scores
        after_comment.desc = comment.desc
        after_comment.pic_large = pic_big
        after_comment.pic_small = pic_small
        return after_comment, job_status

# DataCleanDriver.driver("2608e4d2-fa3e-11e6-a325-f079600aae50")
