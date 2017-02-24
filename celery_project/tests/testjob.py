# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 下午2:14
# @Author   : Jason
# @File     : testjob.py

from tools.job_helper import JobField

job = JobField.create_job()
print(job.parent_job_id)
