# coding=utf-8
from PIL import Image
import requests
from io import BytesIO

# get image
from bson import Binary
from pymongo import MongoClient

# im = Image.open('https://cbu01.alicdn.com/img/ibank/2016/402/065/3704560204_970532914.460x460xz.jpg')
from celery_proj.tools.qcloud.cos_api.upload_image import UploadImage


def store_img():
    # url = "https://img.alicdn.com/imgextra/i4/2228361831/TB2CzzCc9tkpuFjy0FhXXXQzFXa_!!2228361831.jpg"
    url = "https://img.alicdn.com/imgextra/i1/2228361831/TB2PJa2ppXXXXa8XXXXXXXXXXXX_!!2228361831.jpg"
    r = requests.get(url)
    print repr(r)
    img = Image.open(BytesIO(r.content))

    print "size:%s" % (img.size,)
    x, y = img.size
    if x == y:
        img.thumbnail((540, 540))

        c_img = img.crop((46, 5, 494, 535))
        c_img.save('11.jpg')
    else:
        img.thumbnail((464, 575))

        c_img = img.crop((8, 23, 456, 523))
        c_img.save('45.jpg')

    # upload
    # ui = UploadImage()
    # ui.upload('test.jpg', u'./hih.jpg')

    # write image
    # with open('./fan.jpg', 'w') as f:
    # c_img.save(f)
    # f.write(r.content)

    # write in db
    def insert(content):
        b_content = Binary(content)

        mc = MongoClient()
        c = mc['test']['image']
        c.insert_one({
            "img_src": 'http://',
            "img": b_content
        })

        # insert(r.content)


def get_img():
    mc = MongoClient()
    c = mc['test']['image']
    r = c.find_one({
        "img_src": 'http://'
    })
    # r['img']

    with open('./fan.jpg', 'w') as f:
        f.write(r['img'])


# get_img()


store_img()
