FROM ubuntu:20.04

RUN apt-get update && apt-get -y install socat gcc gcc-multilib

COPY service /service
WORKDIR /service

RUN chmod 555 uMemo

EXPOSE 10004
USER nobody

CMD socat -v tcp-l:10004,reuseaddr,fork exec:'./uMemo'
