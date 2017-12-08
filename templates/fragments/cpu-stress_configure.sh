#!/bin/bash
. /etc/sysconfig/heat-params

echo "Start to configure cpu stressor as a client"

sudo apt update && apt install -y libmicrohttpd10 \
                       libhwloc5 libcurl4-openssl-dev
wget -O stressor.tar.gz https://owncloud.gwdg.de/index.php/s/bx2q1X5OkjgfgI9/download
tar zxvf stressor.tar.gz
cd bin
nohup sudo ./launcher &

