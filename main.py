#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:56
from api import cdn, ecdn, ssl, tools
import config

def run_config_ssl(id, key, cer_file, key_file):
    '''上传SSl证书到腾讯云SSL证书管理，返回新证书的id
    '''
    cert_info = {
        # Let's Encrypt 是通过中级 CA 机构颁发的证书，拿到的证书文件包含
        # whuzfb.cn.cer    ca.cer
        # 需要人为地将服务器证书与中间证书拼接在一起（acme.sh已经进行拼接）
        # fullchain.cer
        "cer": tools.read_file(cer_file),
        "key": tools.read_file(key_file),
        "type": "CA"
    }
    ssl_client = ssl.get_ssl_client_instance(id, key)
    cert_list = ssl.get_cert_list(ssl_client)
    for cert in cert_list:
        # 获取每个证书的id
        cert_id = cert.CertificateId
        # 获取每个证书的信息
        # if domain == ssl.get_cert_info(ssl_client, cert_id).Domain:
        #     # 删除证书
        #     # delete_cert(client, cert_id)
        #     # break
        #     print(cert_id)
    # 上传证书，获取新证书的id
    id = ssl.upload_cert(ssl_client, cert_info)
    if len(id)>0:
        return id
    else:
        exit("获取新证书id失败")


def run_config_cdn(id, key, domain, cert_id):
    '''该函数实现为CDN更新ssl证书的功能
    '''
    cdn_client = cdn.get_cdn_client_instance(id, key)
    cdns = cdn.get_cdn_detail_info(cdn_client)
    https = None
    for _cdn in cdns:
        if _cdn.Domain == domain:
            https = _cdn.Https
            break
    print(https)
    # generate_https(https)
    cdn.update_cdn_ssl(cdn_client, domain, cert_id)

def https_options_enabler(id, key, domain, http2, hsts, age, hsts_subdomain, ocsp):
    '''开启HTTPS配置中的部分选项
    '''
    cdn_client = cdn.get_cdn_client_instance(id, key)
    cdn.update_cdn_https_options(cdn_client, domain, http2, hsts, age, hsts_subdomain, ocsp)

def delete_old_ssls(id, key, cdn_domain, ignore_id):
    '''删除某个CDN的，除ignore_id以外的所有ssl证书
    '''
    ssl_client = ssl.get_ssl_client_instance(id, key)
    cert_list = ssl.get_cert_list(ssl_client)
    for cert in cert_list:
        cert_id = cert.CertificateId
        # 刚上传的这个证书不删除
        if cert_id == ignore_id:
            continue
        cert_info = ssl.get_cert_info(ssl_client, cert_id)
        cert_domain_and_alt_name = [cert_info.Domain] + cert_info.SubjectAltName
        matched = False
        # 判断域名匹配
        for cert_name in cert_domain_and_alt_name:
            if cert_name:
                # 判断主域名或多域名
                if cert_name == cdn_domain:
                    matched = True
                    break
                # 判断泛域名 m=['*','example.cn']
                m = cert_name.split('.', 1)
                n = cdn_domain.split('.', 1)
                if m[0] == "*" and m[1] == n[1]:
                    matched = True
                    break
        # 根据结果删除证书
        if matched:
            ssl.delete_cert(ssl_client, cert_id)


def run_config_ecdn(id, key, domain, cert_id):
    '''全站加速网络：为指定域名的CDN更新SSL证书
    '''
    ecdn_client = ecdn.get_ecdn_client_instance(id, key)
    ecdn.get_ecdn_basic_info(ecdn_client)
    cdns = ecdn.get_ecdn_detail_info(ecdn_client)
    ecdn.update_ecdn_ssl(ecdn_client, domain, cert_id)


