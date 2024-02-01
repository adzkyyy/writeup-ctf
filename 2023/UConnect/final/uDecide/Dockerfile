FROM ubuntu:20.04

RUN apt-get update && apt-get -y install socat gcc gcc-multilib

COPY service /service
WORKDIR /service

RUN chmod 555 uDecide

EXPOSE 10003
USER nobody

CMD socat -v tcp-l:10003,reuseaddr,fork exec:'./uDecide'
