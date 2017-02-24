# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 17/2/23 下午5:49
# @Author   : Jason
# @File     : python3-upload.py

import os
import re
import requests
import random
import time
import urllib.parse
import hmac
import hashlib
import binascii
import base64


class ParamCheck(object):
    def __init__(self):
        self._err_tips = u''

    # 获取错误信息
    def get_err_tips(self):
        return self._err_tips

    # 检查参数是否是unicode
    # param_name 参数名
    # param_value 参数值
    def check_param_unicode(self, param_name, param_value):
        if param_value == None:
            self._err_tips = param_name + ' is None!'
            return False
        return True

    # 检查参数是否是int
    # param_name 参数名
    # param_value 参数值
    def check_param_int(self, param_name, param_value):
        if param_value == None:
            self._err_tips = param_name + ' is None!'
            return False
        if not isinstance(param_value, int):
            self._err_tips = param_name + ' is not int!'
            return False
        return True

    # 检查cos_path是否合法, 必须以/开始
    # 文件路径则不能以/结束, 目录路径必须以/结束
    # 路径合法返回True, 否则返回False
    def check_cos_path_valid(self, cos_path, is_file_path):
        if cos_path[0] != u'/':
            self._err_tips = 'cos path must start with /'
            return False

        last_letter = cos_path[len(cos_path) - 1]
        if is_file_path and last_letter == u'/':
            self._err_tips = 'for file operation, cos_path must not end with /'
            return False
        elif not is_file_path and last_letter != u'/':
            self._err_tips = 'for folder operation, cos_path must end with /'
            return False
        else:
            pass

        illegal_letters = ['?', '*', ':', '|', '\\', '<', '>', '"']
        for illegal_letter in illegal_letters:
            if cos_path.find(illegal_letter) != -1:
                self._err_tips = 'cos path contain illegal letter %s' % illegal_letter
                return False

        pattern = re.compile(r'/(\s*)/')
        if pattern.search(cos_path):
            self._err_tips = 'cos path contain illegal letter / /'
            return False
        return True

    # 检查不是cos的跟路基
    # 不等进行根路径操作的有 1 update 2 cretate 3 delete
    def check_not_cos_root(self, cos_path):
        if cos_path == u'/':
            self._err_tips = 'bucket operation is not supported by sdk,'
            ' please use cos console: https://console.qcloud.com/cos'
            return False
        else:
            return True

    # 检查本地文件有效(存在并且可读)
    def check_local_file_valid(self, local_path):
        if not os.path.exists(local_path):
            self._err_tips = 'local_file %s not exist!' % local_path
            return False
        if not os.path.isfile(local_path):
            self._err_tips = 'local_file %s is not regular file!' % local_path
            return False
        if not os.access(local_path, os.R_OK):
            self._err_tips = 'local_file %s is not readable!' % local_path
            return False
        return True

    # 检查分片大小有效
    def check_slice_size(self, slice_size):
        min_size = 512 * 1024  # 512KB
        max_size = 20 * 1024 * 1024  # 20MB
        if slice_size >= min_size and slice_size <= max_size:
            return True
        else:
            self._err_tips = 'slice_size is invalid, only accept [%d, %d]' \
                             % (min_size, max_size)
            return False

    # 检查文件上传的insert_only参数
    def check_insert_only(self, insert_only):
        if insert_only != 1 and insert_only != 0:
            self._err_tips = 'insert_only only support 0 and 1'
            return False
        else:
            return True

    # 检查move的over write标志
    def check_move_over_write(self, to_over_write):
        if to_over_write != 1 and to_over_write != 0:
            self._err_tips = 'to_over_write only support 0 and 1'
            return False
        else:
            return True

    # 检查文件的authority属性
    # 合法的取值只有eInvalid, eWRPrivate, eWPrivateRPublic和空值
    def check_file_authority(self, authority):
        if authority != u'' and \
                        authority != u'eInvalid' and \
                        authority != u'eWRPrivate' and \
                        authority != u'eWPrivateRPublic':
            self._err_tips = 'file authority valid value is:'
            'eInvalid, eWRPrivate, eWPrivateRPublic'
            return False
        else:
            return True

    # 检查x_cos_meta_dict, key和value都必须是UTF8编码
    def check_x_cos_meta_dict(self, x_cos_meta_dict):
        prefix_len = len('x-cos-meta-')
        for key in x_cos_meta_dict.keys():
            if not self.check_param_unicode('x-cos-meta-key', key):
                return False
            if not self.check_param_unicode('x-cos-meta-value',
                                            x_cos_meta_dict[key]):
                return False
            if key[0:prefix_len] != u'x-cos-meta-':
                self._err_tips = 'x-cos-meta key must start with x-cos-meta-'
                return False
            if len(key) == prefix_len:
                self._err_tips = 'x-cos-meta key must not just be x-cos-meta-'
                return False
            if (len(x_cos_meta_dict[key]) == 0):
                self._err_tips = 'x-cos-meta value must not be empty'
                return False
        return True

    # 检查更新文件的flag
    def check_update_flag(self, flag):
        if flag == 0:
            self._err_tips = 'no any attribute to be updated!'
            return False
        else:
            return True

    # 检查list folder的order
    # 合法取值0(正序), 1(逆序)
    def check_list_order(self, list_order):
        if list_order != 0 and list_order != 1:
            self._err_tips = 'list order is invalid, please use 0(positive) or 1(reverse)!'
            return False
        else:
            return True

    # 检查list folder的pattern
    # 合法取值eListBoth, eListDirOnly, eListFileOnly
    def check_list_pattern(self, list_pattern):
        if list_pattern != u'eListBoth' and \
                        list_pattern != u'eListDirOnly' and \
                        list_pattern != u'eListFileOnly':
            self._err_tips = 'list pattern is invalid,'
            ' please use eListBoth or eListDirOnly or eListFileOnly'
            return False
        else:
            return True