def run_url_push(id, key, domain, urls_file):
    '''为CDN推送预热URL
    '''
    from time import sleep
    from os.path import isfile
    urls = []
    try:
        urls = tools.get_sitemap_urls("https://{}/sitemap.xml".format(domain))
    except Exception as e:
        print(repr(e))
    if isfile(urls_file):
        urls = urls + tools.get_urls_from_file(urls_file)
    cdn_client = cdn.get_cdn_client_instance(id, key)
    cdn_region = cdn.get_cdn_basic_info(cdn_client, domain)[0].Area
    # 预热URL支持area为global的参数，但是为了方便统计用量配额，手动分开刷新
    if cdn_region == 'global':
        cdn_region = ['mainland', 'overseas']
    else:
        cdn_region = [cdn_region]
    info = cdn.get_cdn_url_push_info(cdn_client)
    # 统计预热url数量
    cnt = 0
    # 根据加速域名配置的区域进行预热
    for i in info:
        if i.Area in cdn_region:
            grp_size = i.Batch
            available = i.Available
            print("正在对区域{0}进行url预热，剩余配额{1}条".format(i.Area, available))
            new_urls = tools.resize_url_list(urls, grp_size)
            for url_grp in new_urls:
                res = cdn.update_cdn_url_push(cdn_client, url_grp, i.Area)
                if res:
                    cnt = cnt + len(url_grp)
                    sleep(0.1)
                else:
                    break
    print("成功预热{}个URL".format(cnt))


def run_purge_url(id, key, domain, urls_file):
    '''为CDN推送刷新URL
    '''
    from time import sleep
    from os.path import isfile
    urls = []
    try:
        urls = tools.get_sitemap_urls("https://{}/sitemap.xml".format(domain))
    except Exception as e:
        print(repr(e))
    if isfile(urls_file):
        urls = urls + tools.get_urls_from_file(urls_file)
    cdn_client = cdn.get_cdn_client_instance(id, key)
    cdn_region = cdn.get_cdn_basic_info(cdn_client, domain)[0].Area
    # 刷新URL不支持area为global的参数
    if cdn_region == 'global':
        cdn_region = ['mainland', 'overseas']
    else:
        cdn_region = [cdn_region]
    info = cdn.get_cdn_purge_url_info(cdn_client)
    # 统计刷新url数量
    cnt = 0
    # 根据加速域名配置的区域进行刷新
    for i in info:
        if i.Area in cdn_region:
            grp_size = i.Batch
            available = i.Available
            print("正在对区域{0}进行url刷新，剩余配额{1}条".format(i.Area, available))
            new_urls = tools.resize_url_list(urls, grp_size)
            for url_grp in new_urls:
                res = cdn.update_cdn_purge_url(cdn_client, url_grp, i.Area)
                if res:
                    cnt = cnt + len(url_grp)
                    sleep(0.1)
                else:
                    break
    print("成功刷新{}个URL".format(cnt))


if __name__ == "__main__":
    SECRETID = config.SECRETID
    SECRETKEY = config.SECRETKEY
    # 泛域名证书
    if config.UPLOAD_SSL:
        cert_id = run_config_ssl(SECRETID, SECRETKEY, config.CER_FILE, config.KEY_FILE)
    else:
        cert_id = config.CERT_ID
    for my_domain in config.CDN_DOMAIN:
        if config.UPDATE_SSL:
            run_config_cdn(SECRETID, SECRETKEY, my_domain, cert_id)
        if config.ENABLE_HSTS or config.ENABLE_OCSP or config.ENABLE_HTTP2:
            https_options_enabler(SECRETID, SECRETKEY, my_domain, config.ENABLE_HTTP2, config.ENABLE_HSTS,
                                  config.HSTS_TIMEOUT_AGE, config.HSTS_INCLUDE_SUBDOMAIN, config.ENABLE_OCSP)
        if config.DELETE_OLD_CERTS:
            delete_old_ssls(SECRETID, SECRETKEY, my_domain, cert_id)
        if config.PUSH_URL:
            run_url_push(SECRETID, SECRETKEY, my_domain, config.URLS_FILE)
        if config.PURGE_URL:
            run_purge_url(SECRETID, SECRETKEY, my_domain, config.URLS_FILE)
        # ecdn是全球加速服务，与CDN不同，本账号没有开通该功能
        # run_config_ecdn(SECRETID, SECRETKEY, my_domain, cert_id)

