# coding=utf-8
from __future__ import absolute_import, unicode_literals

import os
import time

import requests
from PIL import Image
from io import BytesIO

from requests import HTTPError
from tools.qcloud.cos_api.python_upload import UploadImage


class CutHelper:
    def __init__(self):
        pass

    @staticmethod
    def fix_http_url(url):
        if url.startswith("//"):
            fixed_url = "%s%s" % ("http:", url)
        elif url.startswith("http"):
            fixed_url = url
        else:
            fixed_url = url

        return fixed_url

    @staticmethod
    def cut_and_upload(src_img_url, target_image_name):
        need_retry = False
        card_big_image_url = None
        card_small_image_url = None
        try:
            r = requests.get(src_img_url)
            r.raise_for_status()
            if r.status_code == 200:
                print("[cur_and_upload]get image successful")
            # [cut]
            img = Image.open(BytesIO(r.content))
            x, y = img.size
            y -= 80
            box = (0, 0, 0 + x, 0 + y)
            img_after = img.crop(box)
            local_image_path = '/tmp/%s' % ('big_' + target_image_name)
            img_after.save(local_image_path)
            # [upload]
            ui = UploadImage()
            ret = ui.upload(('big_' + target_image_name), local_image_path)
            # [获取卡片图cos-url]
            if ret['code'] == 0:
                card_big_image_url = ret['data']['source_url']
                print("[cut_and_upload]upload successful url:%s" % card_big_image_url)
            elif ret['code'] == -4018:
                card_big_image_url = ret['data']['access_url']
                print("[cut_and_upload]file already exists url:%s" % card_big_image_url)
            else:
                need_retry = True
                print("[cut_and_upload]upload failure!")

            # [delete file]
            os.remove(local_image_path)

            min_px = min(x, y)
            box = ((x - min_px) / 2, 0, (x - min_px) / 2 + min_px, 0 + min_px)
            img_after = img.crop(box)
            local_image_path = '/tmp/%s' % ('small_' + target_image_name)
            img_after.save(local_image_path)
            # [upload]
            ui = UploadImage()
            ret = ui.upload(('small_' + target_image_name), local_image_path)
            # [获取卡片图cos-url]
            if ret['code'] == 0:
                card_small_image_url = ret['data']['source_url']
                print("[cut_and_upload]upload successful url:%s" % card_small_image_url)
            elif ret['code'] == -4018:
                card_small_image_url = ret['data']['access_url']
                print("[cut_and_upload]file already exists url:%s" % card_small_image_url)
            else:
                need_retry = True
                print("[cut_and_upload]upload failure!")

            # [delete file]
            os.remove(local_image_path)
        except HTTPError:
            print("[cut_helper]get image http error")
            need_retry = True
        except OSError:  # for remove
            print("[cut_helper]remove file not exists")
            need_retry = True

        return need_retry, card_big_image_url, card_small_image_url


if __name__ == '__main__':
    def test_cut_and_upload():
        url = "http://qcloud.dpfile.com/pc/mzD1Js5cY3gJZw1KDyyDkDxjSin4gm-SbusC9DQ1VxiWaWl-JNHXcz6PguBWxtDiTYGVDmosZWTLal1WbWRW3A.jpg"

        a, b, c = CutHelper.cut_and_upload(url, 'heng.jpg')
        print(a, b, c)

    test_cut_and_upload()
