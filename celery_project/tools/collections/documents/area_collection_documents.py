# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/20 上午10:54
# @Author   : Jason
# @File     : area_collection_documents.py

from mongoengine import *


class Area(EmbeddedDocument):
    area_name = StringField()
    area_info = ListField(field=StringField())


class AreaCollection(Document):
    job_id = StringField(required=True)
    job_status = StringField(max_length=100)
    job_created_timestamp = DateTimeField()
    job_updated_timestamp = DateTimeField()
    parent_job_id = StringField()
    job_result = StringField()
    location = StringField()
    area_url = StringField()
    business_area = EmbeddedDocumentListField(document_type=Area)
