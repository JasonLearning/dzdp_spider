# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/20 上午11:59
# @Author   : Jason
# @File     : search_by_area_collection_documents.py

from mongoengine import *


class Comment(EmbeddedDocument):
    person = StringField(max_length=200, required=True)
    star = StringField(max_length=1)
    scores = StringField(max_length=200)
    desc = StringField()
    pic_large = ListField(field=StringField())
    pic_small = ListField(field=StringField())


class ShopDetailsCollection(Document):
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
