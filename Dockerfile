FROM python:alpine

LABEL AUTHOR="monlor"

ENV LANG="C.UTF-8" 
ENV TZ="Asia/Shanghai" 
ENV CERT_HOME="/data/certs"
ENV WORK_DIR="/data"
ENV ACME_HOME="/root/.acme.sh"

WORKDIR /data

COPY api /data/api
COPY main.py /data/
COPY requirements.txt /data/
COPY docker/entrypoint.sh /
COPY docker/update.sh /data

RUN apk update && apk add --no-cache curl openssl socat && \
    ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    pip install -r requirements.txt && \
    chmod +x /entrypoint.sh /data/update.sh && \
    curl https://get.acme.sh | sh -s email=my@example.com

VOLUME ["/data/certs"]
ENTRYPOINT [ "/entrypoint.sh" ]