class CredInfo(object):
    def __init__(self, appid, secret_id, secret_key):
        self._appid = appid
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._param_check = ParamCheck()

    def get_appid(self):
        return self._appid

    def get_secret_id(self):
        return self._secret_id

    def get_secret_key(self):
        return self._secret_key


class CosConfig(object):
    def __init__(self):
        self._end_point = 'http://web.file.myqcloud.com/files/v1'
        self._user_agent = 'cos-python-sdk-v3.3'
        self._timeout = 30
        self._sign_expired = 300

    # 设置COS的域名地址
    def set_end_point(self, end_point):
        self._end_point = end_point

    # 获取域名地址
    def get_end_point(self):
        return self._end_point

    # 获取HTTP头中的user_agent
    def get_user_agent(self):
        return self._user_agent

    # 设置连接超时, 单位秒
    def set_timeout(self, time_out):
        assert isinstance(time_out, int)
        self._timeout = time_out

    # 获取连接超时，单位秒
    def get_timeout(self):
        return self._timeout

    # 设置签名过期时间, 单位秒
    def set_sign_expired(self, expired):
        assert isinstance(expired, int)
        self._sign_expired = expired

    # 获取签名过期时间, 单位秒
    def get_sign_expired(self):
        return self._sign_expired

    # 打开https
    def enable_https(self):
        self._end_point = 'https://web.file.myqcloud.com/files/v1'


class BaseOp(object):
    # cred: 用户的身份信息
    # config: cos_config配置类
    # http_session: http 会话
    # expired_period: 签名过期时间, 单位秒
    def __init__(self, cred, config, http_session):
        self._cred = cred
        self._config = config
        self._http_session = http_session
        self._expired_period = self._config.get_sign_expired()


class Auth(object):
    def __init__(self, cred):
        self.cred = cred

    def app_sign(self, bucket, cos_path, expired, upload_sign=True):
        appid = self.cred.get_appid()
        bucket = bucket
        secret_id = self.cred.get_secret_id()
        now = int(time.time())
        rdm = random.randint(0, 999999999)
        cos_path = urllib.parse.quote(cos_path.encode('utf8'), '~/')
        if upload_sign:
            fileid = '/%s/%s%s' % (appid, bucket, cos_path)
        else:
            fileid = cos_path
        if expired != 0 and expired < now:
            expired = now + expired
        sign_tuple = (appid, secret_id, expired, now, rdm, fileid, bucket)

        plain_text = 'a=%s&k=%s&e=%d&t=%d&r=%d&f=%s&b=%s' % sign_tuple
        secret_key = self.cred.get_secret_key().encode('utf8')
        sha1_hmac = hmac.new(secret_key, plain_text.encode('utf-8'), hashlib.sha1)
        hmac_digest = sha1_hmac.hexdigest()
        hmac_digest = binascii.unhexlify(hmac_digest)
        sign_hex = hmac_digest + plain_text.encode('utf-8')
        sign_base64 = base64.b64encode(sign_hex)
        return sign_base64

    # 单次签名(针对删除和更新操作)
    # bucket: bucket名称
    # cos_path: 要操作的cos路径, 以'/'开始
    def sign_once(self, bucket, cos_path):
        return self.app_sign(bucket, cos_path, 0)

    # 多次签名(针对上传文件，创建目录, 获取文件目录属性, 拉取目录列表)
    # bucket: bucket名称
    # cos_path: 要操作的cos路径, 以'/'开始
    # expired:  签名过期时间, UNIX时间戳
    #           如想让签名在30秒后过期, 即可将expired设成当前时间加上30秒
    def sign_more(self, bucket, cos_path, expired):
        return self.app_sign(bucket, cos_path, expired)

    # 下载签名(用于获取后拼接成下载链接，下载私有bucket的文件)
    # bucket: bucket名称
    # cos_path: 要下载的cos文件路径, 以'/'开始
    # expired:  签名过期时间, UNIX时间戳
    #           如想让签名在30秒后过期, 即可将expired设成当前时间加上30秒
    def sign_download(self, bucket, cos_path, expired):
        return self.app_sign(bucket, cos_path, expired, False)


