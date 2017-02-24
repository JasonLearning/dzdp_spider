# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 下午4:55
# @Author   : Jason
# @File     : shop_list_collection_document.py
from mongoengine import *


class ShopListCollection(Document):
    job_id = StringField(required=True)
    job_status = StringField(max_length=100)
    job_created_timestamp = DateTimeField()
    job_updated_timestamp = DateTimeField()
    parent_job_id = StringField()
    job_result = StringField()
    category_url = StringField()
    brand = StringField()
    shop_url_list = ListField(field=StringField())
