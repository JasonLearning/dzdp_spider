# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/16 下午3:51
# @Author   : Jason
# @File     : tasks.py

import celeryconfig
from celery import Celery
app = Celery()
app.config_from_object(celeryconfig)


@app.task(name='sum_of_two_numbers')
def add(x, y):
    return x + y

if __name__ == '__main__':
    app.worker_main()
