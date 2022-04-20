## 腾讯云自动SSL证书上传及替换
功能：  
* 把本地的SSL证书上传到腾讯云[SSL证书](https://console.cloud.tencent.com/ssl)，并记录id
* 为CDN服务更换指定id的SSL证书
* 根据网址，批量预热URL

目的：
* 把利用[acme.sh](https://github.com/acmesh-official/acme.sh)申请的`Let's Encrypt`证书上传到腾讯云
* 由于多次申请`TrustAsia`的一年期免费单域名证书失败，所以准备使用`Let's Encrypt`证书
* 该程序已将每一个步骤都实现：自动上传SSL并替换CDN的证书
* 为了使网站访问更快，每天预热URL（可以单独抽出该函数，运行在[腾讯云函数](https://github.com/zfb132/auto_push_url)）


## 部署方式

### 使用 Docker 快速部署

每月 1 号凌晨 2 点定时执行证书更新

* `ACME_DNS_TYPE`: Acme 的 dns 类型，你可以选择你的 dns 类型并配置[环境变量密钥](https://github.com/acmesh-official/acme.sh/wiki/dnsapi)
* `ACME_DOMAIN`: 你的顶级域名，例如：monlor.com，自动申请证书 monlor.com/*.monlor.com
* `SECRETID`: 腾讯云 Secret Id
* `SECRETKEY`: 腾讯云 Secret Key
* `CDN_DOMAIN`: CDN 域名，多个域名用逗号分隔
* `RUN_NOW`: 是否在 Docker 启动时执行程序

```bash
docker run -d \
  --name qcloud-ssl-cdn \
  --restart=unless-stopped \ 
  -e DP_Id=xxx \
  -e DP_Key=xxx \ 
  -e ACME_DNS_TYPE=dns_dp \ 
  -e ACME_DOMAIN=monlor.com \
  -e SECRETID=xxx \
  -e SECRETKEY=xxx \
  -e CDN_DOMAIN=www.monlor.com \
  -e RUN_NOW=true \
  ghcr.io/monlor/qcloud-ssl-cdn:main
```

其他变量

* `ACME_ENABLED`: 是否启用 acme，不启用将证书映射到容器`/data/certs`目录
* `PUSH_URLS`: CDN 刷新/预热地址，逗号分隔


### 使用 GitHub Action 部署

Fork 此项目，配置以下 Github Action Secrets

* `ACME_DNS_TYPE`: Acme 的 dns 类型，你可以选择你的 dns 类型并配置[环境变量密钥](https://github.com/acmesh-official/acme.sh/wiki/dnsapi)
* `ACME_DOMAIN`: 你的顶级域名，例如：monlor.com，自动申请证书 monlor.com/*.monlor.com
* `SECRETID`: 腾讯云 Secret Id
* `SECRETKEY`: 腾讯云 Secret Key
* `CDN_DOMAIN`: CDN 域名，多个域名用逗号分隔
* `BARK_HOST`: [Bark](https://github.com/Finb/Bark) 消息通知 Host
* `BARK_KEY`: [Bark](https://github.com/Finb/Bark) 消息通知 Key

### 手动部署

#### 使用acme.sh申请证书
[安装及简单使用](https://blog.whuzfb.cn/blog/2020/07/07/web_https/#3-%E5%AE%89%E8%A3%85acme%E8%87%AA%E5%8A%A8%E7%AD%BE%E5%8F%91%E8%AF%81%E4%B9%A6)  
对于本程序  
```bash
# 腾讯云支持使用单域名和泛域名的证书，例如申请泛域名
acme.sh --issue  -d "whuzfb.cn" -d "*.whuzfb.cn" --dns dns_dp
# 申请单域名
# acme.sh --issue  -d "blog.whuzfb.cn" --dns dns_dp
```

#### 修改config.example.py参数
根据注释修改每一项内容  
然后重命名为`config.py`

## 主要函数
`ssl.get_cert_list(client)`：获取所有的SSL证书列表  
`ssl.get_cert_info(client, cert_id)`：根据id获取SSL证书的信息  
`ssl.get_cert_detail(client, cert_id)`：根据id获取SSL证书的详情  
`ssl.delete_cert(client, cert_id)`：删除指定id的SSL证书  
`ssl.upload_cert(client, local_cert_info)`：把本地的SSL证书上传到腾讯云，返回新证书的id  


`cdn.get_cdn_detail_info(client)`：获取所有CDN的详细信息，返回列表  
`cdn.get_cdn_url_push_info(client)`：查询CDN预热配额和每日可用量  
`cdn.update_cdn_url_push(client, urls)`：指定 URL 资源列表加载至 CDN 节点，支持指定加速区域预热；默认情况下境内、境外每日预热 URL 限额为各 1000 条，每次最多可提交 20 条  
`cdn.get_cdn_purge_url_info(client)`：查询CDN刷新配额和每日可用量  
`cdn.update_cdn_purge_url(client, urls)`：指定 URL 资源的刷新，支持指定加速区域刷新；默认情况下境内、境外每日刷新 URL 限额为各 10000 条，每次最多可提交 1000 条  
`cdn.update_cdn_ssl(client, domain, cert_id)`：为指定域名的CDN更换SSL证书  


`ecdn.get_ecdn_basic_info(client)`：获取所有ECDN（全球加速服务）的基本信息，返回列表  
`ecdn.get_ecdn_detail_info(client)`：获取所有ECDN的详细信息，返回列表  
`ecdn.update_ecdn_ssl(client, domain, cert_id)`：为指定域名的CDN的更换SSL证书  
