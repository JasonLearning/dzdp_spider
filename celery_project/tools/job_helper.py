# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 上午11:28
# @Author   : Jason
# @File     : job_helper.py

import uuid

from datetime import datetime
from pytz import timezone
from mongoengine import *


class Jobs(Document):
    job_id = StringField(required=True)
    job_status = StringField(max_length=100)
    job_created_timestamp = DateTimeField()
    job_updated_timestamp = DateTimeField()
    parent_job_id = StringField()
    job_result = StringField()


class JobField:

    @staticmethod
    def gen_job_id():
        job_id = str(uuid.uuid1())

        return job_id

    @staticmethod
    def get_datetime_now():
        now = datetime.now(tz=timezone('Asia/Shanghai'))

        return now

    @staticmethod
    def create_job(Field):
        now = JobField.get_datetime_now()
        job = Field(job_id=JobField.gen_job_id(),
                    job_status=JobStatus.just_created,
                    job_created_timestamp=now,
                    job_updated_timestamp=now,
                    parent_job_id="",
                    job_result="")

        return job


class JobSyncStatus:
    def __init__(self):
        pass

    wait_sync = 'wait_sync'
    sync_data_ready = 'sync_data_ready'
    already_sync = 'already_sync'


class JobStatus:
    def __init__(self):
        pass

    just_created = 'just_created'
    throw_into_mq = 'throw_into_mq'
    wait_schedule = 'wait_schedule'
    running = 'running'
    finished = 'finished'
    err_exit = 'err_exit'
    archived = 'archived'  # 归档 使用场景：商品详情爬虫 爬取的商品信息归档
    timeout = 'timeout'

    status_list = [
        just_created,
        throw_into_mq,
        wait_schedule,
        running
    ]
    spider_sub_job_split_done = 'spider_sub_job_split_done'  # 爬虫子作业切分完毕

