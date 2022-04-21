#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:42
import json

from datetime import datetime
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入 cdn 产品模块的 models
from tencentcloud.cdn.v20180606 import models

from api.get_client_profile import get_client_instance

def get_cdn_client_instance(id, key):
    '''获取cdn的实例，用于后面对cdn的各种操作
    '''
    client = get_client_instance(id, key, "cdn")
    return client


def get_cdn_detail_info(client):
    '''获取所有CDN的详细信息，返回列表
    '''
    try:
        req = models.DescribeDomainsConfigRequest()
        # 参数列表为空：表示获取所有信息
        # 部分可选参数
        # Filters: Array Of DomainFilter, 查询条件过滤器，复杂类型
        # filter = DomainFilter()
        # filter.Name = "domain"
        # filter.Value = [domain]
        # filter.Fuzzy = False
        params = {}
        req.from_json_string(json.dumps(params))
    
        resp = client.DescribeDomainsConfig(req)
        # print(resp.to_json_string())
        print("获取所有cdn详细信息成功")
        return resp.Domains

    except TencentCloudSDKException as err:
        print(err)
        return []

def get_cdn_basic_info(client, domain_name):
    '''获取指定CDN的基本信息
    '''
    try:
        req = models.DescribeDomainsRequest()
        params = {
            "Limit": 1,
            "Filters": [
                {
                    "Name": "domain",
                    "Value": [ domain_name ],
                    "Fuzzy": False
                }
            ]
        }
        req.from_json_string(json.dumps(params))
    
        resp = client.DescribeDomains(req)
        # print(resp.to_json_string())
        print("获取指定cdn基本信息成功")
        return resp.Domains

    except TencentCloudSDKException as err:
        print(err)
        return []

def get_cdn_url_push_info(client):
    '''查询CDN预热配额和每日可用量
    '''
    try:
        req = models.DescribePushQuotaRequest()
        params = {}
        req.from_json_string(json.dumps(params))
        resp = client.DescribePushQuota(req)
        # print(resp.to_json_string())
        print("获取CDN预热配额和每日可用量信息成功")
        return resp.UrlPush

    except TencentCloudSDKException as err:
        print(err)
        return []


def update_cdn_url_push(client, urls, region):
    '''指定 URL 资源列表加载至 CDN 节点，支持指定加速区域预热
    默认情况下境内、境外每日预热 URL 限额为各 1000 条，每次最多可提交 20 条
    '''
    try:
        req = models.PushUrlsCacheRequest()
        params = {
            "Urls": urls,
            "Area": region,
        }
        req.from_json_string(json.dumps(params))
        resp = client.PushUrlsCache(req)
        print(resp.to_json_string())
        print("URL:{}预热成功".format(', '.join(urls)))
        return True

    except TencentCloudSDKException as err:
        print(err)
        return False


def get_cdn_purge_url_info(client):
    '''查询CDN刷新URL配额和每日可用量
    '''
    try:
        req = models.DescribePurgeQuotaRequest()
        params = {}
        req.from_json_string(json.dumps(params))
        resp = client.DescribePurgeQuota(req)
        # print(resp.to_json_string())
        print("获取CDN刷新URL配额和每日可用量信息成功")
        return resp.UrlPurge

    except TencentCloudSDKException as err:
        print(err)
        return []


def update_cdn_purge_url(client, urls, region):
    '''指定 URL 资源的刷新，支持指定加速区域刷新
    默认情况下境内、境外每日刷新 URL 限额为各 10000 条，每次最多可提交 1000 条
    '''
    try:
        req = models.PurgeUrlsCacheRequest()
        params = {
            "Urls": urls,
            "Area": region,
            "UrlEncode": True
        }
        req.from_json_string(json.dumps(params))
        resp = client.PurgeUrlsCache(req)
        print(resp.to_json_string())
        print("URL:{}刷新成功".format(', '.join(urls)))
        return True

    except TencentCloudSDKException as err:
        print(err)
        return False


def update_cdn_ssl(client, domain, cert_id):
    '''为指定域名的CDN更换SSL证书
    '''
    try:
        req = models.UpdateDomainConfigRequest()
        # 必选参数
        # Domain: String, 域名
        # 部分可选参数
        # Https: Https, Https 加速配置
        # 该类型详见 https://cloud.tencent.com/document/api/228/30987#Https
        timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "Domain": domain,
            "Https": {
                "Switch": "on",
                "CertInfo": {
                    "CertId": cert_id,
                    "Message": "Auto update by api at {}".format(timestr)
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

def update_cdn_https_options(client, domain, http2, hsts, age, hsts_subdomain, ocsp):
    '''为指定域名的CDN的HTTPS开启HTTP 2.0、HSTS、OCSP等多个可选项
    '''
    try:
        req = models.UpdateDomainConfigRequest()
        params = {
            "Domain": domain,
            "Https": {
                "Switch": "on"
            }
        }
        if http2:
            params["Https"]["Http2"] = "on"
        if hsts:
            params["Https"]["Hsts"] = {
                "Switch": "off",
                "MaxAge": 0,
                "IncludeSubDomains": "off"
            }
            params["Https"]["Hsts"]["Switch"] = "on"
            params["Https"]["Hsts"]["MaxAge"] = age
            if hsts_subdomain:
                params["Https"]["Hsts"]["IncludeSubDomains"] = "on"
        if ocsp:
            params["Https"]["OcspStapling"] = "on"

        req.from_json_string(json.dumps(params))
    
        resp = client.UpdateDomainConfig(req)
        print(resp.to_json_string())
        print("成功开启域名为{0}的CDN的HTTPS选项".format(domain))
    
    except TencentCloudSDKException as err:
        print(err)
        exit("为{}的CDN开启HTTPS选项功能出错".format(domain))
