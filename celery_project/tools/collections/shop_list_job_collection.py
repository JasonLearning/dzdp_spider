# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/16 下午5:11
# @Author   : Jason
# @File     : shop_list_job_collection.py

from datetime import datetime
from pytz import timezone
from mongoengine import *

from tools.job_helper import JobField, JobStatus, Jobs
from tools.exceptions import *
from tools.collections.documents.shop_list_job_collection_document import ShopListCollection


class ShopListJobCollectionClass:
    db_name = "mx_dzdp_db"
    connect(db_name)

    @staticmethod
    def create_job(brand, category_url):
        """
       [插入商品id]
       :param brand:
       :param category_url:
       :return:
       """
        # 构建作业
        job = JobField.create_job(ShopListCollection)
        job.category_url = category_url
        job.brand = brand
        job.shop_url_list = []
        job.save()

        return job.job_id

    @staticmethod
    def insert_shop_id_list(job_id, shop_url_list):
        """
        [插入商品id]
        :param job_id:
        :param shop_url_list:
        :return:
        """
        if not isinstance(shop_url_list, (tuple, list)):
            raise InvalidParamException("invalid shop_id_list type!", {'shop_id_list': shop_url_list})

        job = ShopListCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        # [子任务商品id列表在字段]
        job.shop_url_list = shop_url_list
        job.save()

    @staticmethod
    def get_url(job_id):
        job = ShopListCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        return job.category_url

    @staticmethod
    def get_shop_url_list(job_id):
        job = ShopListCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        return job.shop_url_list