class FileOp(BaseOp):
    # cred: 用户的身份信息
    # config: cos_config配置类
    # http_session: http 会话
    def __init__(self, cred, config, http_session):
        BaseOp.__init__(self, cred, config, http_session)
        # 单文件上传的最大上限是20MB
        self.max_single_file = 20 * 1024 * 1024

    def set_config(self, config):
        self._config = config
        self._expired_period = self._config.get_sign_expired()

    def _check_params(self, request):
        return None

    def upload_file(self, request):
        assert isinstance(request, UploadFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        local_path = request.get_local_path()
        file_size = os.path.getsize(local_path)

        suit_single_file_zie = 8 * 1024 * 1024
        if (file_size < suit_single_file_zie):
            return self.upload_single_file(request)

    def _sha1_content(self, content):
        sha1_obj = hashlib.sha1()
        sha1_obj.update(content)
        return sha1_obj.hexdigest()

    def upload_single_file(self, request):
        assert isinstance(request, UploadFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        local_path = request.get_local_path()
        file_size = os.path.getsize(local_path)
        # 判断文件是否超过单文件最大上限, 如果超过则返回错误
        # 并提示用户使用别的接口
        if file_size > self.max_single_file:
            return "file is to big, please use upload_file interface"

        auth = Auth(self._cred)
        bucket = request.get_bucket_name()
        cos_path = request.get_cos_path()
        expired = int(time.time()) + self._expired_period
        sign = auth.sign_more(bucket, cos_path, expired)

        http_header = {'Authorization': str(sign)[2:-1], 'User-Agent': self._config.get_user_agent()}

        with open(local_path, 'rb') as f:
            file_content = f.read()

        http_body = {}
        http_body['op'] = 'upload'
        http_body['filecontent'] = file_content
        http_body['sha'] = self._sha1_content(file_content)
        http_body['biz_attr'] = request.get_biz_attr()
        http_body['insertOnly'] = str(request.get_insert_only())

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header, files=http_body, timeout=timeout)

    def _build_url(self, bucket, cos_path):
        bucket = bucket.encode('utf8')
        print(bucket)
        bucket = str(bucket)[2:-1]
        end_point = self._config.get_end_point().rstrip('/').encode('utf8')
        end_point = str(end_point)[2:-1]
        appid = self._cred.get_appid()
        cos_path = urllib.parse.quote(cos_path.encode('utf8'), '~/')
        url = '%s/%s/%s%s' % (end_point, appid, bucket, cos_path)
        print(str(url))
        return url

    def send_request(self, method, bucket, cos_path, **args):
        url = self._build_url(bucket, cos_path)
        http_resp = {}
        try:
            if method == 'POST':
                http_resp = self._http_session.post(url, verify=False, **args)
            else:
                http_resp = self._http_session.get(url, verify=False, **args)

            status_code = http_resp.status_code
            if status_code == 200 or status_code == 400:
                return http_resp.json()
            else:
                err_detail = 'url:%s, status_code:%d' % (url, status_code)
                return err_detail
        except Exception as e:
            err_detail = 'url:%s, exception:%s' % (url, repr(e))
            return err_detail


class FolderOp(BaseOp):
    def __init__(self, cred, config, http_session):
        BaseOp.__init__(self, cred, config, http_session)

    def set_config(self, config):
        self._config = config
        self._expired_period = self._config.get_sign_expired()


class CosClient(object):
    # 设置用户的相关信息
    def __init__(self, appid, secret_id, secret_key):
        self._cred = CredInfo(appid, secret_id, secret_key)
        self._config = CosConfig()
        self._http_session = requests.session()
        self._file_op = FileOp(self._cred, self._config, self._http_session)
        self._folder_op = FolderOp(self._cred, self._config, self._http_session)

    # 设置config
    def set_config(self, config):
        assert isinstance(config, CosConfig)
        self._config = config
        self._file_op.set_config(config)
        self._folder_op.set_config(config)

    def upload_file(self, request):
        assert isinstance(request, UploadFileRequest)
        return self._file_op.upload_file(request)


class BaseRequest(object):
    # bucket_name: bucket的名称
    # cos_path: cos的绝对路径, 即从bucket下的根/开始
    def __init__(self, bucket_name, cos_path):
        self._bucket_name = bucket_name.strip()
        self._cos_path = cos_path.strip()
        self._param_check = ParamCheck()

    # 设置bucket_name
    def set_bucket_name(self, bucket_name=u''):
        self._bucket_name = bucket_name.strip()

    # 获取bucket_name
    def get_bucket_name(self):
        return self._bucket_name

    # 设置cos_path
    def set_cos_path(self, cos_path=u''):
        self._cos_path = cos_path.strip()

    # 获取cos_path
    def get_cos_path(self):
        return self._cos_path

    # 获取错误信息
    def get_err_tips(self):
        return self._param_check.get_err_tips()

    # 检查参数是否合法
    def check_params_valid(self):
        if not self._param_check.check_param_unicode('bucket', self._bucket_name):
            return False
        return self._param_check.check_param_unicode('cos_path', self._cos_path)


class UploadFileRequest(BaseRequest):
    # bucket_name:            bucket的名称
    # cos_path:               cos的绝对路径(目的路径), 从bucket根/开始
    # local_path:             上传的本地文件路径(源路径)
    # biz_attr:               文件的属性
    # insert_only:            是否覆盖写, 0覆盖, 1不覆盖,返回错误

    def __init__(self, bucket_name, cos_path, local_path, biz_attr=u'',
                 insert_only=1):
        super(UploadFileRequest, self).__init__(bucket_name, cos_path)
        self._local_path = local_path.strip()
        self._biz_attr = biz_attr
        self._insert_only = insert_only

    # 设置local_path
    def set_local_path(self, local_path):
        self._local_path = local_path.strip()

    # 获取local_path
    def get_local_path(self):
        return self._local_path

    # 设置biz_attr
    def set_biz_attr(self, biz_attr):
        self._biz_attr = biz_attr

    # 获取biz_attr
    def get_biz_attr(self):
        return self._biz_attr

    # 设置insert_only，0表示如果文件存在, 则覆盖
    def set_insert_only(self, insert_only):
        self._insert_only = insert_only

    # 获取insert_only
    def get_insert_only(self):
        return self._insert_only

    # 检查参数是否有效
    def check_params_valid(self):
        if not super(UploadFileRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, is_file_path=True):
            return False
        if not self._param_check.check_param_unicode('biz_attr', self._biz_attr):
            return False
        if not self._param_check.check_param_unicode('local_path', self._local_path):
            return False
        if not self._param_check.check_local_file_valid(self._local_path):
            return False
        if not self._param_check.check_param_int('insert_only', self._insert_only):
            return False
        return self._param_check.check_insert_only(self._insert_only)


class UploadImage:
    app_id = 10056151
    # secret id
    # AKIDtNtth4SdBNy5aidDI9wHEiPDYXvRsfbV
    secret_id = u'AKIDtNtth4SdBNy5aidDI9wHEiPDYXvRsfbV'
    # secret key
    # 7pdJ5w9Uq0OGderacgWaA4UCerip5AVe
    secret_key = u'7pdJ5w9Uq0OGderacgWaA4UCerip5AVe'
    # set bucket
    bucket = u'portal'

    def __init__(self):
        # cos client
        self.cos_client = CosClient(self.app_id, self.secret_id, self.secret_key)

    def upload(self, target_image_name, local_path):
        # upload
        request = UploadFileRequest(
            self.bucket,
            u'/card_image/%s' % target_image_name,
            local_path,
            insert_only=0
        )
        ret = self.cos_client.upload_file(request)
        # upload file ret: {
        # u'message': u'SUCCESS',
        # u'code': 0,
        # u'data': {
        # u'url': u'http://web.file.myqcloud.com/files/v1/card_image/test_upload.jpg',
        # u'access_url': u'http://portal-10056151.file.myqcloud.com/card_image/test_upload.jpg',
        # u'resource_path': u'/card_image/test_upload.jpg',
        # u'source_url': u'http://portal-10056151.cos.myqcloud.com/card_image/test_upload.jpg'
        # }}

        print("upload file ret:", repr(ret))

        return ret
