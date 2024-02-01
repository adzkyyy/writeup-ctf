FROM vulhub/redis:5.0.7

COPY ./Web/curl/redis/redis.conf /etc/redis.conf
COPY ./Web/curl/redis/healthcheck.sh /healthcheck.sh
COPY ./Web/flag/curl.flag /flag
RUN chmod 444 /flag && chmod +x /healthcheck.sh 

CMD /healthcheck.sh 