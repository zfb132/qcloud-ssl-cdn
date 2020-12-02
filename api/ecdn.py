#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:50
import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入 ecdn 产品模块的 models
from tencentcloud.ecdn.v20191012 import models

from api.get_client_profile import get_client_instance

def get_ecdn_client_instance(id, key):
    '''获取ecdn的实例，用于后面对ecdn的各种操作
    '''
    client = get_client_instance(id, key, "ecdn")
    return client


def get_ecdn_basic_info(client):
    '''获取所有ECDN的基本信息，返回列表
    '''
    try:
        req = models.DescribeDomainsRequest()
        params = {}
        req.from_json_string(json.dumps(params))
        resp = client.DescribeDomains(req)
        # print(resp.to_json_string())
        print("获取所有ecdn基本信息成功")
        return resp.Domains

    except TencentCloudSDKException as err:
        print(err)
        return []

def get_ecdn_detail_info(client):
    '''获取所有ECDN的详细信息，返回列表
    '''
    try:
        req = models.DescribeDomainsConfigRequest()
        params = {}
        req.from_json_string(json.dumps(params))
        resp = client.DescribeDomainsConfig(req) 
        # print(resp.to_json_string())
        print("获取所有ecdn详细信息成功")
        return resp.Domains

    except TencentCloudSDKException as err:
        print(err)
        return []

def update_ecdn_ssl(client, domain, cert_id):
    '''为指定域名的CDN的更换SSL证书
    '''
    # 为ecdn更新证书，使用ecdn相关接口
    # https://console.cloud.tencent.com/api/explorer?Product=ecdn&Version=2019-10-12
    try:
        req = models.UpdateDomainConfigRequest()
        # 必选参数
        # Domain: String, 域名
        # 部分可选参数
        # Https: Https, Https 加速配置
        # 该类型详见 https://cloud.tencent.com/document/api/228/30987#Https
        params = {
            "Domain": domain,
            "Https": {
                "CertInfo": {
                    "CertId": cert_id
                }
            }
        }
        req.from_json_string(json.dumps(params))
        resp = client.UpdateDomainConfig(req) 
        print(resp.to_json_string())
        print("成功更新域名为{0}的CDN的ssl证书为{1}".format(domain, cert_id))
    
    except TencentCloudSDKException as err:
        print(err)
        exit("为CDN设置SSL证书{}出错".format(cert_id))