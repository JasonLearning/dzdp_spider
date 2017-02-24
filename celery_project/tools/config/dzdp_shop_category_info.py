# coding=utf-8
from __future__ import absolute_import, unicode_literals


class DzdpShopCategoryInfo:
    def __init__(self):
        pass

    brand = [
        {
            "name": "hm",
            "city": "上海",
            "url": "http://www.dianping.com/search/branch/1/0_2021353/g0",
        },
        {
            "name": "zara",
            "city": "上海",
            "url": "http://www.dianping.com/search/branch/1/0_1866661/g0",
        },
        # {
        #     "name": "dazzle",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/branch/1/0_3097282/g0",
        # },
        # {
        #     "name": "miss-sixty",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/branch/1/0_1868419/g0",
        # },
        # {
        #     "name": "mo_co",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/branch/1/0_3997813/g0",
        # },
        # {
        #     "name": "snidel",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/keyword/1/0_snidel",
        # },
        # {
        #     "name": "ur",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/keyword/1/0_UR",
        # },
        # {
        #     "name": "uniqlo",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/branch/1/0_1892386/g0",
        # },
        # {
        #     "name": "ochirly",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/branch/1/0_1860088/g0",
        # },
        # {
        #     "name": "fiveplus",
        #     "city": "上海",
        #     "url": "http://www.dianping.com/search/branch/1/0_3213904/g0",
        # },
    ]

    shop_id = [
        {
            "name": "zara",
            "id": "0001"
        }
    ]

    area = [
        {
            "name": "上海",
            "url": "http://www.dianping.com/shopall/1/0#BDBlock",
        }
    ]

for category_meta in DzdpShopCategoryInfo.brand:
    print(category_meta['name'], category_meta['url'])