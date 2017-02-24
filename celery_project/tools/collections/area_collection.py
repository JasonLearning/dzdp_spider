# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/20 上午11:03
# @Author   : Jason
# @File     : area_collection.py

from datetime import datetime
from pytz import timezone
from mongoengine import *

from tools.job_helper import JobField, JobStatus, Jobs
from tools.exceptions import *
from tools.collections.documents.area_collection_documents import AreaCollection


class AreaCollectionClass:
    db_name = "mx_dzdp_db"
    connect(db_name)

    @staticmethod
    def create_job(location, area_url):
        """
       [插入商品id]
       :param location:
       :param area_url:
       :return:
       """
        # 构建作业
        job = JobField.create_job(AreaCollection)
        job.location = location
        job.area_url = area_url
        job.save()

        return job.job_id

    @staticmethod
    def insert_areas(job_id, business_area):
        """
        [插入商品id]
        :param job_id:
        :param business_area:
        :return:
        """
        job = AreaCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        # [子任务商品id列表在字段]
        job.business_area = business_area
        job.save()

    @staticmethod
    def get_url(job_id):
        job = AreaCollection.objects(job_id=job_id).first()
        if job is None:
            raise InvalidParamException({"job_id": job_id})
        return job.area_url

# AreaCollectionClass.create_job("上海", "http://www.dianping.com/shopall/1/0#BDBlock")
# print(AreaCollectionClass.get_url("c9aa57a6-f71c-11e6-8dc7-f079600aae50"))
