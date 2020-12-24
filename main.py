#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2020-12-02 15:56
from api import cdn, ecdn, ssl, tools
import config

def run_config_ssl(id, key, domain, cer_file, key_file):
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
        if domain == ssl.get_cert_info(ssl_client, cert_id).Domain:
            # 删除证书
            # delete_cert(client, cert_id)
            # break
            print(cert_id)
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
    urls = tools.get_sitemap_urls("https://{}/sitemap.xml".format(domain))
    if isfile(urls_file):
        urls = urls + tools.get_urls_from_file(urls_file)
    cdn_client = cdn.get_cdn_client_instance(id, key)
    info = cdn.get_cdn_url_push_info(cdn_client)
    # 统计预热url数量
    cnt = 0
    # 只对国内进行预热
    for i in info:
        if i.Area == "mainland":
            grp_size = i.Batch
            available = i.Available
            print("正在对区域{0}进行url预热，剩余配额{1}条".format(i.Area, available))
            new_urls = tools.resize_url_list(urls, grp_size)
            for url_grp in new_urls:
                res = cdn.update_cdn_url_push(cdn_client, url_grp)
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
    urls = tools.get_sitemap_urls("https://{}/sitemap.xml".format(domain))
    if isfile(urls_file):
        urls = urls + tools.get_urls_from_file(urls_file)
    cdn_client = cdn.get_cdn_client_instance(id, key)
    info = cdn.get_cdn_purge_url_info(cdn_client)
    # 统计刷新url数量
    cnt = 0
    # 只对国内进行刷新
    for i in info:
        if i.Area == "mainland":
            grp_size = i.Batch
            available = i.Available
            print("正在对区域{0}进行url刷新，剩余配额{1}条".format(i.Area, available))
            new_urls = tools.resize_url_list(urls, grp_size)
            for url_grp in new_urls:
                res = cdn.update_cdn_purge_url(cdn_client, url_grp)
                if res:
                    cnt = cnt + len(url_grp)
                    sleep(0.1)
                else:
                    break
    print("成功刷新{}个URL".format(cnt))


if __name__ == "__main__":
    SECRETID = config.SECRETID
    SECRETKEY = config.SECRETKEY
    my_domain = config.CDN_DOMAIN
    if config.UPLOAD_SSL:
        cert_id = run_config_ssl(SECRETID, SECRETKEY, my_domain, config.CER_FILE, config.KEY_FILE)
    else:
        cert_id = config.CERT_ID
    if config.UPDATE_SSL:
        run_config_cdn(SECRETID, SECRETKEY, my_domain, cert_id)
    if config.PUSH_URL:
        run_url_push(SECRETID, SECRETKEY, my_domain, config.URLS_FILE)
    if config.PURGE_URL:
        run_purge_url(SECRETID, SECRETKEY, my_domain, config.URLS_FILE)
    # ecdn是全球加速服务，与CDN不同，本账号没有开通该功能
    # run_config_ecdn(SECRETID, SECRETKEY, my_domain, cert_id)

