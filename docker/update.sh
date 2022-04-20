#!/bin/sh

if [ "${ACME_ENABLED}" != "false" ]; then
  # 使用acme获取/更新证书
  cd /root/.acme.sh
  ./acme.sh ${ACME_PARAMS} --force --issue --cert-home ${CERT_HOME} -d ${ACME_DOMAIN} -d *.${ACME_DOMAIN} --dns dns_dp 
fi

cd /data && python main.py