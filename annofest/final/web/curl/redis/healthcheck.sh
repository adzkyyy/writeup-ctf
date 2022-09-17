#!/bin/bash

redis-server /etc/redis.conf &

while true; do
    timeout 2 redis-cli -h redis-hub -p 6378
    if [[ $? -ne 0 ]]; then
        exit 1
    fi
    sleep 10
done