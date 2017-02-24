# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 下午4:53
# @Author   : Jason
# @File     : shop_details_collection_documents.py
from mongoengine import *


class Comment(EmbeddedDocument):
    person = StringField(max_length=200, required=True)
    star = StringField(max_length=1)
    scores = StringField(max_length=200)
    desc = StringField()
    pic = ListField(field=StringField())


class ShopDetailsJobCollection(Document):
    job_id = StringField(required=True)
    job_status = StringField(max_length=100)
    job_created_timestamp = DateTimeField()
    job_updated_timestamp = DateTimeField()
    parent_job_id = StringField()
    job_result = StringField()
    shop_url = StringField()
    location = StringField()
    name = StringField(max_length=200)
    area = StringField(max_length=200)
    address = StringField(max_length=200)
    telephone = StringField(max_length=200)
    # time = StringField(max_length=200)
    shop_info = DictField(field=StringField())
    imgUrl = URLField()
    environment = ListField(field=StringField())
    comment_list = EmbeddedDocumentListField(document_type=Comment)
