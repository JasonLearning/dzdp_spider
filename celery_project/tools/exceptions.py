# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/17 下午2:39
# @Author   : Jason
# @File     : exceptions.py


class InvalidGoodUrlException(Exception):
    pass


class InvalidCategoryUrlException(Exception):
    pass


class DocumentNotFoundException(Exception):
    pass


class InvalidParamException(Exception):
    pass
