#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 16:15

# 腾讯云支持使用单域名和泛域名的证书，例如
# acme.sh --issue  -d "whuzfb.cn" -d "*.whuzfb.cn" --dns dns_dp
# acme.sh --issue  -d "blog.whuzfb.cn" --dns dns_dp

# 使用ACME申请的SSL完整证书的本地存放路径
CER_FILE = "/home/zfb/.acme.sh/whuzfb.cn/fullchain.cer"

# 使用ACME申请的SSL证书私钥的本地存放路径
KEY_FILE = "/home/zfb/.acme.sh/whuzfb.cn/whuzfb.cn.key"

# CDN服务配置的域名（需要提前在腾讯云网页前端创建）
# 如果ACME申请的证书为泛域名证书，且要配置多个CDN加速
# CDN_DOMAIN = ["blog.whuzfb.cn", "blog2.whuzfb.cn", "web.whuzfb.cn"]
CDN_DOMAIN = ["blog.whuzfb.cn"]

# 腾讯云：https://console.cloud.tencent.com/cam/capi
SECRETID = "AKeee5555512345677777123456788889876"
SECRETKEY = "A71234567890abcdefedcba098765432"

# 控制功能开关
# 是否进行上传证书文件的操作（根据CER_FILE和KEY_FILE）
UPLOAD_SSL = True
# 以下为HTTPS额外功能
# 是否开启HTTP2
ENABLE_HTTP2 = True
# 是否开启HSTS
ENABLE_HSTS = True
# 为HSTS设定最长过期时间（以秒为单位）
HSTS_TIMEOUT_AGE = 1
# HSTS包含子域名（仅对泛域名有效）
HSTS_INCLUDE_SUBDOMAIN = True
# 是否开启OCSP
ENABLE_OCSP = True
# 是否删除适用于CDN_DOMAIN域名下的其他所有证书
# 满足以下条件：证书适用于CDN_DOMAIN、证书id不是本次使用的id
DELETE_OLD_CERTS = True

# 是否进行为CDN_DOMAIN更换SSL证书的操作
# 若UPDATE_SSL = True且UPLOAD_SSL = True，则CERT_ID可不设置，直接利用UPLOAD_SSL的证书
UPDATE_SSL = True
CERT_ID = ""
# 是否进行预热URL的操作
PUSH_URL = True
# 是否进行刷新URL的操作
PURGE_URL = True
# 自定义的预热URL（默认会预热sitemap.xml的所有链接）文件路径
# 该文件内，每行一个URL，例如
# https://blog.whuzfb.cn/img/me2.jpg
# https://blog.whuzfb.cn/img/home-bg.jpg
URLS_FILE = "urls.txt"
