FROM ubuntu:20.04

RUN apt-get update && apt-get -y install socat gcc gcc-multilib

COPY service /service
WORKDIR /service

RUN chmod 555 uSystemv2

EXPOSE 10001
USER nobody

CMD socat -v tcp-l:10001,reuseaddr,fork exec:'./uSystemv2'
