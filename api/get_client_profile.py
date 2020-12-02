#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:17

from tencentcloud.common import credential
# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入ssl产品模块的 client
from tencentcloud.ssl.v20191205 import ssl_client
# 导入cdn产品模块的 client
from tencentcloud.cdn.v20180606 import cdn_client
# 导入ecdn产品模块的 client
from tencentcloud.ecdn.v20191012 import ecdn_client

def get_client_instance(id, key, product):
    '''获取指定endpoint的实例，用于后面对其的各种操作
    '''
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 secretId，secretKey, 此处还需注意密钥对的保密
        cred = credential.Credential(id, key)

        # 实例化一个 http 选项，可选
        httpProfile = HttpProfile()
        # post 请求 (默认为 post 请求)
        httpProfile.reqMethod = "POST"
        # 请求超时时间，单位为秒 (默认60秒)
        httpProfile.reqTimeout = 30
        # 不指定接入地域域名 (默认就近接入)
        httpProfile.endpoint = "{}.tencentcloudapi.com".format(product)

        # 实例化一个 client 选项，可选
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的 client 对象，clientProfile 是可选的
        if product == "ssl":
            client = ssl_client.SslClient(cred, "", clientProfile)
            print("实例化一个ssl_client成功")
        elif product == "cdn":
            client = cdn_client.CdnClient(cred, "", clientProfile)
            print("实例化cdn client成功")
        elif product == "ecdn":
            client = ecdn_client.EcdnClient(cred, "", clientProfile)
            print("实例化ecdn client成功")
        else:
            exit("本程序仅支持ssl、cdn、ecdn")
        return client
    except TencentCloudSDKException as err:
        print(err)
        exit(-1)