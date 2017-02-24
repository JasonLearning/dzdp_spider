# coding=utf-8

from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest

app_id = 10056151
# secret id
# AKIDtNtth4SdBNy5aidDI9wHEiPDYXvRsfbV
secret_id = u'AKIDtNtth4SdBNy5aidDI9wHEiPDYXvRsfbV'
# secret key
# 7pdJ5w9Uq0OGderacgWaA4UCerip5AVe
secret_key = u'7pdJ5w9Uq0OGderacgWaA4UCerip5AVe'

# cos client
cos_client = CosClient(app_id, secret_id, secret_key)

# set bucket
bucket = u'portal'

# upload
request = UploadFileRequest(bucket, u'/card_image/test_upload.jpg', u'./suit.jpg')
ret = cos_client.upload_file(request)
print "upload file ret:", repr(ret)
