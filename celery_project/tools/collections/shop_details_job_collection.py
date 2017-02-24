# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 上午10:10
# @Author   : Jason
# @File     : shop_details_job_collection.py

from datetime import datetime
from pytz import timezone
from mongoengine import *

from tools.job_helper import JobField, JobStatus, Jobs
from tools.exceptions import *
from tools.collections.documents.shop_details_job_collection_documents import ShopDetailsJobCollection


class ShopDetailsJobCollectionClass:
    db_name = "mx_dzdp_db"
    connect(db_name)

    @staticmethod
    def create_job(shop_url, parent_job_id):
        # 构建作业
        job = JobField.create_job(ShopDetailsJobCollection)
        job.shop_url = shop_url
        job.parent_job_id = parent_job_id
        job.save()

        return job.job_id

    @staticmethod
    def insert_shop_details(job_id, job_status, location, name, address, telephone, shop_info, imgUrl, environment, comment_list):
        if not isinstance(comment_list, (tuple, list)):
            raise InvalidParamException("invalid comment_list type!", {'comment_list': comment_list})

        job = ShopDetailsJobCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        # [子任务商品id列表在字段]
        job.location = location
        job.job_status = job_status
        job.name = name
        job.address = address
        job.telephone = telephone
        job.shop_info = shop_info
        job.imgUrl = imgUrl
        job.environment = environment
        job.comment_list = comment_list
        job.save()

    @staticmethod
    def get_url(job_id):
        job = ShopDetailsJobCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        return job.shop_url

# ShopDetailsCollectionClass.create_job("http://www.dianping.com/shop/21213855")
