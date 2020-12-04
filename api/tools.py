#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:45

def read_file(name):
    '''读取文件内容
    '''
    with open(name, 'r') as file:
        text = file.read()
        return text


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def resize_url_list(url_list, group_size):
    '''将一维列表按照指定长度分割
    '''
    url_chunks = list(chunks(url_list, group_size))
    results = []
    for i in range(len(url_chunks)):
        results.append(url_chunks[i])
    print("重置的URL列表个数{}，每个列表包含文件数{}".format(len(results), group_size))
    return results


def get_sitemap_urls(url):
    '''从给定的sitemap.xml文件获取链接
    '''
    import requests
    import re
    text = requests.get(url).text
    pattern = re.compile(r'<loc>(.*?)</loc>')
    results = re.findall(pattern, text)
    url_list = []
    for res in results:
        if not res.endswith("/"):
            res = res + "/"
        url_list.append(res)
    return url_list


def get_urls_from_file(file_name):
    '''从给定的文件获取链接
    '''
    with open(file_name, 'r') as file:
        return [x.strip() for x in file.readlines()]

def generate_https(https):
    '''由于Https无法序列化，自己将其改为字典（已弃用）
    '''
    server_cert = {}
    server_cert["CertId"] = https.CertInfo.CertId
    server_cert["CertName"] = https.CertInfo.CertName
    server_cert["Certificate"] = https.CertInfo.Certificate
    server_cert["PrivateKey"] = https.CertInfo.PrivateKey
    server_cert["ExpireTime"] = https.CertInfo.ExpireTime
    server_cert["DeployTime"] = https.CertInfo.DeployTime
    server_cert["Message"] = https.CertInfo.Message

    client_cert = {}
    client_cert["Certificate"] = https.ClientCertInfo.Certificate
    client_cert["CertName"] = https.ClientCertInfo.CertName
    client_cert["ExpireTime"] = https.ClientCertInfo.ExpireTime
    client_cert["DeployTime"] = https.ClientCertInfo.DeployTime

    hsts = {}
    hsts["Switch"] = https.Hsts.Switch
    hsts["MaxAge"] = https.Hsts.MaxAge
    hsts["IncludeSubDomains"] = https.Hsts.IncludeSubDomains

    res = {}
    res["Switch"] = https.Switch
    res["Http2"] = https.Http2
    res["OcspStapling"] = https.OcspStapling
    res["VerifyClient"] = https.VerifyClient
    res["Spdy"] = https.Spdy
    res["SslStatus"] = https.SslStatus
    res["CertInfo"] = server_cert
    res["ClientCertInfo"] = client_cert
    res["Hsts"] = https.Hsts
    return res
