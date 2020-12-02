#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:02
import json
from datetime import datetime

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入 ssl 产品模块的 models
from tencentcloud.ssl.v20191205 import models

from api.get_client_profile import get_client_instance

def get_ssl_client_instance(id, key):
    '''获取ssl的实例，用于后面对ssl的各种操作
    '''
    client = get_client_instance(id, key, "ssl")
    return client


def get_cert_list(client):
    '''获取所有的SSL证书列表
    '''
    try:
        # 实例化一个 ssl 实例信息查询请求对象,每个接口都会对应一个 request 对象
        req = models.DescribeCertificatesRequest()
        # 可选参数列表
        # Offset: Integer, 分页偏移量，从0开始
        # Limit:  Integer, 每页数量，默认20
        # SearchKey: String, 搜索关键词，可搜索证书 ID、备注名称、域名
        # CertificateType:  String, 证书类型：CA = 客户端证书，SVR = 服务器证书
        # ProjectId: Integer, 项目 ID
        # ExpirationSort: String, 按到期时间排序：DESC = 降序， ASC = 升序
        # CertificateStatus: Array Of Integer, 证书状态
        # Deployable:  Integer, 是否可部署，可选值：1 = 可部署，0 = 不可部署
        params = {}
        req.from_json_string(json.dumps(params))

        # 通过 client 对象调用 DescribeCertificatesRequest 方法发起请求，请求方法名与请求对象对应
        # 返回的 resp 是一个 DescribeCertificatesResponse 类的实例，与请求对象对应
        resp = client.DescribeCertificates(req)
        # 输出 json 格式的字符串回包
        # print(resp.to_json_string())
        # 也可以取出单个值，通过官网接口文档或跳转到 response 对象的定义处查看返回字段的定义
        # print(resp.TotalCount)
        print("获取ssl证书列表成功")
        return resp.Certificates
    except TencentCloudSDKException as err:
        print(err)
        return []


def get_cert_info(client, cert_id):
    '''根据id获取SSL证书的信息
    '''
    try:
        req = models.DescribeCertificateRequest()
        # 必选参数
        # CertificateId: String, 证书 ID
        params = {
            "CertificateId": cert_id
        }
        req.from_json_string(json.dumps(params))
    
        resp = client.DescribeCertificate(req)
        # print(resp.to_json_string())
        print("获取ssl证书{}的信息成功".format(cert_id))
        return resp
    
    except TencentCloudSDKException as err:
        print(err)
        exit("获取证书{}信息出错".format(cert_id))


def get_cert_detail(client, cert_id):
    '''根据id获取SSL证书的详情
    '''
    try:
        req = models.DescribeCertificateDetailRequest()
        # 必选参数
        # CertificateId: String, 证书 ID
        params = {
            "CertificateId": cert_id
        }
        req.from_json_string(json.dumps(params))
    
        resp = client.DescribeCertificateDetail(req)
        # print(resp.to_json_string())
        print("获取ssl证书{}的详细信息成功".format(cert_id))

    except TencentCloudSDKException as err:
        print(err)
        exit("获取证书{}详细信息出错".format(cert_id))


def delete_cert(client, cert_id):
    '''删除指定id的SSL证书
    '''
    try:
        req = models.DeleteCertificateRequest()
        # 必选参数
        # CertificateId: String, 证书 ID
        params = {
            "CertificateId": cert_id
        }
        req.from_json_string(json.dumps(params))
    
        resp = client.DeleteCertificate(req)
        # print(resp.to_json_string())
        print("删除ssl证书{}成功".format(cert_id))

    except TencentCloudSDKException as err:
        print(err)
        exit("删除证书{}出错".format(cert_id))


def upload_cert(client, local_cert_info):
    '''把本地的SSL证书上传到腾讯云，返回新证书的id
    '''
    try:
        req = models.UploadCertificateRequest()
        # 必选参数
        # CertificatePublicKey: String, 证书公钥内容
        # CertificatePrivateKey: String, 私钥内容，证书类型为 SVR 时必填，为 CA 时可不填
        # 可选参数列表
        # CertificateType: String, 证书类型，默认 SVR。CA = 客户端证书，SVR = 服务器证书
        # Alias: String, 备注名称
        # ProjectId: Integer, 项目 ID
        timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "CertificatePublicKey": local_cert_info["cer"],
            "CertificatePrivateKey": local_cert_info["key"],
            "CertificateType": local_cert_info["type"],
            "Alias": "Auto upload by api at {}".format(timestr)
        }
        req.from_json_string(json.dumps(params))
    
        resp = client.UploadCertificate(req)
        # print(resp.to_json_string())
        print("上传ssl证书成功")
        return resp.CertificateId

    except TencentCloudSDKException as err:
        print(err)
        return ""
