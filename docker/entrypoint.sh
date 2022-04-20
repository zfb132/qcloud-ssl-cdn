#!/bin/sh

# 添加crontab配置
cat > /var/spool/cron/crontabs/root <<-EOF
0 2 1 * * /data/update.sh &> /data/run.log
EOF
# 启动crontab服务
crond
# 马上执行证书更新
if [ ! -f /data/run.log ]; then
  touch /data/run.log
fi
if [ "${RUN_NOW:-"false"}" = "true" ]; then
  nohup /data/update.sh &> /data/run.log &
fi

tail -f /data/run.log